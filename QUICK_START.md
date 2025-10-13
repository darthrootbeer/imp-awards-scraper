# Quick Start Guide

Get up and running in 3 minutes.

## Setup (One-Time)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Get TMDb API key (free)
#    Visit: https://www.themoviedb.org/settings/api
#    Sign up, request developer API key

# 3. Create .env file with your key
echo 'TMDB_API_KEY=your_key_here' > .env
```

## Common Commands

### Test with Single Poster

```bash
python poster_downloader.py
# Choose option 2
# Enter URL: http://www.impawards.com/2025/tron_ares.html
# See genres, confirm download
```

### Download Recent Additions (Fully Automated)

```bash
# Latest page only (~50 posters)
python poster_downloader.py --latest

# Last 5 pages (~200-250 posters)
python poster_downloader.py --latest --pages 5

# Clear downloads and start fresh
python poster_downloader.py --startfresh --latest
```

### Download Entire Year (Fully Automated)

```bash
# All 2024 posters (~2,135 posters)
python poster_downloader.py --year 2024

# Clear downloads and rebuild from scratch
python poster_downloader.py --startfresh --year 2024
```

### Filter by Genre

```bash
# Only Animation from 2024
python poster_downloader.py --year 2024 --genre Animation

# Only Romance + Comedy (must have BOTH)
python poster_downloader.py --year 2021 --genre Romance --genre Comedy
```

## What Gets Downloaded

- **Resolution**: XXLG (preferred) or XLG (fallback)
- **Format**: JPEG files
- **Location**: `downloads/YEAR/movie_name/poster_name_SIZE_dimensions.jpg`
- **Filtered by**: Your `genre_config.yaml` blocklist + any --genre filters

## Customization

Edit `genre_config.yaml` to block genres you never want:

```yaml
genres:
  Horror:
    allow: false  # Never download horror
  Romance:
    allow: false  # Never download romance
```

## Next Steps

- See [README.md](README.md) for complete documentation
- See [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) for advanced examples
- See [GENRE_BLOCKLIST.md](GENRE_BLOCKLIST.md) for filtering guide

## Help

```bash
python poster_downloader.py --help
```

Shows all available options.
