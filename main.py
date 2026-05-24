"""
Focus Reminder — sends one "Is it worth it?" email per GitHub Actions trigger.
Setup: pip install python-dotenv
"""

import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# ─── CONFIG ────────────────────────────────────────────────────────────────────

SENDER_EMAIL       = os.getenv("SENDER_EMAIL")
RECEIVER_EMAIL     = os.getenv("RECEIVER_EMAIL")
APP_PASSWORD       = os.getenv("APP_PASSWORD")
ACTIVE_HOURS_START = int(os.getenv("ACTIVE_HOURS_START", 8))
ACTIVE_HOURS_END   = int(os.getenv("ACTIVE_HOURS_END", 22))

# ─── VALIDATION ────────────────────────────────────────────────────────────────

missing = [k for k, v in {
    "SENDER_EMAIL": SENDER_EMAIL,
    "RECEIVER_EMAIL": RECEIVER_EMAIL,
    "APP_PASSWORD": APP_PASSWORD,
}.items() if not v]

if missing:
    raise EnvironmentError(
        f"Missing required environment variables: {', '.join(missing)}\n"
        "Add them in GitHub repo → Settings → Secrets and variables → Actions."
    )

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
    hour = datetime.utcnow().hour + 5  # UTC → IST (UTC+5:30, simplified)
    hour = hour % 24
    return ACTIVE_HOURS_START <= hour < ACTIVE_HOURS_END


def send_reminder():
    if not is_active_hours():
        print(f"[{datetime.utcnow():%H:%M} UTC] Outside active hours, skipping.")
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
        print(f"[{datetime.utcnow():%H:%M} UTC] ✅ Reminder sent.")
    except Exception as e:
        print(f"[{datetime.utcnow():%H:%M} UTC] ❌ Failed: {e}")


if __name__ == "__main__":
    send_reminder()