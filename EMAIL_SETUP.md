# Email Notification Setup Guide

The IMP Awards Poster Downloader now supports automated email notifications! Get daily updates with newly downloaded posters sent directly to your inbox.

## Features

- **Daily Digest Emails**: Automatically receive newly downloaded posters
- **Smart Batching**: Splits large batches into multiple emails (40MB limit per email)
- **Clickable Thumbnails**: Email contains optimized thumbnails that link to full-size images on IMP Awards
- **Tracking System**: Never sends the same poster twice
- **Beautiful HTML Format**: Clean, professional email layout with movie metadata

## Setup Instructions

### 1. Email Credentials (Already Configured)

Your Gmail credentials are already set up in the `.env` file:
- **From/To**: echose7en@gmail.com
- **SMTP**: Gmail (smtp.gmail.com:587)
- **Max Size**: 40MB per email

### 2. Usage Examples

#### Download Latest and Email
```bash
python poster_downloader.py --latest --email-update
```

#### Download from Multiple Pages and Email
```bash
python poster_downloader.py --latest --pages 5 --email-update
```

#### Download Specific Year and Email
```bash
python poster_downloader.py --year 2025 --email-update
```

#### With Genre Filtering
```bash
python poster_downloader.py --latest --genre Animation --email-update
```

## Email Format

Each email includes:

```
Movie Title (Release Year)
Poster #X
[Clickable thumbnail - links to full-size image]
─────────────────────────
(repeats for each poster)
```

### Example Email:
```
Subject: IMP Awards Daily Update - October 14, 2025 - 12 Posters

Tron: Ares (2025)
Poster #31
[Image thumbnail - click to view 2053x3000]
─────────────────────────
Predator: Badlands (2025)
Poster #12
[Image thumbnail - click to view 1080x1350]
─────────────────────────
...
```

## Automated Daily Updates

### macOS (using launchd)

Create a daily automation that runs at 8 AM:

1. Create file: `~/Library/LaunchAgents/com.impawards.daily.plist`
```xml
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
        <string>--latest</string>
        <string>--email-update</string>
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
```

2. Load the automation:
```bash
launchctl load ~/Library/LaunchAgents/com.impawards.daily.plist
```

3. To stop:
```bash
launchctl unload ~/Library/LaunchAgents/com.impawards.daily.plist
```

### Linux (using cron)

Add to crontab:
```bash
crontab -e
```

Add line:
```
0 8 * * * cd /path/to/imp-awards-scraper && venv/bin/python3 poster_downloader.py --latest --email-update
```

## How It Works

### Duplicate Prevention
The system uses `email_tracking.json` to remember which posters have been sent:
- First run: Sends all newly downloaded posters
- Subsequent runs: Only sends posters that haven't been emailed before
- Never duplicates emails

### Smart Batching (40MB Limit)
If your download includes many large posters:
1. System calculates total email size
2. If > 40MB, splits into multiple emails
3. Each email labeled: "Daily Update (1 of 3)", "Daily Update (2 of 3)", etc.
4. Each batch stays under 40MB

### Thumbnail Generation
- Original posters can be 1-3MB each
- System creates 800px-wide thumbnails (~100-200KB each)
- Thumbnails embedded in email for quick viewing
- Click thumbnail to view full-size on IMP Awards

## Tracking File

`email_tracking.json` keeps a record:
```json
{
  "sent_posters": [
    "downloads/2025_tron_ares_ver31_XXLG_1440x2086.jpg",
    "downloads/2025_predator_badlands_ver12_XLG_1080x1350.jpg"
  ],
  "last_sent": "2025-10-14T08:00:00.000000"
}
```

To reset and resend everything:
```bash
rm email_tracking.json
```

## Troubleshooting

### No Email Received?
1. Check spam folder
2. Verify credentials in `.env` file
3. Check error messages in terminal output

### Gmail Authentication Error?
- Ensure you're using an App Password (not your regular Gmail password)
- Enable 2-factor authentication on your Google account
- Generate new App Password: https://myaccount.google.com/apppasswords

### Want to Change Email Settings?
Edit `.env` file:
```bash
EMAIL_TO=different@email.com    # Change recipient
EMAIL_MAX_SIZE_MB=25            # Smaller batch size
```

## Security Note

⚠️ **IMPORTANT**: The `.env` file contains your email password and is automatically excluded from git commits. Never share this file or commit it to GitHub.

## What's Next?

This email system is Phase 6 of the enhancement plan. Future additions could include:
- HTML email templates with richer formatting
- Genre breakdown statistics in email
- Direct links to IMDb/TMDb pages
- Webhook support for Slack/Discord notifications

