import html, os, re, urllib.request, urllib.parse
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

BOT_TOKEN  = os.environ["BOT_TOKEN"]
CHAT_ID    = os.environ["CHAT_ID"]
ICAL_URL   = os.environ["ICAL_URL"]
SGT        = ZoneInfo("Asia/Singapore")
DAYS_AHEAD = 14

def fetch_ical():
    with urllib.request.urlopen(ICAL_URL) as r:
        return r.read().decode("utf-8")

def parse_events(text):
    text = re.sub(r'\r?\n[ \t]', '', text)
    events = []
    for block in re.findall(r'BEGIN:VEVENT(.*?)END:VEVENT', text, re.DOTALL):
        def get(key):
            m = re.search(rf'^{key}(?:;[^:]+)?:(.*)', block, re.MULTILINE)
            return m.group(1).strip() if m else ""
        summary    = get("SUMMARY") \
                         .replace("\\,", ",") \
                         .replace("\\;", ";") \
                         .replace("\\\\", "\\") \
                         .replace("\\n", " ")
        dtraw      = get("DTSTART").replace("Z", "")
        categories = get("CATEGORIES")
        if not summary or not dtraw:
            continue
        try:
            due = datetime.strptime(dtraw, "%Y%m%dT%H%M%S").replace(tzinfo=SGT)
        except ValueError:
            continue
        events.append({"summary": summary, "due": due, "course": categories})
    return events

def urgency(due, now):
    days = (due - now).total_seconds() / 86400
    if days <= 3:   return 0
    elif days <= 7: return 1
    else:           return 2

TIERS = [
    ("🔴", "Urgent"),
    ("🟠", "This week"),
    ("🟢", "Coming up"),
]

def send_telegram(msg):
    data = urllib.parse.urlencode({
        "chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"
    }).encode()
    urllib.request.urlopen(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data)

def main():
    now    = datetime.now(SGT)
    cutoff = now + timedelta(days=DAYS_AHEAD)

    events   = parse_events(fetch_ical())
    upcoming = [e for e in events if now <= e["due"] <= cutoff]
    upcoming.sort(key=lambda e: e["due"])

    if not upcoming:
        return

    # Group into urgency tiers
    buckets = [[], [], []]
    for e in upcoming:
        buckets[urgency(e["due"], now)].append(e)

    lines = ["📚 <b>Upcoming Deadlines — next 14 days</b>"]
    for (icon, label), bucket in zip(TIERS, buckets):
        if not bucket:
            continue
        lines.append(f"\n{icon} <b>{label}</b>")
        for e in bucket:
            due_str = e["due"].strftime("%a %d %b, %I:%M %p")
            course  = f" ({html.escape(e['course'])})" if e["course"] else ""
            lines.append(f"• {html.escape(e['summary'])}{course}\n  {due_str}")

    send_telegram("\n".join(lines))

if __name__ == "__main__":
    main()
