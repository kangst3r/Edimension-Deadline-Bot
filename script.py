import os
import re
import urllib.request
import urllib.parse
import json
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

ICAL_URL = os.environ["ICAL_URL"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

SGT = ZoneInfo("Asia/Singapore")


def fetch_ical(url):
    with urllib.request.urlopen(url) as resp:
        return resp.read().decode("utf-8", errors="replace")


def unfold(text):
    # Join lines that are continued with a leading space or tab
    return re.sub(r"\r?\n[ \t]", "", text)


def parse_events(text):
    text = unfold(text)
    events = []
    for block in re.findall(r"BEGIN:VEVENT(.*?)END:VEVENT", text, re.DOTALL):
        summary_m = re.search(r"^SUMMARY[^:]*:(.*)", block, re.MULTILINE)
        dtstart_m = re.search(r"^(DTSTART[^:]*:(.*))", block, re.MULTILINE)
        if not summary_m or not dtstart_m:
            continue
        summary = summary_m.group(1).strip()
        raw_dtstart = dtstart_m.group(1).strip()
        dt = parse_dtstart(raw_dtstart)
        if dt is None:
            continue
        events.append({"summary": summary, "dtstart": dt})
    return events


def parse_dtstart(raw):
    # Matches both:
    #   DTSTART;TZID=Asia/Singapore:20260410T090000
    #   DTSTART:20260410T090000Z
    m = re.match(r"DTSTART(?:;TZID=([^:]+))?:(\d{8}T\d{6})(Z?)", raw)
    if not m:
        return None
    tzid, dt_str, zulu = m.group(1), m.group(2), m.group(3)
    naive = datetime.strptime(dt_str, "%Y%m%dT%H%M%S")
    if zulu == "Z":
        dt = naive.replace(tzinfo=timezone.utc).astimezone(SGT)
    elif tzid:
        dt = naive.replace(tzinfo=ZoneInfo(tzid)).astimezone(SGT)
    else:
        dt = naive.replace(tzinfo=SGT)
    return dt


def urgency_emoji(days_remaining):
    if days_remaining <= 3:
        return "🔴"
    if days_remaining <= 7:
        return "🟠"
    return "🟢"


def format_event(event, now_sgt):
    dt = event["dtstart"]
    days_remaining = (dt.date() - now_sgt.date()).days
    emoji = urgency_emoji(days_remaining)
    due_str = dt.strftime("%a %-d %b, %I:%M %p").replace(" 0", " ")
    return f"{emoji} {event['summary']}\n  ⏰ {due_str}"


def send_telegram(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = json.dumps({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
    }).encode()
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        resp.read()


def main():
    now_sgt = datetime.now(tz=SGT)
    window_end = now_sgt + timedelta(days=14)

    raw = fetch_ical(ICAL_URL)
    events = parse_events(raw)

    upcoming = [
        e for e in events
        if now_sgt <= e["dtstart"] <= window_end
    ]

    if not upcoming:
        return

    upcoming.sort(key=lambda e: e["dtstart"])

    lines = ["📚 *Upcoming Deadlines — next 14 days*", ""]
    for event in upcoming:
        lines.append(format_event(event, now_sgt))
    lines.append("")
    lines.append("🔴 ≤3 days  🟠 ≤7 days  🟢 ≤14 days")

    send_telegram(BOT_TOKEN, CHAT_ID, "\n".join(lines))


if __name__ == "__main__":
    main()
