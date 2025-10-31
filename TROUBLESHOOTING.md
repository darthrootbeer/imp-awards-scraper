# Troubleshooting Guide

This guide helps you diagnose and fix common issues when installing or running the IMP Awards Scraper.

## Quick Diagnosis Checklist

Run these checks to quickly identify the problem:

```bash
# 1. Check if you're in the right directory
pwd
# Should show: .../imp-awards-scraper

# 2. Check if Python is installed
python3 --version
# Should show: Python 3.8 or higher

# 3. Check if virtual environment exists
ls venv/bin/python
# Should show the file exists

# 4. Check if dependencies are installed
venv/bin/pip list | grep -E "(requests|beautifulsoup4|pillow)"
# Should list these packages

# 5. Check if .env file exists
ls .env
# Should show the file exists

# 6. Check if .env has required keys
cat .env
# Should show TMDB_API_KEY=...
```

---

## Common Issues

### "Command not found: python3"

**Problem:** Python 3 isn't installed or isn't in your PATH.

**Solution:**

1. **macOS:**
   ```bash
   # Install via Homebrew
   brew install python3
   ```

2. **Ubuntu/Debian:**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   ```

3. **Verify installation:**
   ```bash
   python3 --version
   ```

---

### "ModuleNotFoundError: No module named 'requests'"

**Problem:** Dependencies aren't installed in the virtual environment.

**Solution:**

1. **Make sure you're in the project directory:**
   ```bash
   cd /path/to/imp-awards-scraper
   ```

2. **Run the installer:**
   ```bash
   python3 scripts/install.py
   ```

3. **Or manually install:**
   ```bash
   # Activate virtual environment
   source venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt
   ```

---

### "virtualenv not found" or "venv module error"

**Problem:** The Python venv module isn't available.

**Solution:**

**macOS:**
```bash
# If using Homebrew, reinstall Python with pip
brew reinstall python3
```

**Ubuntu/Debian:**
```bash
sudo apt install python3-venv python3-pip
```

**Verify:**
```bash
python3 -m venv --help
```

---

### "TMDB_API_KEY not found" or "TMDb API errors"

**Problem:** Missing or invalid API key.

**Solution:**

1. **Check if .env exists:**
   ```bash
   ls .env
   ```

2. **If missing, run the installer:**
   ```bash
   python3 scripts/install.py
   ```
   
   Or create .env manually:
   ```bash
   echo 'TMDB_API_KEY=your_key_here' > .env
   ```

3. **Get a free API key:**
   - Visit: https://www.themoviedb.org/settings/api
   - Sign up (free)
   - Request a developer API key
   - Copy it and add to .env

4. **Verify the key works:**
   ```bash
   source venv/bin/activate
   python3 poster_downloader.py --latest --pages 1
   ```

---

### "SMTP connection failed" or email errors

**Problem:** Email credentials are missing or incorrect.

**Solution:**

1. **Check .env file has email settings:**
   ```bash
   grep SMTP .env
   # Should show: SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD
   ```

2. **For Gmail users:**
   - Don't use your regular password
   - Create an "App Password":
     1. Go to: https://myaccount.google.com/apppasswords
     2. Sign in if needed
     3. Select app: "Mail"
     4. Select device: "Other" → name it "IMP Awards"
     5. Copy the 16-character password
     6. Use that in .env

3. **Verify email settings:**
   ```bash
   source venv/bin/activate
   python3 email_sender.py
   # Should show: "✓ Email sender ready!"
   ```

4. **Update .env manually if needed:**
   ```bash
   # Edit the file
   nano .env
   
   # Add these lines (example for Gmail):
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your.email@gmail.com
   SMTP_PASSWORD=your_app_password
   EMAIL_FROM=your.email@gmail.com
   EMAIL_TO=your.email@gmail.com
   EMAIL_MAX_SIZE_MB=40
   ```

---

### "Permission denied" errors

**Problem:** Virtual environment or scripts lack execute permissions.

**Solution:**

```bash
# Fix permissions
chmod +x venv/bin/python
chmod +x venv/bin/pip
chmod +x scripts/install.py
chmod +x scripts/run_email_digest.sh

