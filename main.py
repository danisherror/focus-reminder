"""
Focus Reminder — sends a "Is it worth it?" email at scheduled intervals.
Setup: pip install apscheduler schedule
"""

import smtplib
import schedule
import time
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# ─── CONFIG ────────────────────────────────────────────────────────────────────

SENDER_EMAIL    = "your_gmail@gmail.com"       # Gmail you're sending FROM
RECEIVER_EMAIL  = "your_phone_email@gmail.com" # Gmail that notifies your phone
APP_PASSWORD    = "xxxx xxxx xxxx xxxx"        # Gmail App Password (see README)

SEND_INTERVAL_MINUTES = 60   # How often to send (e.g. 60 = every hour)

# Active hours — won't send outside this range (24h format)
ACTIVE_HOURS_START = 8   # 8 AM
ACTIVE_HOURS_END   = 22  # 10 PM

# ─── MESSAGES ──────────────────────────────────────────────────────────────────

SUBJECT = "⚡ Is it worth it?"

MESSAGES = [
    """\
Is what you're doing RIGHT NOW the most important thing for today?

✅ If YES → keep going. You're on track.
❌ If NO  → stop. Find your #1 priority and work on that instead.

Your future self is watching.""",

    """\
Quick check-in:

What are you doing right now?
Is it moving the needle on what actually matters today?

If not — close the tab, put down the phone, and get back to what counts.""",

    """\
Doomscrolling check 🔍

Rate what you're doing (1–10 for future impact).
If it's below a 7 → switch to your top priority task NOW.

You don't get this hour back.""",

    """\
Your most important task today is waiting.

Every minute spent on low-value activity is a minute stolen from the person you're trying to become.

Is it worth it?""",
]

# ─── CORE ──────────────────────────────────────────────────────────────────────

def is_active_hours() -> bool:
    hour = datetime.now().hour
    return ACTIVE_HOURS_START <= hour < ACTIVE_HOURS_END


def send_reminder():
    if not is_active_hours():
        print(f"[{datetime.now():%H:%M}] Outside active hours, skipping.")
        return

    body = random.choice(MESSAGES)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = SUBJECT
    msg["From"]    = SENDER_EMAIL
    msg["To"]      = RECEIVER_EMAIL
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        print(f"[{datetime.now():%H:%M}] ✅ Reminder sent.")
    except Exception as e:
        print(f"[{datetime.now():%H:%M}] ❌ Failed: {e}")


def main():
    print(f"Focus Reminder started. Sending every {SEND_INTERVAL_MINUTES} min "
          f"between {ACTIVE_HOURS_START}:00–{ACTIVE_HOURS_END}:00.")

    # Send one immediately on startup
    send_reminder()

    schedule.every(SEND_INTERVAL_MINUTES).minutes.do(send_reminder)

    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    main()