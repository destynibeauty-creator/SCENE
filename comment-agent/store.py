"""A small SQLite database that remembers every comment and what happened to it."""

import sqlite3
import time
from contextlib import contextmanager

import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS comments (
    comment_id   TEXT PRIMARY KEY,
    account_id   TEXT NOT NULL,
    media_id     TEXT,
    username     TEXT,
    text         TEXT,
    caption      TEXT,
    draft        TEXT,
    reason       TEXT,
    -- pending | needs_human | posted | skipped | rejected | error
    status       TEXT NOT NULL,
    reply_id     TEXT,
    error        TEXT,
    created_at   REAL NOT NULL,
    updated_at   REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_status ON comments(status);
"""


@contextmanager
def db():
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        conn.executescript(SCHEMA)
        yield conn
        conn.commit()
    finally:
        conn.close()


def seen(comment_id: str) -> bool:
    with db() as c:
        return c.execute("SELECT 1 FROM comments WHERE comment_id=?", (comment_id,)).fetchone() is not None


def add(comment: dict, caption: str, draft: str, reason: str, status: str) -> bool:
    """Returns False if the comment was already stored (webhooks can repeat)."""
    now = time.time()
    with db() as c:
        cur = c.execute(
            """INSERT OR IGNORE INTO comments
               (comment_id, account_id, media_id, username, text, caption, draft, reason,
                status, created_at, updated_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (comment["comment_id"], comment["account_id"], comment.get("media_id"),
             comment.get("username"), comment.get("text"), caption, draft, reason,
             status, now, now),
        )
        return cur.rowcount == 1


def get(comment_id: str):
    with db() as c:
        return c.execute("SELECT * FROM comments WHERE comment_id=?", (comment_id,)).fetchone()


def update(comment_id: str, **fields) -> None:
    fields["updated_at"] = time.time()
    cols = ", ".join(f"{k}=?" for k in fields)
    with db() as c:
        c.execute(f"UPDATE comments SET {cols} WHERE comment_id=?", (*fields.values(), comment_id))


def by_status(*statuses: str, limit: int = 200):
    marks = ",".join("?" * len(statuses))
    with db() as c:
        return c.execute(
            f"SELECT * FROM comments WHERE status IN ({marks}) ORDER BY created_at DESC LIMIT ?",
            (*statuses, limit),
        ).fetchall()


def last_post_time() -> float:
    with db() as c:
        row = c.execute("SELECT MAX(updated_at) FROM comments WHERE status='posted'").fetchone()
        return row[0] or 0.0
