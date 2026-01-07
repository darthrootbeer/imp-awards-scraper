#!/usr/bin/env python3
"""
Example templates for using TOOLBOX notification utilities.

These examples demonstrate best practices for sending notifications.
"""

import sys
import os

# Add TOOLBOX to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python'))

from pushover import send_pushover, format_message, format_timestamp
from emailer import send_email, send_styled_email, format_timestamp as email_timestamp


# Example 1: Simple Pushover notification
def example_simple_pushover():
    """Basic notification with project identifier."""
    send_pushover("Task completed successfully", "Status Update")


# Example 2: Pushover with formatted message (best practice)
def example_formatted_pushover():
    """Notification with summary and details."""
    summary = "Task completed: Database backup finished in 45 seconds"
    details = """Detailed Summary:
- Database: production_db
- Backup size: 2.4 GB
- Destination: /backups/prod_db_backup.sql
- Status: SUCCESS"""
    
    message = format_message(summary, details)
    send_pushover(message, "System Notification")


# Example 3: Pushover with HTML formatting
def example_html_pushover():
    """HTML formatted notification with colors and styling."""
    summary = "✨ <b>System Status Update</b> ✨"
    details = """<b>Status:</b> <font color="#22c55e">🟢 All Systems Operational</font><br><br>
<u>Details:</u><br>
• <b>CPU:</b> <font color="#3b82f6">42%</font> (Normal)<br>
• <b>Memory:</b> <font color="#3b82f6">68%</font> (Normal)<br>
• <b>Disk:</b> <font color="#f59e0b">78%</font> (Warning)"""
    
    message = format_message(summary, details, use_html=True)
    send_pushover(message, "System Update", html=True)


# Example 4: Pushover with timestamp
def example_pushover_with_timestamp():
    """Notification including formatted timestamp."""
    timestamp = format_timestamp()
    summary = f"Task completed at {timestamp}"
    details = "All systems are operating normally."
    
    message = format_message(summary, details)
    send_pushover(message, "Status Update")


# Example 5: Simple email
def example_simple_email():
    """Basic HTML email (automatically uses styled template)."""
    send_email("Task Report", "<p>Task completed successfully.</p>", html=True)


# Example 6: Email with formatted content
def example_formatted_email():
    """Email with structured content."""
    from emailer import format_message as email_format_message
    
    summary = "Task Completed Successfully"
    details = """<p>Your automated task has been completed. Here are the details:</p>
<table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin: 20px 0; border-collapse: collapse;">
    <tr>
        <td style="padding: 12px; background-color: #f9fafb; border: 1px solid #e5e7eb; font-weight: 600; color: #374151;">Status</td>
        <td style="padding: 12px; background-color: #ffffff; border: 1px solid #e5e7eb; color: #10b981;">✓ Success</td>
    </tr>
    <tr>
        <td style="padding: 12px; background-color: #f9fafb; border: 1px solid #e5e7eb; font-weight: 600; color: #374151;">Duration</td>
        <td style="padding: 12px; background-color: #ffffff; border: 1px solid #e5e7eb;">45 seconds</td>
    </tr>
</table>
<p style="margin-bottom: 0;">All systems are operating normally.</p>"""
    
    body = email_format_message(summary, details)
    send_email("Task Report", body, html=True)


# Example 7: Styled email with custom colors
def example_styled_email():
    """Email with custom header color for alerts."""
    body = """<p>High CPU usage detected on server.</p>
<ul>
    <li>CPU Usage: 95.3%</li>
    <li>Memory Usage: 78%</li>
    <li>Action Required: Review process activity</li>
</ul>"""
    
    send_styled_email(
        "System Alert",
        body,
        header_color="#ef4444",  # Red for alerts
        body_style="font-size: 16px; color: #1f2937; line-height: 1.6;"
    )


# Example 8: Email with timestamp
def example_email_with_timestamp():
    """Email including formatted timestamp."""
    timestamp = email_timestamp()
    body = f"""<p>Last system check completed at <strong>{timestamp}</strong>.</p>
<p>All systems are operating normally.</p>"""
    
    send_email("System Status", body, html=True)


# Example 9: Error notification with full details
def example_error_notification():
    """Error notification with detailed information."""
    timestamp = format_timestamp()
    summary = f"Error: Connection timeout after 30s ({timestamp})"
    details = """Error Details:
- Service: API endpoint
- Endpoint: api.example.com
- Retry count: 3/3
- Last error: ETIMEDOUT
- Action: Manual intervention required"""
    
    message = format_message(summary, details)
    send_pushover(message, "System Alert", priority=1, sound="siren")


# Example 10: Success notification with HTML
def example_success_html():
    """Success notification with HTML formatting."""
    summary = "✅ <b>Deployment Successful</b>"
    details = """<b>Version:</b> v2.1.0<br>
<b>Environment:</b> <font color="#22c55e">Production</font><br>
<b>Status:</b> <font color="#22c55e">🟢 Live</font><br><br>
All services are operational."""
    
    message = format_message(summary, details, use_html=True)
    send_pushover(message, "Deployment", html=True, priority=0, sound="none")


if __name__ == "__main__":
    print("TOOLBOX Notification Examples")
    print("=" * 50)
    print("\nThese are example functions demonstrating best practices.")
    print("Uncomment the function you want to test and run this script.")
    print("\nAvailable examples:")
    print("  1. example_simple_pushover()")
    print("  2. example_formatted_pushover()")
    print("  3. example_html_pushover()")
    print("  4. example_pushover_with_timestamp()")
    print("  5. example_simple_email()")
    print("  6. example_formatted_email()")
    print("  7. example_styled_email()")
    print("  8. example_email_with_timestamp()")
    print("  9. example_error_notification()")
    print("  10. example_success_html()")
    print("\nNote: Make sure TOOLBOX/.env is configured with credentials.")

