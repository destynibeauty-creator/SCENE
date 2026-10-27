# Comment Desk - AI replies for @richdestyni + @profashionalist

Claude reads every new Instagram comment and writes a reply in Destyni's
voice. You approve it with one tap, or turn on auto-post for the easy ones.

```
New comment on Instagram
   -> Meta sends it to this app (webhook)
   -> Claude decides: reply / skip (spam) / flag for you
   -> reply waits in your dashboard   (or posts itself if AUTO_POST=true)
   -> you tap "Post reply"            -> it shows up under the comment
```

**Safety built in**
- Auto-post is **off** to start. Nothing posts until you tap it.
- Even with auto-post on, complaints, health questions, money/order issues,
  business offers, and anything unclear are **always** held for you.
- Spam and bots are skipped. It never replies to your own comments.
- Replies are spaced out (45 seconds by default) so it never looks like a bot.
- The **Facebook reply helper** box on the dashboard drafts replies for your
  Facebook profile. Facebook doesn't let apps post there, so you copy the
  reply and post it yourself.

**Your voice lives in [`voice.md`](voice.md).** Edit it any time (what you
say, what you never say, emoji you like). Changes work right away.

---

## Setup (about 30-45 minutes, one time)

### 1. Check both Instagram accounts are professional
Instagram app -> Settings -> **Account type and tools**. Each one must be a
**Creator** or **Business** account. Personal accounts can't use the API.

### 2. Get a Claude API key
[console.anthropic.com](https://console.anthropic.com) -> API Keys -> Create key.
Add a few dollars of credit. Each comment costs about 1 cent with the
default model (Claude Opus 5.5), so 1,000 comments is about $10. To spend
about half that, add `CLAUDE_MODEL=claude-sonnet-5-5` to your `.env`.

### 3. Create the Meta app
1. Go to [developers.facebook.com](https://developers.facebook.com) -> **My Apps** -> **Create app**.
2. Pick the use case **"Manage messaging & content on Instagram."**
3. Open **API setup with Instagram login**.
4. Under **Generate access tokens**, click **Add account** and log in as
   **@richdestyni**. Copy the token it shows you. Do the same for
   **@profashionalist**. Save both tokens somewhere private.
5. Copy the **Instagram app secret** from the same page.

### 4. Put the app online
It needs a public `https://` address so Instagram can reach it.
[Render](https://render.com) or [Railway](https://railway.app) both work
(about $7/month):
- Connect this GitHub repo and set the root folder to `comment-agent`
- Build command: `pip install -r requirements.txt`
- Start command: `python app.py`
- Add a **disk** (persistent storage) so `comments.db` and `accounts.json`
  survive restarts.
- Add the settings from [`.env.example`](.env.example) as environment variables.

### 5. Connect your accounts
In the host's shell (or on your computer, in this folder):

```bash
python cli.py add-account <TOKEN_FOR_RICHDESTYNI>
python cli.py add-account <TOKEN_FOR_PROFASHIONALIST>
python cli.py test "how did you make this video??"   # dry run, posts nothing
```

To give an account its own style, open `accounts.json` and edit
`voice_notes` (example: `"Fashion account. Talk outfits and style."`).

### 6. Turn on comment webhooks
1. Meta app -> **API setup with Instagram login** -> **Configure webhooks**.
2. Callback URL: `https://YOUR-APP-ADDRESS/webhook`
3. Verify token: the same phrase you put in `WEBHOOK_VERIFY_TOKEN`.
4. Click **Verify and save**, then subscribe to the **comments** field.
5. Run `python cli.py subscribe`.

Now open `https://YOUR-APP-ADDRESS/` (any username, your
`DASHBOARD_PASSWORD`) and leave a test comment on one of your posts from
another account.

> **No webhooks yet?** Meta can hold back webhooks until the app is
> switched to **Live** mode. That needs a privacy policy link, and Meta may
> ask for App Review. While you wait, `python cli.py poll` checks your 5
> newest posts for new comments. You can run it on a schedule (every 15
> minutes) as a cron job on your host.

### 7. Keep tokens fresh
Instagram tokens last 60 days. Schedule this to run once a month:

```bash
python cli.py refresh-tokens
```

---

## Day to day
- Open the dashboard on your phone. **Waiting on you** shows drafts. Edit
  if you want, then tap **Post reply** or **Skip**.
- Once the drafts sound like you, set `AUTO_POST=true` and restart. After
  that you only see the flagged ones.
- Not sounding right? Add a rule to `voice.md`, like "never say 'babe'" or
  "for lash questions, point them to Rich Lash."

## Files
| File | What it does |
|---|---|
| `voice.md` | Your voice and rules. Edit freely. |
| `app.py` | Webhook receiver + dashboard |
| `agent.py` | New comment -> draft -> queue or post |
| `drafter.py` | The Claude call that writes each reply |
| `instagram.py` | Instagram API calls |
| `cli.py` | Setup commands |
| `tests/` | `python -m pytest tests` (no keys needed) |

Run only **one** copy of `app.py`. The background worker that posts
replies lives inside it.
