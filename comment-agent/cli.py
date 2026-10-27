"""Setup and maintenance commands.

python cli.py add-account <ACCESS_TOKEN>   connect an Instagram account
python cli.py subscribe                    turn on comment webhooks for every account
python cli.py poll                         check recent posts for new comments now
python cli.py refresh-tokens               renew tokens (run at least every 50 days)
python cli.py test "great video!"          see what Claude would reply, posts nothing
"""

import logging
import sys

import config

logging.basicConfig(level=logging.INFO, format="%(message)s")


def add_account(token: str) -> None:
    import instagram
    me = instagram.get_me(token)
    accounts = config.load_accounts()
    acct = config.Account(name=me["username"], ig_user_id=str(me["user_id"]), access_token=token)
    old = accounts.get(acct.ig_user_id)
    if old:
        acct.voice_notes = old.voice_notes
    accounts[acct.ig_user_id] = acct
    config.save_accounts(accounts)
    print(f"Connected @{acct.name} (id {acct.ig_user_id}).")


def subscribe() -> None:
    import instagram
    for a in config.load_accounts().values():
        print(f"@{a.name}: {instagram.subscribe_to_comment_webhooks(a.access_token)}")


def poll() -> None:
    import agent
    print(f"Handled {agent.poll_once()} new comment(s). Open the dashboard to review.")


def refresh_tokens() -> None:
    import instagram
    accounts = config.load_accounts()
    for a in accounts.values():
        a.access_token = instagram.refresh_long_lived_token(a.access_token)["access_token"]
        print(f"@{a.name}: token renewed for another 60 days.")
    config.save_accounts(accounts)


def test(text: str) -> None:
    import drafter
    d = drafter.draft_reply(comment_text=text, username="testuser", caption="", account_name="richdestyni")
    print(f"{d.action}: {d.reply}\n({d.reason})")


if __name__ == "__main__":
    cmd, args = (sys.argv[1], sys.argv[2:]) if len(sys.argv) > 1 else ("help", [])
    commands = {"add-account": add_account, "subscribe": subscribe, "poll": poll,
                "refresh-tokens": refresh_tokens, "test": test}
    if cmd not in commands:
        print(__doc__)
        sys.exit(1)
    commands[cmd](*args)
