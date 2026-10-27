"""Web server: receives Instagram webhooks and serves Destyni's approval dashboard.

Run:  python app.py      (one process only - the worker thread lives inside it)
"""

import hmac
import logging
import os
from functools import wraps

from flask import Flask, Response, abort, jsonify, redirect, render_template_string, request, url_for

import agent
import config
import drafter
import instagram
import store

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
app = Flask(__name__)
agent.start_worker()


# ---------------- webhook ----------------

@app.get("/webhook")
def verify_webhook():
    """Meta calls this once when you add the webhook URL in the app dashboard."""
    if (request.args.get("hub.mode") == "subscribe"
            and config.WEBHOOK_VERIFY_TOKEN
            and hmac.compare_digest(request.args.get("hub.verify_token", ""), config.WEBHOOK_VERIFY_TOKEN)):
        return request.args.get("hub.challenge", "")
    abort(403)


@app.post("/webhook")
def receive_webhook():
    raw = request.get_data()
    if not instagram.signature_is_valid(raw, request.headers.get("X-Hub-Signature-256"), config.APP_SECRET):
        abort(403)
    for comment in instagram.comments_from_webhook(request.get_json(silent=True) or {}):
        agent.enqueue_comment(comment)
    return "ok"  # answer fast; drafting happens in the background


# ---------------- dashboard ----------------

def require_password(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not config.DASHBOARD_PASSWORD:
            return Response("Set DASHBOARD_PASSWORD in your .env first.", 503)
        if not auth or not hmac.compare_digest(auth.password or "", config.DASHBOARD_PASSWORD):
            return Response("Login required", 401, {"WWW-Authenticate": 'Basic realm="Comments"'})
        return view(*args, **kwargs)
    return wrapper


PAGE = """<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Comment Desk</title>
<style>
:root{--bg:#0b0b0d;--card:#17171b;--line:#2a2a31;--text:#f2f2f4;--muted:#9a9aa5;--cyan:#00e5ff;--mag:#f600a2}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:16px/1.45 -apple-system,system-ui,sans-serif}
main{max-width:720px;margin:0 auto;padding:16px}
h1{font-size:22px;margin:8px 0 4px}h2{font-size:17px;margin:28px 0 10px;color:var(--cyan)}
.sub{color:var(--muted);font-size:14px;margin:0 0 8px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px;margin:10px 0}
.who{font-weight:600}.meta{color:var(--muted);font-size:13px}
.flag{display:inline-block;font-size:12px;padding:2px 8px;border-radius:99px;background:#3a1030;color:#ff8bd3;margin-left:6px}
.cap{color:var(--muted);font-size:13px;margin:6px 0;max-height:3.2em;overflow:hidden}
.comment{margin:8px 0;font-size:16px}
textarea,input{width:100%;background:#0f0f12;color:var(--text);border:1px solid var(--line);border-radius:10px;padding:10px;font:inherit}
textarea{min-height:70px}
.row{display:flex;gap:8px;margin-top:8px}
button{flex:1;border:0;border-radius:10px;padding:11px;font:600 15px system-ui;cursor:pointer}
.go{background:var(--cyan);color:#000}.no{background:#2a2a31;color:var(--text)}
.small{font-size:13px;color:var(--muted)}.err{color:#ff8080;font-size:13px}
.done{opacity:.75}
</style></head><body><main>
<h1>Comment Desk</h1>
<p class="sub">Auto-post is <b>{{ 'ON' if auto_post else 'OFF' }}</b>.
{{ 'Simple replies post by themselves. Flagged ones wait here.' if auto_post else 'Every reply waits for your OK.' }}</p>

<h2>Waiting on you ({{ waiting|length }})</h2>
{% for c in waiting %}
<form class="card" method="post" action="{{ url_for('decide', comment_id=c.comment_id) }}">
  <div class="who">@{{ c.username }}{% if c.status == 'needs_human' %}<span class="flag">flagged</span>{% endif %}
  {% if c.status == 'error' %}<span class="flag">failed</span>{% endif %}</div>
  <div class="meta">{{ accounts.get(c.account_id, c.account_id) }} · {{ c.reason or '' }}</div>
  {% if c.caption %}<div class="cap">Post: {{ c.caption }}</div>{% endif %}
  <div class="comment">“{{ c.text }}”</div>
  {% if c.error %}<div class="err">{{ c.error }}</div>{% endif %}
  <textarea name="reply">{{ c.draft or '' }}</textarea>
  <div class="row"><button class="go" name="do" value="post">Post reply</button>
  <button class="no" name="do" value="skip">Skip</button></div>
</form>
{% else %}<p class="small">All caught up. 🎬</p>{% endfor %}

<h2>Facebook reply helper</h2>
<p class="sub">Facebook won't let apps reply on your profile, so paste a comment here, copy the reply, and post it yourself.</p>
<form class="card" method="post" action="{{ url_for('facebook_helper') }}">
  <input name="post" placeholder="What was the post about? (optional)" value="{{ fb_post or '' }}">
  <div style="height:8px"></div>
  <textarea name="comment" placeholder="Paste the comment here">{{ fb_comment or '' }}</textarea>
  <div class="row"><button class="go">Write my reply</button></div>
  {% if fb_reply %}<div style="height:10px"></div><textarea id="fbout" readonly>{{ fb_reply }}</textarea>
  <div class="row"><button class="no" type="button" onclick="navigator.clipboard.writeText(document.getElementById('fbout').value);this.textContent='Copied ✅'">Copy</button></div>
  {% if fb_note %}<p class="small">{{ fb_note }}</p>{% endif %}{% endif %}
</form>

<h2>Recently handled</h2>
{% for c in recent %}
<div class="card done"><div class="who">@{{ c.username }} <span class="meta">· {{ c.status }}</span></div>
<div class="comment">“{{ c.text }}”</div>{% if c.status in ('posted','sending') %}<div class="small">↳ {{ c.draft }}</div>{% endif %}</div>
{% else %}<p class="small">Nothing yet.</p>{% endfor %}
</main></body></html>"""


def _render(**extra):
    accounts = {a.ig_user_id: "@" + a.name for a in config.load_accounts().values()}
    return render_template_string(
        PAGE,
        waiting=store.by_status("needs_human", "pending", "error"),
        recent=store.by_status("posted", "sending", "skipped", "rejected", limit=30),
        accounts=accounts,
        auto_post=config.AUTO_POST,
        **extra,
    )


@app.get("/")
@require_password
def dashboard():
    return _render()


@app.post("/comment/<comment_id>")
@require_password
def decide(comment_id):
    if request.form.get("do") == "post":
        agent.enqueue_post(comment_id, request.form.get("reply", ""))
    else:
        store.update(comment_id, status="rejected")
    return redirect(url_for("dashboard"))


@app.post("/facebook")
@require_password
def facebook_helper():
    comment = request.form.get("comment", "").strip()
    post = request.form.get("post", "").strip()
    if not comment:
        return redirect(url_for("dashboard"))
    d = drafter.draft_reply(comment_text=comment, username="someone", caption=post,
                            account_name="Destyni Monique (Facebook profile)")
    note = {"skip": "Looks like spam - probably no reply needed.",
            "needs_human": f"Heads up: {d.reason}. Read this one carefully before posting."}.get(d.action, "")
    return _render(fb_comment=comment, fb_post=post, fb_reply=d.reply or "(no reply suggested)", fb_note=note)


@app.get("/health")
def health():
    return jsonify(ok=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
