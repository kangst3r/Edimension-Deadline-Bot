# eDimension Deadline Bot

A Telegram bot that sends you deadline reminders from your eDimension calendar. Runs for free on GitHub Actions, no server required.

## Features

- 14-day lookahead window
- Colour-coded urgency (🔴 3 days or less, 🟠 7 days or less, 🟢 14 days or less)
- Events sorted by due date
- Runs 3 times a day automatically
- Powered entirely by GitHub Actions, no server needed

## Prerequisites

- A GitHub account
- A Telegram account

## Setup

1. **Fork this repo**, then go to your fork's **Settings > General** and set the visibility to **Private**.

2. **Create a Telegram bot** via [@BotFather](https://t.me/BotFather), follow the prompts, and copy the bot token it gives you.

3. **Get your chat ID** by starting a chat with your new bot and sending it any message, then visiting:
   ```
   https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
   ```
   Look for `"chat"` then `"id"` in the JSON response and copy that number.

4. **Get your eDimension iCal URL** by logging into eDimension, going to **Calendar**, clicking the **gear icon** (top right), selecting **Get External Calendar Link**, and copying the `.ics` URL.

5. **Add GitHub Secrets** by going to **Settings > Secrets and variables > Actions > New repository secret** in your forked repo and adding:
   - `BOT_TOKEN`: the token from BotFather
   - `CHAT_ID`: the chat ID from step 3
   - `ICAL_URL`: the `.ics` URL from step 4

6. **Test it** by going to the **Actions** tab, clicking **Deadline Notifier**, then **Run workflow**. You should get a message on Telegram shortly after.

## After Forking

GitHub automatically disables scheduled workflows on forked repos. Once you have added your secrets, go to the Actions tab in your forked repo, select Deadline Notifier, and click Enable workflow. Then run it manually once via Run workflow to confirm everything is working before the schedule kicks in.

## Schedule

The workflow runs automatically at **8:00 AM, 1:00 PM, and 8:00 PM SGT** every day (UTC 0:00, 5:00, 12:00). Note that GitHub may delay scheduled runs by up to 3.5 hours during peak times. 

**IMPORTANT**: GitHub disables scheduled workflows on repos with no commit activity for 60 days. To keep the bot running, make any small commit to your repo at least once every 2 months (e.g. editing a line in this README). You can re-enable the workflow manually in the Actions tab if it gets disabled.

## Privacy

Your `BOT_TOKEN`, `CHAT_ID`, `ICAL_URL` are stored as a **GitHub Secrets** and are never exposed in the repository. You can keep your fork private if you don't want your workflow run logs visible to others, but it is not a security requirement.
