# eDimension Deadline Bot

Telegram bot that sends upcoming deadline reminders from your eDimension calendar, runs free on GitHub Actions.

## Features

- 14-day lookahead window
- Colour-coded urgency (🔴 ≤3 days, 🟠 ≤7 days, 🟢 ≤14 days)
- Events sorted by due date ascending
- Runs 3× daily automatically
- No server needed — powered entirely by GitHub Actions

## Prerequisites

- A GitHub account
- A Telegram account

## Setup

1. **Fork this repo**, then go to your fork's **Settings → General** and set the visibility to **Private**.

2. **Create a Telegram bot** via [@BotFather](https://t.me/BotFather), follow the prompts, and copy the bot token it gives you.

3. **Get your chat ID** — start a chat with your new bot, send it any message, then visit:
   ```
   https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
   ```
   Find `"chat"` → `"id"` in the JSON response and copy that number.

4. **Get your eDimension iCal URL** — log in to eDimension, go to **Calendar**, click the **gear icon** (top right) → **Get External Calendar Link**, and copy the `.ics` URL.

5. **Add GitHub Secrets** — in your forked repo go to **Settings → Secrets and variables → Actions → New repository secret** and add:
   - `BOT_TOKEN` — the token from BotFather
   - `CHAT_ID` — the chat ID from step 3
   - `ICAL_URL` — the `.ics` URL from step 4

6. **Test it** — go to the **Actions** tab → **Deadline Notifier** → **Run workflow**. Check your Telegram for a message.

## Schedule

The workflow runs automatically at **8:00 AM, 1:00 PM, and 8:00 PM SGT** every day (UTC 0:00, 5:00, 12:00).

## Privacy

Your eDimension iCal URL contains a personal authentication token. Keep your forked repo **private** to prevent others from accessing your calendar data.

## Contributing

PRs welcome.
