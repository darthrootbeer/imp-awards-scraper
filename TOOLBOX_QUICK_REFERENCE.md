# TOOLBOX Quick Reference Guide

Quick reference for using TOOLBOX utilities in your projects.

## Importing Utilities

```python
import sys
sys.path.append('../../TOOLBOX/python')  # Adjust path as needed
from pushover import send_pushover, format_message, format_timestamp
from emailer import send_email, send_styled_email, format_timestamp
```

## Pushover Notifications

### Basic Usage
```python
send_pushover("Message", "Title")
```

### Best Practice Format
```python
summary = "Task completed: Database backup finished"  # <= 140 chars
details = "Detailed information here..."
message = format_message(summary, details)
send_pushover(message, "Notification")
```

### HTML Formatting
```python
summary = "✨ <b>Status</b> ✨"
details = "<b>CPU:</b> <font color=\"#3b82f6\">42%</font>"
message = format_message(summary, details, use_html=True)
send_pushover(message, "Update", html=True)
```

### With Timestamp
```python
timestamp = format_timestamp()  # "Sat 2025-12-13 • 5:17p"
send_pushover(f"Task completed at {timestamp}", "Status")
```

## Email Notifications

### Basic HTML Email (Auto-Styled)
```python
send_email("Subject", "<p>Body content</p>", html=True)
# Automatically includes icon, styled template, project identifier
```

### Styled Email with Custom Colors
```python
send_styled_email(
    "Alert",
    "<p>High CPU usage detected</p>",
    header_color="#ef4444",  # Red for alerts
    body_style="font-size: 16px; color: #1f2937;"
)
```

### With Timestamp
```python
timestamp = format_timestamp()
send_email("Report", f"<p>Last updated: {timestamp}</p>", html=True)
```

## Project Identification

Automatically detected from:
1. `TOOLBOX_PROJECT_NAME` environment variable
2. Current working directory (if under `~/projects`)
3. Defaults to `vader/TOOLBOX`

Format: `vader/{project-name}`

## Message Formatting Best Practices

### Pushover
- **First 140 characters**: Visible in pop-up notification
- **2 blank lines**: Separator (use `\n\n` or `<br><br>`)
- **Details**: Visible when notification is expanded

### Email
- Use `html=True` for automatic styled templates
- Include icon and project identifier automatically
- Responsive design works across email clients

## Timestamp Format

Standard format: `"Sat 2025-12-13 • 5:17p"` (Eastern time)

```python
from pushover import format_timestamp
from emailer import format_timestamp

timestamp = format_timestamp()  # Current time
timestamp = format_timestamp(datetime_obj)  # Specific time
```

## Configuration

### Environment Variables (.env)
- `TOOLBOX_PUSHOVER_APP_TOKEN` - Pushover app token
- `TOOLBOX_PUSHOVER_USER_TOKEN` - Pushover user token
- `TOOLBOX_GMAIL_USER` - Gmail address
- `TOOLBOX_GMAIL_APP_PASSWORD` - Gmail app password
- `TOOLBOX_PROJECT_NAME` - Override project name detection

### Config Files
- `config/pushover.yaml` - Pushover default settings
- `config/.cursorrules` - Centralized cursor rules
- `config/cursor_operator_instructions.md` - Operator instructions

## Bash Scripts

```bash
# Pushover notification
~/projects/TOOLBOX/scripts/pushover.sh "Message" "Title"

# With options
~/projects/TOOLBOX/scripts/pushover.sh "Message" "Title" --priority 1 --sound bugle --html
```

## Common Patterns

### Success Notification
```python
send_pushover("✅ Task completed successfully", "Status", priority=0, sound="none")
```

### Error Notification
```python
send_pushover("❌ Error: Connection failed", "Alert", priority=1, sound="siren")
```

### Status Report Email
```python
body = """<h2>System Status Report</h2>
<p>All systems operational.</p>
<p>Last check: {}</p>""".format(format_timestamp())
send_email("Status Report", body, html=True)
```

## Verification

Run setup verification:
```bash
~/projects/TOOLBOX/scripts/verify_toolbox_setup.sh
```

## Examples

See `examples/notification_examples.py` for complete working examples.

## Full Documentation

See `README.md` for complete documentation.

