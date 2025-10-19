#!/bin/bash
set -euo pipefail

# Resolve project root relative to this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR/.."

cd "$PROJECT_ROOT"

# Default to scanning 5 pages unless overridden
PAGES="${PAGES_OVERRIDE:-5}"

if [[ -d "venv" ]]; then
    PYTHON_BIN="$PROJECT_ROOT/venv/bin/python"
else
    PYTHON_BIN="$(which python3)"
fi

if [[ -z "$PYTHON_BIN" ]]; then
    echo "python3 not found. Please install Python 3.8+."
    exit 1
fi

"$PYTHON_BIN" poster_downloader.py --email-digest --digest-pages "$PAGES" "$@"
