# Focus Reminder — Setup Guide
 
Sends a "Is it worth it?" email to your phone every hour to prevent doomscrolling.
 
---
 
## 1. Install dependencies
 
```bash
pip install schedule
```
 
---
 
## 2. Get a Gmail App Password
 
Gmail blocks plain passwords for SMTP. You need an **App Password**:
 
1. Go to your Google Account → **Security**
2. Enable **2-Step Verification** (required)
3. Search for **"App passwords"** in the search bar
4. Select app: **Mail** → device: **Other** → name it "Focus Reminder"
5. Copy the 16-character password (e.g. `abcd efgh ijkl mnop`)
---
 
## 3. Configure reminder.py
 
Open `reminder.py` and fill in:
 
```python
SENDER_EMAIL    = "your_gmail@gmail.com"
RECEIVER_EMAIL  = "your_gmail@gmail.com"   # can be same email
APP_PASSWORD    = "abcd efgh ijkl mnop"    # from step 2
SEND_INTERVAL_MINUTES = 60                 # adjust as needed
ACTIVE_HOURS_START = 8                     # 8 AM
ACTIVE_HOURS_END   = 22                    # 10 PM
```
 
> **Tip:** SENDER and RECEIVER can be the same Gmail — it'll still notify your phone.
 
---
 
## 4. Run it
 
```bash
python reminder.py
```
 
Keep the terminal open (or run it as a background service — see below).
 
---
 
## 5. Run it 24/7 (optional)
 
### On Linux/macOS — run in background:
```bash
nohup python reminder.py &
```
 
### As a system service (Linux):
Create `/etc/systemd/system/focus-reminder.service`:
```
[Unit]
Description=Focus Reminder
 
[Service]
ExecStart=/usr/bin/python3 /path/to/reminder.py
Restart=always
 
[Install]
WantedBy=multi-user.target
```
Then: `sudo systemctl enable focus-reminder && sudo systemctl start focus-reminder`
 
---
 
## Phone notification setup
 
In Gmail app on Android/iPhone:
- Go to **Settings → your account → Notifications**
- Enable notifications for "Primary" inbox
- The subject line "⚡ Is it worth it?" will appear on your lock screen
---
 
## Customise messages
 
Add your own nudges to the `MESSAGES` list in `reminder.py`. One is chosen randomly each time.
 
---
 
## Complementary habits (no code needed)
 
- **Grayscale mode** on phone — makes it boring to look at
- **App timers** — Digital Wellbeing (Android) / Screen Time (iOS)
- **Phone in another room** while working
- **Pomodoro timer** — 25 min work, 5 min break