# Verify
ls -l venv/bin/python
```

---

### The script runs but downloads fail

**Problem:** Network issues or IMP Awards site changes.

**Solution:**

1. **Test internet connection:**
   ```bash
   curl http://www.impawards.com
   # Should return HTML
   ```

2. **Check if site is blocking you:**
   - Visit http://www.impawards.com in your browser
   - If blocked, wait and try again later

3. **Try a simple test download:**
   ```bash
   source venv/bin/activate
   python3 poster_downloader.py
   # Choose option 2 (single poster)
   # Enter: http://www.impawards.com/2025/tron_ares.html
   ```

4. **Check genre_config.yaml exists:**
   ```bash
   ls genre_config.yaml
   # If missing, it's optional but can cause issues
   ```

---

### "ImportError" or "No module named 'dotenv'"

**Problem:** Dependencies installed in wrong Python environment.

**Solution:**

```bash
# Deactivate any current environment
deactivate 2>/dev/null || true

# Make sure you're using the project's venv
cd /path/to/imp-awards-scraper
source venv/bin/activate

# Verify you're using the right Python
which python
# Should show: .../imp-awards-scraper/venv/bin/python

# Reinstall dependencies
pip install -r requirements.txt
```

---

### "OSError: [Errno 2] No such file or directory"

**Problem:** Scripts expect files/directories that don't exist yet.

**Solution:**

```bash
# Make sure you're in the right directory
cd /path/to/imp-awards-scraper

# Create missing directories
mkdir -p downloads
mkdir -p scripts

# Create default config files if missing
if [ ! -f genre_config.yaml ]; then
  echo "genres: {}" > genre_config.yaml
fi

if [ ! -f resolution_config.yaml ]; then
  echo "resolutions: {}" > resolution_config.yaml
fi

if [ ! -f movie_metadata.json ]; then
  echo "{}" > movie_metadata.json
fi
```

---

### Script works on one computer but not another

**Problem:** Different Python versions or missing system dependencies.

**Solution:**

1. **Check Python version:**
   ```bash
   python3 --version
   # Need 3.8+
   ```

2. **Install system dependencies:**

   **macOS:**
   ```bash
   # Install Xcode Command Line Tools
   xcode-select --install
   ```

   **Ubuntu/Debian:**
   ```bash
   sudo apt update
   sudo apt install python3-dev python3-venv libxml2-dev libxslt1-dev zlib1g-dev libjpeg-dev
   ```

3. **Reinstall everything:**
   ```bash
   # Remove old venv
   rm -rf venv
   
   # Run installer
   python3 scripts/install.py
   ```

---

### "The installer hangs or gets stuck"

**Problem:** Network issue downloading packages or incorrect input.

**Solution:**

1. **Check internet connection:**
   ```bash
   ping pypi.org
   ```

2. **Use a different mirror (if behind firewall):**
   ```bash
   # Edit scripts/install.py, find pip install lines, add:
   python3 -m pip install --index-url https://pypi.python.org/simple/ -r requirements.txt
   ```

3. **Run installer with more verbose output:**
   ```bash
   python3 scripts/install.py 2>&1 | tee install.log
   ```

4. **Check the log for errors:**
   ```bash
   tail -f install.log
   ```

---

### Email digest not running from cron

**Problem:** Cron environment is different than your shell.

**Solution:**

1. **Check if the script is executable:**
   ```bash
   chmod +x scripts/run_email_digest.sh
   ```

2. **Test the script manually:**
   ```bash
   bash scripts/run_email_digest.sh --digest-pages 1
   ```

3. **Verify cron job exists:**
   ```bash
   crontab -l
   # Should show entry for run_email_digest.sh
   ```

4. **Add full paths to cron:**
   ```bash
   crontab -e
   # Change from:
   # 0 8 * * * /path/to/scripts/run_email_digest.sh
   # To:
   # 0 8 * * * cd /full/path/to/imp-awards-scraper && bash scripts/run_email_digest.sh
   ```

5. **Check cron logs:**
   ```bash
   # macOS
   grep CRON /var/log/system.log
   
   # Linux
   grep CRON /var/log/syslog
   ```

---

## Getting More Help

If none of these solutions work:

1. **Check the error message carefully** - it usually points to the issue
2. **Run with verbose output:**
   ```bash
   source venv/bin/activate
   python3 poster_downloader.py --latest --pages 1
   ```

3. **Check system requirements:**
   ```bash
   python3 --version  # Need 3.8+
   pip3 --version
   ```

4. **Collect diagnostic info:**
   ```bash
   # Run this and save the output
   echo "Python version:"
   python3 --version
   echo "Pip list:"
   venv/bin/pip list
   echo ".env contents (hide passwords):"
   sed 's/=.*/=HIDDEN/' .env
   ```

---

## Still Stuck?

1. Check `QUICK_START.md` for basic setup
2. Check `README.md` for complete documentation
3. Review error messages carefully - they usually indicate what's wrong
4. Ensure you're in the correct directory: `/path/to/imp-awards-scraper`
5. Make sure Python 3.8+ is installed and accessible as `python3`
