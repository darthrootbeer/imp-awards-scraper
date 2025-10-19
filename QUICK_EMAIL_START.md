# Quick Start: Email Notifications

Your automated email notification system is **ready to use right now!**

## Instant Test

Try it immediately:

```bash
cd /Users/bengoddard/projects/imp-awards-scraper
venv/bin/python3 poster_downloader.py --email-digest --digest-pages 5
```

This will:
1. Scan the latest IMP Awards pages (up to 5 deep) until it reaches the last digest
2. Email you only the new posters that haven't been included before
3. Send to: echose7en@gmail.com

**Check your email!** 📧

---

## Daily Automation (Recommended)

### Option 1: Simple Daily Script

Create a daily run script:

```bash
cd /Users/bengoddard/projects/imp-awards-scraper
cat > daily_update.sh << 'EOF'
#!/bin/bash
cd /Users/bengoddard/projects/imp-awards-scraper
venv/bin/python3 poster_downloader.py --email-digest --digest-pages 5
EOF
chmod +x daily_update.sh
```

Run it anytime: `./daily_update.sh`

### Option 2: Automatic Daily at 8 AM (macOS)

```bash
# Create the automation file
cat > ~/Library/LaunchAgents/com.impawards.daily.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.impawards.daily</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/bengoddard/projects/imp-awards-scraper/venv/bin/python3</string>
        <string>/Users/bengoddard/projects/imp-awards-scraper/poster_downloader.py</string>
        <string>--email-digest</string>
        <string>--digest-pages</string>
        <string>5</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>8</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/Users/bengoddard/projects/imp-awards-scraper/daily_update.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/bengoddard/projects/imp-awards-scraper/daily_update_error.log</string>
</dict>
</plist>
EOF

# Activate it
launchctl load ~/Library/LaunchAgents/com.impawards.daily.plist

# Verify it's loaded
launchctl list | grep impawards
```

**Done!** You'll get an email every morning at 8 AM with yesterday's new posters.

---

## Email Features

### What You'll Receive

```
Subject: IMP Awards Daily Update - October 14, 2025 - 12 Posters

[Beautiful HTML email with:]

Tron: Ares (2025)
Poster #31
[Clickable thumbnail image]
─────────────────────────

Predator: Badlands (2025)
Poster #12
[Clickable thumbnail image]
─────────────────────────

(etc...)
```

### Clickable Thumbnails
- Click any thumbnail → Opens full-size image on IMP Awards
- Optimized size (~150-200KB each)
- Links directly to source

### Smart Batching
If you download 100+ posters in one run:
- Automatically splits into multiple emails
- Each email < 40MB
- Numbered: "Daily Update (1 of 3)", "Daily Update (2 of 3)", etc.

### Never Duplicates
- `digest_state.json` remembers which poster URLs were already included so the crawler stops exactly where the last digest ended.
- `email_tracking.json` remembers which downloaded files were emailed, preventing duplicate attachments.
- Run the command daily—only brand-new posters are sent each time.

---

## Common Commands

```bash
# Email digest (scan 5 pages or until the last digest)
python poster_downloader.py --email-digest

# Go deeper (scan 10 pages before emailing)
python poster_downloader.py --email-digest --digest-pages 10

# Only send Animation + Family posters
python poster_downloader.py --email-digest --genre Animation --genre Family

# Prefix subject with [TEST]
python poster_downloader.py --email-digest --digest-test
```

---

## Troubleshooting

### "No new posters to email"
✅ This is normal! It means everything has already been emailed.

### Want to resend emails?
Delete the tracking files:
```bash
rm digest_state.json email_tracking.json
```
Next run will email everything again.

### Not receiving emails?
1. Check spam folder
2. Verify your Gmail allows "less secure apps" or has app password enabled
3. Check terminal output for errors

### Stop daily automation
```bash
launchctl unload ~/Library/LaunchAgents/com.impawards.daily.plist
```

---

## Advanced Usage

### Different Time (e.g., 6 PM instead of 8 AM)
Edit the plist file:
```xml
<key>Hour</key>
<integer>18</integer>  <!-- 6 PM -->
```
Then reload:
```bash
launchctl unload ~/Library/LaunchAgents/com.impawards.daily.plist
launchctl load ~/Library/LaunchAgents/com.impawards.daily.plist
```

### Multiple Times Per Day
Create separate plist files with different times.

### Check Logs
```bash
# See what happened
cat /Users/bengoddard/projects/imp-awards-scraper/daily_update.log

# See errors
cat /Users/bengoddard/projects/imp-awards-scraper/daily_update_error.log
```

---

## That's It!

You're all set. The system is working and ready to use.

**Your first email should arrive within seconds of running the command.**

For detailed documentation, see:
- `EMAIL_SETUP.md` - Complete guide
- `IMPLEMENTATION_SUMMARY.md` - Technical details
- `README.md` - Full project documentation

Enjoy your automated poster collection! 🎬🖼️
