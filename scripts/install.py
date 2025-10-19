#!/usr/bin/env python3
"""
Repository installer for IMP Awards Scraper.

Sets up a Python virtual environment, installs dependencies,
collects required credentials, creates supporting configuration files,
and optionally schedules the daily email digest.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from getpass import getpass
from pathlib import Path
from textwrap import dedent
from typing import Dict, Optional

from dotenv import dotenv_values


PROJECT_ROOT = Path(__file__).resolve().parent.parent
VENV_DIR = PROJECT_ROOT / "venv"
ENV_FILE = PROJECT_ROOT / ".env"
MOVIE_METADATA_FILE = PROJECT_ROOT / "movie_metadata.json"
DIGEST_SCRIPT = PROJECT_ROOT / "scripts" / "run_email_digest.sh"


def run_command(cmd: list[str], *, check: bool = True, capture_output: bool = False, text: bool = True) -> subprocess.CompletedProcess:
    """Run a subprocess command with consistent defaults."""
    return subprocess.run(cmd, check=check, capture_output=capture_output, text=text)


def create_venv() -> Path:
    """Create the virtual environment if it does not already exist."""
    if VENV_DIR.exists():
        print(f"[✓] Virtual environment already exists at {VENV_DIR}")
    else:
        print(f"[1/5] Creating a private Python environment...")
        run_command([sys.executable, "-m", "venv", str(VENV_DIR)])
        print("    Done.")
    return VENV_DIR


def get_venv_executable(name: str) -> Path:
    """Return full path to an executable inside the venv."""
    if os.name == "nt":
        path = VENV_DIR / "Scripts" / f"{name}.exe"
    else:
        path = VENV_DIR / "bin" / name
    return path


def install_requirements() -> None:
    """Install Python dependencies into the virtual environment."""
    python_path = get_venv_executable("python")
    # Ensure pip exists
    run_command([str(python_path), "-m", "ensurepip", "--upgrade"], check=False)
    print("[2/5] Installing the software (this may take a minute)...")
    run_command([str(python_path), "-m", "pip", "install", "--upgrade", "pip"])
    run_command([str(python_path), "-m", "pip", "install", "-r", str(PROJECT_ROOT / "requirements.txt")])
    print("    Done.")


def prompt_env_values() -> Dict[str, str]:
    """Collect credentials and configuration values from the user."""
    existing_env = dotenv_values(str(ENV_FILE)) if ENV_FILE.exists() else {}
    print("\n[3/5] Let's collect the information we need.")
    print("We'll guide you through each question. Press Enter to accept the default.")

    def prompt(message: str, *, default: Optional[str] = None, secret: bool = False, required: bool = False) -> str:
        while True:
            suffix = f" [{default}]" if default else ""
            raw = getpass(f"{message}{suffix}: ") if secret else input(f"{message}{suffix}: ")
            if raw:
                return raw.strip()
            if default is not None:
                return default
            if not required:
                return ""
            print("  This value is required.")

    print("\n--- TMDb (Movie Database) ---")
    print("We use TMDb to look up genres. Create a free key at https://www.themoviedb.org/settings/api.")
    tmdb_key = prompt("1) TMDb API key", default=existing_env.get("TMDB_API_KEY"), required=True)

    print("\n--- Email details ---")
    print("Use an email account that allows SMTP (Gmail users: create an app password).")
    smtp_server = prompt("2) SMTP server", default=existing_env.get("SMTP_SERVER", "smtp.gmail.com"))
    smtp_port = prompt("3) SMTP port", default=existing_env.get("SMTP_PORT", "587"))
    smtp_username = prompt("4) SMTP username", default=existing_env.get("SMTP_USERNAME"), required=True)
    smtp_password = prompt("5) SMTP password (input hidden)", default=existing_env.get("SMTP_PASSWORD"), secret=True, required=True)
    email_from = prompt("6) Email FROM address", default=existing_env.get("EMAIL_FROM", smtp_username), required=True)
    email_to = prompt("7) Daily digest TO address", default=existing_env.get("EMAIL_TO", email_from), required=True)
    max_size_mb = prompt("8) Max email size in MB", default=existing_env.get("EMAIL_MAX_SIZE_MB", "40"))

    values = {
        "TMDB_API_KEY": tmdb_key,
        "SMTP_SERVER": smtp_server,
        "SMTP_PORT": smtp_port,
        "SMTP_USERNAME": smtp_username,
        "SMTP_PASSWORD": smtp_password,
        "EMAIL_FROM": email_from,
        "EMAIL_TO": email_to,
        "EMAIL_MAX_SIZE_MB": max_size_mb,
    }
    return values


def write_env_file(values: Dict[str, str]) -> None:
    """Write collected values to .env, backing up an existing file if necessary."""
    if ENV_FILE.exists():
        backup = ENV_FILE.with_suffix(".backup")
        shutil.copy2(ENV_FILE, backup)
        print(f"Existing .env backed up to {backup}")

    with open(ENV_FILE, "w", encoding="utf-8") as fh:
        for key, value in values.items():
            fh.write(f"{key}={value}\n")
    print(f"[✓] Saved settings to {ENV_FILE}")


def ensure_metadata_store() -> None:
    """Create an empty movie metadata store if one does not exist."""
    if MOVIE_METADATA_FILE.exists():
        print(f"[✓] Movie metadata store already exists at {MOVIE_METADATA_FILE}")
        return
    with open(MOVIE_METADATA_FILE, "w", encoding="utf-8") as fh:
        json.dump({}, fh, indent=2)
    print(f"[✓] Created movie metadata store at {MOVIE_METADATA_FILE}")


def create_digest_runner() -> Path:
    """Create a helper shell script that executes the daily email digest."""
    DIGEST_SCRIPT.parent.mkdir(parents=True, exist_ok=True)
    script_contents = dedent(
        """\
        #!/bin/bash
        set -euo pipefail

        SCRIPT_DIR="$(cd "$(dirname \"${BASH_SOURCE[0]}\")" && pwd)"
        PROJECT_ROOT="$SCRIPT_DIR/.."

        cd "$PROJECT_ROOT"

        PAGES="${PAGES_OVERRIDE:-5}"

        if [[ -x "$PROJECT_ROOT/venv/bin/python" ]]; then
            PYTHON_BIN="$PROJECT_ROOT/venv/bin/python"
        else
            PYTHON_BIN="$(command -v python3)"
        fi

        if [[ -z "$PYTHON_BIN" ]]; then
            echo "python3 not found. Please install Python 3.8+."
            exit 1
        fi

        "$PYTHON_BIN" poster_downloader.py --email-digest --digest-pages "$PAGES" "$@"
        """
    )
    with open(DIGEST_SCRIPT, "w", encoding="utf-8") as fh:
        fh.write(script_contents)
    os.chmod(DIGEST_SCRIPT, 0o755)
    print(f"✓ Created digest runner script at {DIGEST_SCRIPT}")
    return DIGEST_SCRIPT


def schedule_digest(cron_command: str) -> None:
    """Append the digest job to the user's crontab (Unix-like systems only)."""
    if shutil.which("crontab") is None:
        print("⚠️  'crontab' not found on this system. Please schedule the digest manually.")
        print(f"    Suggested command: {cron_command}")
        return

    try:
        current = run_command(["crontab", "-l"], check=False, capture_output=True)
        existing = current.stdout if current.returncode == 0 else ""
    except Exception:
        existing = ""

    if cron_command in existing:
        print("✓ Cron entry already present; skipping update.")
        return

    new_crontab = (existing.rstrip("\n") + "\n" + cron_command + "\n").lstrip("\n")
    subprocess.run(["crontab", "-"], input=new_crontab, text=True, check=True)
    print("[✓] Daily digest scheduled.")


