"""The core loop: new comment -> Claude draft -> queue or post."""

import logging
import queue
import threading
import time

import config
import drafter
import instagram
import store

log = logging.getLogger("agent")

_jobs: queue.Queue = queue.Queue()
_caption_cache: dict[str, str] = {}


def _caption(media_id: str, token: str) -> str:
    if not media_id:
        return ""
    if media_id not in _caption_cache:
        try:
            _caption_cache[media_id] = instagram.get_media(media_id, token).get("caption", "") or ""
        except instagram.InstagramError as e:
            log.warning("Could not load caption for %s: %s", media_id, e)
            return ""
    return _caption_cache[media_id]


def handle_comment(comment: dict) -> None:
    """Draft a reply for one new comment, then queue it or post it."""
    accounts = config.load_accounts()
    account = accounts.get(comment["account_id"])
    if account is None:
        log.info("Comment for unknown account %s, ignoring", comment["account_id"])
        return
    # Never reply to ourselves (our own replies come back as webhook events too).
    if comment.get("from_id") == account.ig_user_id or comment.get("username") == account.name:
        return
    if not comment.get("comment_id") or store.seen(comment["comment_id"]):
        return

    caption = _caption(comment.get("media_id", ""), account.access_token)
    decision = drafter.draft_reply(
        comment_text=comment.get("text", ""),
        username=comment.get("username", ""),
        caption=caption,
        account_name=account.name,
        account_notes=account.voice_notes,
        is_reply_in_thread=bool(comment.get("parent_id")),
    )
    status = {"reply": "pending", "skip": "skipped", "needs_human": "needs_human"}[decision.action]
    if not store.add(comment, caption, decision.reply, decision.reason, status):
        return  # another delivery of the same comment got here first
    log.info("@%s on @%s -> %s (%s)", comment.get("username"), account.name, status, decision.reason)

    if status == "pending" and config.AUTO_POST:
        post_reply(comment["comment_id"])


def post_reply(comment_id: str, text: str | None = None) -> None:
    row = store.get(comment_id)
    if row is None or row["status"] == "posted":
        return
    account = config.load_accounts().get(row["account_id"])
    if account is None:
        store.update(comment_id, status="error", error="Account no longer configured")
        return
    message = (text if text is not None else row["draft"] or "").strip()
    if not message:
        store.update(comment_id, status="error", error="Empty reply")
        return

    # Space replies out so the account never looks automated.
    wait = store.last_post_time() + config.MIN_SECONDS_BETWEEN_REPLIES - time.time()
    if wait > 0:
        time.sleep(wait)

    try:
        reply_id = instagram.reply_to_comment(comment_id, message, account.access_token)
    except instagram.InstagramError as e:
        log.error("Reply to %s failed: %s", comment_id, e)
        store.update(comment_id, status="error", draft=message, error=str(e)[:500])
        return
    store.update(comment_id, status="posted", draft=message, reply_id=reply_id, error=None)
    log.info("Posted reply to %s", comment_id)


# ---- background worker so webhooks can answer Meta instantly ----

def enqueue_comment(comment: dict) -> None:
    _jobs.put(("comment", comment))


def enqueue_post(comment_id: str, text: str) -> None:
    store.update(comment_id, status="sending", draft=text)
    _jobs.put(("post", (comment_id, text)))


def _worker() -> None:
    while True:
        kind, item = _jobs.get()
        try:
            if kind == "comment":
                handle_comment(item)
            elif kind == "post":
                post_reply(*item)
        except Exception:  # keep the worker alive no matter what
            log.exception("Job %s failed", kind)
        finally:
            _jobs.task_done()


_started = False


def start_worker() -> None:
    global _started
    if not _started:
        threading.Thread(target=_worker, daemon=True, name="comment-worker").start()
        _started = True


# ---- polling: a backup for webhooks, and a way to test before webhooks are set up ----

def poll_once(posts_per_account: int = 5) -> int:
    """Checks the latest posts on every account for comments we have not handled."""
    found = 0
    for account in config.load_accounts().values():
        for media in instagram.recent_media(account.access_token, limit=posts_per_account):
            _caption_cache[media["id"]] = media.get("caption", "") or ""
            for c in instagram.media_comments(media["id"], account.access_token):
                replied_by_me = any(
                    r.get("username") == account.name for r in c.get("replies", {}).get("data", [])
                )
                if replied_by_me or store.seen(c["id"]):
                    continue
                handle_comment({
                    "account_id": account.ig_user_id,
                    "comment_id": c["id"],
                    "parent_id": None,
                    "text": c.get("text", ""),
                    "from_id": c.get("from", {}).get("id", ""),
                    "username": c.get("username", ""),
                    "media_id": media["id"],
                })
                found += 1
    return found
