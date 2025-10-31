#!/bin/bash
echo "=== Basic Checks ==="
echo "Current directory:"
pwd
echo ""
echo "Git status:"
git status 2>&1 | head -5
echo ""
echo "Is venv accessible:"
ls -la venv/bin/python 2>&1 | head -3
echo ""
echo "Cron jobs:"
crontab -l 2>&1 | grep -i imp || echo "No IMP Awards cron job found"
echo ""
echo "=== Test run ==="
echo "Testing if the script works:"
venv/bin/python poster_downloader.py --help 2>&1 | head -10
echo ""
echo "=== Most Common Issue ==="
echo "If cron shows up above but script fails, it's likely a PATH issue."
echo "Try running the manual test:"
echo "  bash scripts/run_email_digest.sh --digest-pages 1"
