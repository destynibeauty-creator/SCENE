"""Run with:  python -m pytest tests   (no API keys needed - Claude and Instagram are faked)"""

import hashlib
import hmac
import json
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


@pytest.fixture()
def env(tmp_path, monkeypatch):
    accounts = [{"name": "richdestyni", "ig_user_id": "111", "access_token": "tok"}]
    (tmp_path / "accounts.json").write_text(json.dumps(accounts))
    monkeypatch.setenv("ACCOUNTS_FILE", str(tmp_path / "accounts.json"))
    import config
    monkeypatch.setattr(config, "DB_PATH", tmp_path / "test.db")
    monkeypatch.setattr(config, "MIN_SECONDS_BETWEEN_REPLIES", 0)
    monkeypatch.setattr(config, "AUTO_POST", False)

    import agent, drafter, instagram
    posted = []
    monkeypatch.setattr(instagram, "get_media", lambda mid, tok: {"caption": "New episode 🎬"})
    monkeypatch.setattr(instagram, "reply_to_comment",
                        lambda cid, msg, tok: posted.append((cid, msg)) or "reply-1")

    def fake_draft(comment_text, **kw):
        if "refund" in comment_text:
            return drafter.Decision(action="needs_human", reply="DM me", reason="money")
        if "follow4follow" in comment_text:
            return drafter.Decision(action="skip", reply="", reason="spam")
        return drafter.Decision(action="reply", reply="Thank you 🤍", reason="compliment")
    monkeypatch.setattr(drafter, "draft_reply", fake_draft)
    return agent, config, posted


def comment(cid, text, from_id="999", username="fan"):
    return {"account_id": "111", "comment_id": cid, "parent_id": None, "text": text,
            "from_id": from_id, "username": username, "media_id": "m1"}


def test_routes_comments_by_decision(env):
    agent, config, posted = env
    import store
    agent.handle_comment(comment("c1", "this is so good"))
    agent.handle_comment(comment("c2", "I want a refund"))
    agent.handle_comment(comment("c3", "follow4follow"))
    assert store.get("c1")["status"] == "pending"
    assert store.get("c2")["status"] == "needs_human"
    assert store.get("c3")["status"] == "skipped"
    assert store.get("c1")["caption"] == "New episode 🎬"
    assert posted == []  # auto-post is off


def test_ignores_own_comments_and_duplicates(env):
    agent, config, posted = env
    import store
    agent.handle_comment(comment("c4", "my own reply", from_id="111", username="richdestyni"))
    assert store.get("c4") is None
    agent.handle_comment(comment("c5", "love it"))
    agent.handle_comment(comment("c5", "love it"))
    assert len(store.by_status("pending")) == 1


def test_auto_post_and_manual_post(env, monkeypatch):
    agent, config, posted = env
    import store
    monkeypatch.setattr(config, "AUTO_POST", True)
    agent.handle_comment(comment("c6", "amazing"))
    agent.handle_comment(comment("c7", "refund please"))
    assert posted == [("c6", "Thank you 🤍")]
    assert store.get("c7")["status"] == "needs_human"  # flagged ones never auto-post
    agent.post_reply("c7", "Sending you a DM now 🙏🏾")
    assert store.get("c7")["status"] == "posted"
    assert posted[-1] == ("c7", "Sending you a DM now 🙏🏾")


def test_webhook_signature_and_parsing():
    import instagram
    body = json.dumps({"object": "instagram", "entry": [{"id": "111", "changes": [{
        "field": "comments",
        "value": {"id": "c9", "text": "hi", "from": {"id": "5", "username": "a"}, "media": {"id": "m1"}},
    }]}]}).encode()
    sig = "sha256=" + hmac.new(b"secret", body, hashlib.sha256).hexdigest()
    assert instagram.signature_is_valid(body, sig, "secret")
    assert not instagram.signature_is_valid(body, sig, "wrong")
    assert not instagram.signature_is_valid(body, None, "secret")
    [c] = instagram.comments_from_webhook(json.loads(body))
    assert c == {"account_id": "111", "comment_id": "c9", "parent_id": None, "text": "hi",
                 "from_id": "5", "username": "a", "media_id": "m1"}


def test_webhook_endpoint(env, monkeypatch):
    agent, config, posted = env
    monkeypatch.setattr(config, "APP_SECRET", "secret")
    monkeypatch.setattr(config, "WEBHOOK_VERIFY_TOKEN", "vt")
    import app as app_module
    queued = []
    monkeypatch.setattr(agent, "enqueue_comment", queued.append)
    client = app_module.app.test_client()

    r = client.get("/webhook?hub.mode=subscribe&hub.verify_token=vt&hub.challenge=42")
    assert r.status_code == 200 and r.data == b"42"
    assert client.get("/webhook?hub.mode=subscribe&hub.verify_token=no&hub.challenge=42").status_code == 403

    body = json.dumps({"object": "instagram", "entry": [{"id": "111", "changes": [
        {"field": "comments", "value": {"id": "c10", "text": "yo", "from": {"id": "5"}}}]}]}).encode()
    sig = "sha256=" + hmac.new(b"secret", body, hashlib.sha256).hexdigest()
    assert client.post("/webhook", data=body, headers={"X-Hub-Signature-256": "sha256=bad"}).status_code == 403
    assert client.post("/webhook", data=body, content_type="application/json",
                       headers={"X-Hub-Signature-256": sig}).status_code == 200
    assert queued[0]["comment_id"] == "c10"


def test_dashboard_requires_password(env, monkeypatch):
    agent, config, posted = env
    monkeypatch.setattr(config, "DASHBOARD_PASSWORD", "pw")
    import app as app_module
    client = app_module.app.test_client()
    assert client.get("/").status_code == 401
    import base64
    auth = {"Authorization": "Basic " + base64.b64encode(b"me:pw").decode()}
    agent.handle_comment(comment("c11", "so pretty"))
    r = client.get("/", headers=auth)
    assert r.status_code == 200 and b"so pretty" in r.data
