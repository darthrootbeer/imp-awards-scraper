# IMP Awards Scraper

**Version:** 1.3.0  
**Repository:** [https://github.com/darthrootbeer/imp-awards-scraper](https://github.com/darthrootbeer/imp-awards-scraper)

A Python tool for downloading high-resolution movie posters from [IMP Awards](http://www.impawards.com).

## Overview

This tool automatically identifies and downloads the highest resolution version available for movie posters on IMP Awards. It prioritizes XXLG resolution over XLG, and skips posters that don't have either.

**Perfect for automated bulk downloads** - Command-line mode runs fully automated with genre filtering, multi-page processing, and detailed progress tracking.

## Features

- **TMDb API Integration**: Uses The Movie Database API to fetch accurate genre information
- **Genre Blocklist**: Automatically filter out unwanted genres (Horror, Romance, etc.)
- **Genre Filtering**: Filter by specific genres using AND logic (`--genre Animation --genre Family`)
- **Resolution Control**: Configure which sizes to download (XXXLG, XXLG, XLG, LG)
- **Duplicate Detection**: Automatically skips already-downloaded files (resume interrupted downloads)
- **IMDb ID Detection**: Automatically extracts IMDb ID from poster pages
- **Smart Resolution Selection**: Downloads highest enabled and available resolution
- **Email Digest Automation**: Builds daily email summaries of new posters with state tracking
- **Interactive Confirmation**: Shows genre info and asks before downloading
- **Flat Directory Structure**: All posters in single downloads/ folder with year prefix
- **Clean Filenames**: Includes year, poster name, resolution type, and dimensions

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/darthrootbeer/imp-awards-scraper.git
cd imp-awards-scraper
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Get a free TMDb API key

- Create an account at [https://www.themoviedb.org/](https://www.themoviedb.org/)
- Go to Settings → API → Request API Key
- Choose "Developer" and fill out the form
- Copy your API key

### 4. Set your API key

#### Option A: Using .env file

Create a `.env` file in the project directory:

```bash
echo 'TMDB_API_KEY=your_api_key_here' > .env
```

The script will automatically load it.

#### Option B: Environment variable

For current session:

```bash
export TMDB_API_KEY="your_api_key_here"
```

Or add to your shell profile (`~/.zshrc`, `~/.bashrc`, etc.):

```bash
echo 'export TMDB_API_KEY="your_api_key_here"' >> ~/.zshrc
source ~/.zshrc
```

## Usage

### Command-Line Mode (Fully Automated)

Use command-line arguments for fully automated processing with **no interactive prompts**:

```bash
# Download all recent additions (latest page only)
python poster_downloader.py --latest

# Download from the last 5 recent pages (~250 posters)
python poster_downloader.py --latest --pages 5

# Download all posters from a specific year
python poster_downloader.py --year 2024

# Clear downloads folder and start fresh
python poster_downloader.py --startfresh --year 2024

# Filter by genre (only Animation movies from 2024)
python poster_downloader.py --year 2024 --genre Animation

# Filter by multiple genres (movies that are BOTH Romance AND Comedy from 2021)
python poster_downloader.py --year 2021 --genre Romance --genre Comedy

# Combine everything: Last 10 pages, only Animation + Family movies
python poster_downloader.py --latest --pages 10 --genre Animation --genre Family

# Clear and rebuild entire 2024 collection from scratch
python poster_downloader.py --startfresh --year 2024

# Email digest of posters added since the last run (scan up to 5 pages)
python poster_downloader.py --email-digest --digest-pages 5
```

All command-line modes automatically:

- Run fully automated (no confirmation prompts)
- Apply genre blocklist filtering (blocks unwanted genres)
- Apply genre filter if specified (requires ALL specified genres)
- Use XXLG > XLG resolution priority
- Show progress and final statistics

**Duplicate Detection:**

By default, the script skips files that have already been downloaded:

- Checks if file exists before downloading
- Shows "✓ Already downloaded" message
- Statistics separate new downloads from existing files
- Allows resuming interrupted batch downloads
- Example: Run `--latest` multiple times, only new posters downloaded

**Start Fresh Option:**

Use `--startfresh` to disable duplicate detection and clear everything:

- Deletes entire `downloads/` directory
- Disables duplicate checking for this run
- Re-downloads everything from scratch
- Useful for rebuilding collections
- Example: `--startfresh --year 2024` clears everything then downloads all 2024 posters

**Multi-Page Processing:**

The `--pages` option works with `--latest` to process multiple archive pages:

- Each recent page has ~36-50 posters
- Pages are processed in chronological order (newest to oldest)
- Navigation follows the "older" links automatically
- Example: `--latest --pages=10` processes ~374 posters across 10 pages

### Key Command-Line Flags

- `--latest` – Process the most recent additions page (use with `--pages` for deeper scans)
- `--year YYYY` – Download all posters for a specific year
- `--genre NAME` – Apply AND filtering for one or more genres
- `--startfresh` – Clear downloads and disable duplicate detection for this run
- `--email-digest` – Send an email digest of posters added since the last digest
- `--digest-pages N` – Limit how deep the digest crawl goes (default: 5 pages)
- `--digest-test` – Prefix digest email subjects with `[TEST]`

### Interactive Menu Mode

Run without arguments to see the menu:

```bash
python poster_downloader.py
```

**Menu Options:**

**1. Process recent additions** - Downloads all posters from the latest additions page  
**2. Download single poster** - Downloads one specific poster by URL  
**3. Download all posters for a year** - Enter year when prompted  
**4. Download all posters for a movie** - Coming soon

### Command-Line Examples

#### Download Recent Additions

```bash
python poster_downloader.py --latest
```

Automatically processes all posters from `http://www.impawards.com/archives/latest.html`

#### Download All Posters from 2024

```bash
python poster_downloader.py --year 2024
```

Processes all 2,135+ posters from 2024 (filtered by your genre blocklist)

**Example:**

```text
Fetching recent additions from: http://www.impawards.com/archives/latest.html
✓ Found 50 posters on recent additions page

Ready to process 50 posters from recent additions
Posters will be filtered by your genre blocklist settings

Continue with batch processing? (yes/no): yes

============================================================
Starting batch processing...
============================================================

[1/50] Processing: http://www.impawards.com/2025/predator_badlands_ver12.html
✓ XXLG available: 2025x3000
Downloading...
✓ Saved to: downloads/2025/predator_badlands/predator_badlands_ver12_XXLG_2025x3000.jpg

[2/50] Processing: http://www.impawards.com/2025/shark_night_3d_ver5.html
✗ BLOCKED: Movie contains blocked genre(s): Horror
...

============================================================
BATCH PROCESSING COMPLETE
============================================================
Total posters:    50
Downloaded:       35
Skipped:          10
Errors:           0
============================================================
```

### Interactive Mode Examples

#### Batch Process Recent Additions

Choose option 1 from the menu.

#### Single Poster Download

Choose option 2 from the menu. **Example session:**

```text
Enter poster page URL: http://www.impawards.com/2025/tron_ares.html

Fetching poster page: http://www.impawards.com/2025/tron_ares.html
✓ Found IMDb URL: https://www.imdb.com/title/tt6604188
  Fetching genre data from TMDb...
✓ Genres: Science Fiction, Adventure, Action

Movie: Tron: Ares
Year: 2025
Poster: #1
✓ XXLG available: 2025x3000

Proceed with download? (yes/no): yes
Downloading: http://www.impawards.com/2025/posters/tron_ares_xxlg.jpg
✓ Saved to: downloads/2025/tron_ares/tron_ares_XXLG_2025x3000.jpg (1,130,350 bytes)

✓ Download complete!
```

This downloads the poster to:

```text
downloads/2025_tron_ares_XXLG_2025x3000.jpg
```

File naming pattern: `{year}_{base_name}_{SIZE}_{dimensions}.jpg`

## Configuration Files

### Genre Filtering (`genre_config.yaml`)

Block unwanted genres permanently:

```yaml
genres:
  Horror:
    allow: false  # Block horror movies
  Romance:
    allow: false  # Block romance movies
```

When a movie matches ANY blocked genre, it's automatically skipped.

See [GENRE_BLOCKLIST.md](GENRE_BLOCKLIST.md) for detailed guide.

### Resolution Control (`resolution_config.yaml`)

Control which poster sizes to download:

```yaml
resolutions:
  XXXLG:
    allow: true   # Extra-extra-extra large (rare)
  XXLG:
    allow: true   # Extra-extra large (common)
  XLG:
    allow: true   # Extra large (fallback)
  LG:
    allow: false  # Standard size (too low quality)
```

Script downloads highest enabled and available resolution.

See [RESOLUTION_CONFIG.md](RESOLUTION_CONFIG.md) for detailed guide.

## How It Works

1. **Prompt** - Asks you to enter a poster page URL
2. **IMDb Detection** - Extracts the IMDb ID from the poster page
3. **TMDb Lookup** - Fetches genre information from TMDb API using the IMDb ID
4. **Genre Filter** - Checks genres against your blocklist (auto-skips if blocked)
5. **Parse** - Extracts movie information and available resolution links
6. **Display Genres** - Shows the movie's genres from TMDb
7. **Prioritize** - Looks for XXLG version first, then XLG as fallback
8. **Confirm** - Asks if you want to proceed with the download (yes/no)
9. **Download** - If confirmed, downloads the highest available resolution to an organized folder structure
10. **Skip** - If genres blocked, resolution unavailable, or you decline, the poster is skipped

### Email Digest Workflow

1. **State Tracking** – `digest_state.json` records poster URLs that have already been emailed (or intentionally skipped).
2. **Crawl Latest Pages** – The crawler walks the `latest` archive, following “older” pages until it encounters a tracked poster or reaches the `--digest-pages` limit.
3. **Download & Reuse** – Posters are downloaded or reused from disk using the same resolution and genre rules as standard downloads.
4. **Digest Email** – `email_sender.py` batches posters, generates thumbnails, and emails them, optionally prefixing subjects with `[TEST]`.
5. **State Update** – Successful sends update the tracker so future digests only include genuinely new additions; skipped posters move to the ignored list.

## Resolution Priority (Configurable)

Priority order (highest to lowest):

1. **XXXLG** - Extra-extra-extra large (3000x4500+) - Very rare
2. **XXLG** - Extra-extra large (2025x3000) - Most common high-res
3. **XLG** - Extra large (1013x1500) - Common fallback
4. **LG** - Large standard (675x1000) - Lower quality

Default: XXXLG, XXLG, and XLG enabled. LG disabled.

Configure in `resolution_config.yaml` to change which sizes to download.

## Project Structure

```text
imp-awards-scraper/
├── poster_downloader.py       # Main downloader script
├── requirements.txt           # Python dependencies
├── genre_config.yaml          # Genre blocklist configuration
├── resolution_config.yaml     # Resolution preferences
├── .env                       # TMDb API key (create this)
├── downloads/                 # Downloaded posters (flat structure)
│   ├── 2025_tron_ares_XXLG_2025x3000.jpg
│   ├── 2024_dune_ver2_XXLG_2024x3000.jpg
│   └── 2021_movie_name_XLG_1080x1350.jpg
└── [documentation files]
```

## Requirements

- Python 3.7+
- requests
- beautifulsoup4
- lxml
- python-dotenv
- pyyaml
- TMDb API key (free) - [Get yours here](https://www.themoviedb.org/settings/api)

See [TMDB_SETUP.md](TMDB_SETUP.md) for detailed API setup instructions.

For comprehensive usage examples including automation scripts and advanced filtering, see [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md).

## Roadmap

- [x] Single poster download
- [x] **Batch processing for recent additions**
- [x] **Multi-page archive processing** (`--latest --pages=10`)
- [x] **Download all posters for a specific year**
- [x] **Command-line interface** (`--latest`, `--year`, `--genre`, `--pages`)
- [x] Genre blocklist filtering
- [x] Genre filter with AND logic
- [ ] Auto-discovery of all posters for a specific movie

## License

MIT License - See LICENSE file for details
