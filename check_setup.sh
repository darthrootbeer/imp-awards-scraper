#!/bin/bash
echo "=========================================="
echo "IMP Awards Scraper - Diagnostic Tool"
echo "=========================================="
echo ""

echo "1. Python version:"
python3 --version 2>&1 || echo "  ❌ python3 not found"
echo ""

echo "2. Current directory:"
pwd
ls -la | grep -E "(poster_downloader|requirements|\.env)" || echo "  ❌ Not in project directory?"
echo ""

echo "3. Virtual environment:"
if [ -d "venv" ]; then
  echo "  ✓ venv directory exists"
  if [ -f "venv/bin/python" ]; then
    echo "  ✓ venv/bin/python exists"
    venv/bin/python --version
  else
    echo "  ❌ venv/bin/python missing"
  fi
else
  echo "  ❌ venv directory missing"
fi
echo ""

echo "4. Dependencies:"
if [ -d "venv" ]; then
  venv/bin/pip list 2>&1 | grep -E "(requests|beautifulsoup4|pillow|dotenv|yaml)" || echo "  ❌ Dependencies not installed"
else
  echo "  ❌ Skipped (no venv)"
fi
echo ""

echo "5. Configuration files:"
[ -f "genre_config.yaml" ] && echo "  ✓ genre_config.yaml" || echo "  ⚠️  genre_config.yaml missing (optional)"
[ -f "resolution_config.yaml" ] && echo "  ✓ resolution_config.yaml" || echo "  ⚠️  resolution_config.yaml missing (optional)"
[ -f "movie_metadata.json" ] && echo "  ✓ movie_metadata.json" || echo "  ⚠️  movie_metadata.json missing"
echo ""

echo "6. .env file:"
if [ -f ".env" ]; then
  echo "  ✓ .env exists"
  grep -c "TMDB_API_KEY" .env && echo "    ✓ TMDB_API_KEY set" || echo "    ❌ TMDB_API_KEY missing"
  grep -c "SMTP_" .env && echo "    ✓ Email settings found" || echo "    ⚠️  Email settings missing (optional)"
else
  echo "  ❌ .env missing"
fi
echo ""

echo "7. Main script:"
if [ -f "poster_downloader.py" ]; then
  echo "  ✓ poster_downloader.py exists"
  if [ -x "poster_downloader.py" ]; then
    echo "  ✓ poster_downloader.py is executable"
  else
    echo "  ⚠️  poster_downloader.py not executable"
  fi
else
  echo "  ❌ poster_downloader.py missing"
fi
echo ""

echo "8. Test run:"
echo "  Attempting test with venv..."
if [ -f "venv/bin/python" ]; then
  venv/bin/python poster_downloader.py --help 2>&1 | head -20 || echo "  ❌ Test failed"
else
  echo "  ❌ Skipped (no venv)"
fi
echo ""

echo "=========================================="
echo "Diagnostic complete"
echo "=========================================="
