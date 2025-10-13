# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2025-10-13

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