def configure_schedule(digest_script: Path) -> None:
    """Interactively configure the daily email digest schedule."""
    print("\n[4/5] Would you like us to set up the daily email digest for you?")
    print("  1) Yes, schedule it automatically")
    print("  2) No, I'll handle it later")
    choice = input("Select an option (1-2): ").strip()
    if choice != "1":
        print("Skipping scheduler configuration. You can add it later by rerunning this installer.")
        print(f"Manual command: {digest_script} --digest-pages 5")
        return

    time_str = input("Enter the daily run time (HH:MM in 24-hour format, default 08:00): ").strip() or "08:00"
    pages = input("How many recent pages should we scan? (default 5): ").strip() or "5"
    print("Should the digest be sent in TEST mode (adds [TEST] to the subject)?")
    print("  1) Yes, send as test")
    print("  2) No, send as normal")
    test_choice = input("Select an option (1-2): ").strip()

    try:
        hour, minute = time_str.split(":")
        hour = str(int(hour))
        minute = str(int(minute))
    except Exception:
        print("⚠️  Invalid time format. Expected HH:MM. We'll skip scheduling for now.")
        return

    extra_flags = f"--digest-pages {pages}"
    if test_choice == "1":
        extra_flags += " --digest-test"

    cron_line = f"{minute} {hour} * * * {digest_script} {extra_flags}".strip()
    schedule_digest(cron_line)


def print_summary() -> None:
    """Display next steps for the user."""
    python_path = get_venv_executable("python")
    summary = dedent(
        f"""
        [5/5] ✅ All set!

        What you can do next:
          1. Activate the environment when working manually:
               • macOS/Linux:  source {VENV_DIR}/bin/activate
               • Windows:      {VENV_DIR}\\Scripts\\activate.bat
          2. Run a quick test download:
               {python_path} poster_downloader.py --latest --pages 1
          3. Send a digest immediately (optional):
               {DIGEST_SCRIPT} --digest-pages 5

        Need to change settings later? Just run:
               python3 scripts/install.py
        """
    ).strip()
    print("\n" + summary + "\n")


def main() -> None:
    print("=" * 60)
    print("IMP Awards Scraper - Installer")
    print("=" * 60)
    print("Tip: If you're using an AI helper, share AI_INSTRUCTIONS.md with it so the assistant can drive this setup for you.")

    if sys.version_info < (3, 8):
        print("⚠️  Python 3.8 or newer is required. Please upgrade Python and re-run the installer.")
        return

    create_venv()
    install_requirements()
    env_values = prompt_env_values()
    write_env_file(env_values)
    ensure_metadata_store()
    digest_runner = create_digest_runner()
    configure_schedule(digest_runner)
    print_summary()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInstallation cancelled by user.")
