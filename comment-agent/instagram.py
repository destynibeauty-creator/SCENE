"""Instagram API (Instagram Login) calls: read comments, post replies, webhooks."""

import hashlib
import hmac

import requests

import config

BASE = f"https://graph.instagram.com/{config.GRAPH_VERSION}"
TIMEOUT = 20


class InstagramError(RuntimeError):
    pass


def _get(path: str, token: str, **params) -> dict:
    r = requests.get(f"{BASE}/{path}", params={**params, "access_token": token}, timeout=TIMEOUT)
    if not r.ok:
        raise InstagramError(f"GET {path} failed ({r.status_code}): {r.text}")
    return r.json()


def _post(path: str, token: str, **data) -> dict:
    r = requests.post(f"{BASE}/{path}", data={**data, "access_token": token}, timeout=TIMEOUT)
    if not r.ok:
        raise InstagramError(f"POST {path} failed ({r.status_code}): {r.text}")
    return r.json()


def get_me(token: str) -> dict:
    """Who does this token belong to? Returns user_id + username."""
    return _get("me", token, fields="user_id,username")


def get_media(media_id: str, token: str) -> dict:
    return _get(media_id, token, fields="id,caption,media_type,media_product_type,permalink")


def recent_media(token: str, limit: int = 10) -> list[dict]:
    return _get("me/media", token, fields="id,caption,permalink,timestamp", limit=limit).get("data", [])


def media_comments(media_id: str, token: str, limit: int = 50) -> list[dict]:
    data = _get(
        f"{media_id}/comments",
        token,
        fields="id,text,username,timestamp,from,replies{id,username}",
        limit=limit,
    )
    return data.get("data", [])


def reply_to_comment(comment_id: str, message: str, token: str) -> str:
    """Posts a public reply under the comment. Returns the new reply's ID."""
    return _post(f"{comment_id}/replies", token, message=message)["id"]


def subscribe_to_comment_webhooks(token: str) -> dict:
    return _post("me/subscribed_apps", token, subscribed_fields="comments")


def refresh_long_lived_token(token: str) -> dict:
    """Long-lived tokens last 60 days. Refreshing gives a fresh 60 days."""
    r = requests.get(
        "https://graph.instagram.com/refresh_access_token",
        params={"grant_type": "ig_refresh_token", "access_token": token},
        timeout=TIMEOUT,
    )
    if not r.ok:
        raise InstagramError(f"Token refresh failed ({r.status_code}): {r.text}")
    return r.json()


def signature_is_valid(raw_body: bytes, header: str | None, app_secret: str) -> bool:
    """Meta signs every webhook with your app secret. Reject anything unsigned."""
    if not header or not header.startswith("sha256=") or not app_secret:
        return False
    expected = hmac.new(app_secret.encode(), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, header.removeprefix("sha256="))


def comments_from_webhook(payload: dict) -> list[dict]:
    """Flattens a webhook payload into simple comment dicts."""
    found = []
    if payload.get("object") != "instagram":
        return found
    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            if change.get("field") != "comments":
                continue
            v = change.get("value", {})
            found.append({
                "account_id": entry.get("id", ""),
                "comment_id": v.get("id", ""),
                "parent_id": v.get("parent_id"),
                "text": v.get("text", ""),
                "from_id": v.get("from", {}).get("id", ""),
                "username": v.get("from", {}).get("username", ""),
                "media_id": v.get("media", {}).get("id", ""),
            })
    return found
