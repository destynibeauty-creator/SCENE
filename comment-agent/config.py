"""Settings, read from environment variables (or a local .env file)."""

import json
import os
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _load_dotenv(path: Path) -> None:
    """Tiny .env reader so there is one less package to install."""
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_dotenv(HERE / ".env")


@dataclass
class Account:
    name: str          # e.g. "richdestyni"
    ig_user_id: str    # the Instagram professional account ID
    access_token: str  # long-lived Instagram user access token
    voice_notes: str = ""  # extra voice notes just for this account


def load_accounts() -> dict[str, Account]:
    """Accounts live in accounts.json (kept out of git). Keyed by ig_user_id."""
    path = Path(os.environ.get("ACCOUNTS_FILE", HERE / "accounts.json"))
    if not path.exists():
        return {}
    accounts = [Account(**a) for a in json.loads(path.read_text())]
    return {a.ig_user_id: a for a in accounts}


def save_accounts(accounts: dict[str, Account]) -> None:
    path = Path(os.environ.get("ACCOUNTS_FILE", HERE / "accounts.json"))
    path.write_text(json.dumps([a.__dict__ for a in accounts.values()], indent=2) + "\n")


def _bool(name: str, default: bool) -> bool:
    return os.environ.get(name, str(default)).strip().lower() in ("1", "true", "yes", "on")


GRAPH_VERSION = os.environ.get("IG_GRAPH_VERSION", "v24.0")
APP_SECRET = os.environ.get("IG_APP_SECRET", "")
WEBHOOK_VERIFY_TOKEN = os.environ.get("WEBHOOK_VERIFY_TOKEN", "")
DASHBOARD_PASSWORD = os.environ.get("DASHBOARD_PASSWORD", "")

# OFF (default): every reply waits in the dashboard for your OK.
# ON: safe, simple replies post by themselves. Anything sensitive still waits.
AUTO_POST = _bool("AUTO_POST", False)

# Wait at least this many seconds between replies so it never looks bot-like.
MIN_SECONDS_BETWEEN_REPLIES = int(os.environ.get("MIN_SECONDS_BETWEEN_REPLIES", "45"))

CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "claude-opus-5-5")
DB_PATH = Path(os.environ.get("DB_PATH", HERE / "comments.db"))
