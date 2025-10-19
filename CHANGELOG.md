# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-10-13
## [1.4.0] - 2025-10-19

### Added

- Guided installation script (`scripts/install.py`) for non-technical users
  - Creates/updates the virtual environment and installs dependencies
  - Collects TMDb + email credentials, writes `.env`
  - Generates reusable digest runner (`scripts/run_email_digest.sh`)
  - Optionally schedules the daily email digest via `crontab`
- Convenience shell runner `scripts/run_email_digest.sh`
- Documentation updates (README, quick-start guides) referencing the new installer and metadata store

### Changed

- Email digest subjects now display poster counts: `[NNN] • IMP Update …`
- `poster_downloader.py` records movie-level metadata in `movie_metadata.json`
- CLI/interactive menu support for `--movie` downloads and new metadata workflow

### Fixed

- Normalized movie keys in the metadata store so all poster variants roll up to a single movie entry

## [1.3.0] - 2025-10-14

### Added

- `--email-digest`, `--digest-pages`, and `--digest-test` CLI flags
- Stateful crawl that stops at the last emailed poster (via new `digest_tracker.py`)
- `digest_state.json` tracking file alongside existing email tracking
- Documentation updates covering digest workflow and automation recipes
- `--movie` CLI flag and interactive menu option to download every poster variant for a specific movie
- Automatic `movie_metadata.json` store capturing movie-level details (IDs, release date, genres, poster inventory)

### Changed

- Email subject helper now supports custom prefixes for test runs
- `process_poster_page` returns download paths for downstream email usage
- Batch processors now report already-downloaded posters separately

### Fixed

- Resolved tuple truthiness bug in batch processors by unpacking return values
- Ensured recent-page crawler avoids duplicates and respects digest boundaries


### Changed

- **Flat directory structure**: All posters now saved in single downloads/ folder
- **Filename format**: Year prefix added to filenames (e.g., `2025_tron_ares_XXLG_2025x3000.jpg`)
- Simplified file organization for easier browsing and sorting

### Benefits

- Easier to browse all posters in one location
- Natural sorting by year when viewing folder
- Simpler backup and sync operations
- No nested directory structure to navigate

## [1.0.0] - 2025-10-13

### Added

- Initial project setup
- Single poster page downloader with interactive URL prompt
- TMDb API integration: uses IMDb ID to fetch genre information via TMDb
- **Genre blocklist system**: YAML-based configuration to filter unwanted genres automatically
- **Batch processing**: Process all posters from recent additions page
- **Multi-page processing**: Process multiple recent archive pages with `--pages` option
- **Year-based batch processing**: Download all posters for a specific year
- **Command-line interface**: `--latest`, `--year=YYYY`, `--genre`, `--pages=N`, and `--startfresh` arguments
- **Genre filtering**: Filter by specific genres using AND logic (e.g., `--genre Romance --genre Comedy`)
- **Resolution configuration**: YAML-based config to control which sizes to download (XXXLG, XXLG, XLG, LG)
- **Duplicate detection**: Automatically skips already-downloaded files to enable resuming interrupted downloads
- **Start fresh option**: `--startfresh` flag to clear downloads folder and disable duplicate checking
- Main menu system with multiple processing options
- Smart resolution selection (XXLG > XLG > Skip)
- Interactive confirmation: displays genres and asks before downloading (single mode)
- Auto-processing in batch mode (no individual confirmations)
- Direct image URL construction from resolution links
- Organized folder structure for downloads (year/movie_name/)
- Comprehensive error handling with graceful degradation (works without API key)
- Batch processing statistics and progress tracking
- Detailed setup documentation for TMDb API
- Environment variable support via .env file (using python-dotenv)
- Genre configuration file with all 19 TMDb genres and descriptions

### Changed

- **Switched to TMDb API** for genre detection (replaced IMDb scraping for better reliability and performance)
- **Command-line mode is fully automated** - no confirmation prompts when using --latest or --year
- Script now prompts for URL interactively instead of requiring command-line argument
- Constructs image URLs directly from resolution links for efficiency (e.g., `tron_ares_xxlg.html` → `posters/tron_ares_xxlg.jpg`)
- File naming uses base poster name: `{base_name}_{SIZE}_{dimensions}.jpg` (e.g., `tron_ares_ver2_XXLG_2025x3000.jpg`)

### Fixed

- Dimension parsing now correctly handles posters with only XLG (no XXLG) by filtering out image wrapper links

### Removed

- IMDb web scraping (replaced with TMDb API)
