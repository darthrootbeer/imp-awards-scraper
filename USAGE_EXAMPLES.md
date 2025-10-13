# Usage Examples

This guide provides practical examples for using the IMP Awards Poster Downloader.

## Quick Start

### Download Recent Posters (Fully Automated)

```bash
# Download all posters from the latest additions page
python poster_downloader.py --latest

# Download from the last 5 recent pages (~200-250 posters)
python poster_downloader.py --latest --pages 5

# Download last 10 pages (~350-400 posters)
python poster_downloader.py --latest --pages 10

# Clear everything and download fresh
python poster_downloader.py --startfresh --latest
```

These commands run **fully automated** with no prompts.

### Download Entire Year (Fully Automated)

```bash
# Download all posters from 2024 (~2,135 posters)
python poster_downloader.py --year 2024

# Clear downloads and rebuild 2024 from scratch
python poster_downloader.py --startfresh --year 2024

# Download all posters from 2023
python poster_downloader.py --year 2023

# Download from 2021
python poster_downloader.py --year 2021
```

## Genre Filtering

### Single Genre Filter

```bash
# Only Animation movies from 2024
python poster_downloader.py --year 2024 --genre Animation

# Only Horror movies from recent additions
python poster_downloader.py --latest --genre Horror

# Only Science Fiction from 2023
python poster_downloader.py --year 2023 --genre "Science Fiction"
```

### Multiple Genre Filter (AND Logic)

```bash
# Movies that are BOTH Romance AND Comedy from 2021
python poster_downloader.py --year 2021 --genre Romance --genre Comedy

# Movies that are Animation AND Family from 2024
python poster_downloader.py --year 2024 --genre Animation --genre Family

# Recent posters that are Action AND Science Fiction
python poster_downloader.py --latest --genre Action --genre "Science Fiction"
```

## Advanced Combinations

### Genre Filter + Multi-Page

```bash
# Last 20 pages, only Animation + Family movies
python poster_downloader.py --latest --pages 20 --genre Animation --genre Family

# Last 50 pages, only Science Fiction
python poster_downloader.py --latest --pages 50 --genre "Science Fiction"
```

### Genre Blocklist vs Genre Filter

**Use blocklist** (`genre_config.yaml`) to **permanently exclude** genres:
- Set `Horror: allow: false` to never download horror
- Applies to ALL operations

**Use genre filter** (`--genre`) to **temporarily include only** specific genres:
- `--genre Animation` downloads ONLY animation
- Only applies to that specific command

**Combine both:**
```bash
# In genre_config.yaml: block Horror
# Command line: only get Animation + Family from 2024
python poster_downloader.py --year 2024 --genre Animation --genre Family

# This will:
# 1. Filter TO Animation + Family movies
# 2. Still block Horror (if one somehow had all three genres)
```

## Interactive Mode

### Single Poster with Preview

```bash
python poster_downloader.py
```

Choose option 2, enter URL, see genres, confirm before download.

### Batch with Preview

```bash
python poster_downloader.py
```

Choose option 1 or 3, see the count, confirm before batch processing.

## Production Use Cases

### Daily Automation

Add to cron/launchd to download new posters daily:

```bash
# Download latest posters every day at 2 AM
0 2 * * * cd /path/to/impawards2025 && source venv/bin/activate && python poster_downloader.py --latest
```

### Archive Building

Build a complete collection:

```bash
# Download all posters from last 5 years
for year in 2025 2024 2023 2022 2021; do
    python poster_downloader.py --year $year
done

# Or with genre filtering
for year in 2025 2024 2023 2022 2021; do
    python poster_downloader.py --year $year --genre "Science Fiction"
done
```

### Catch Up on Recent Additions

```bash
# Download last 100 pages of recent additions
python poster_downloader.py --latest --pages 100
```

This would process ~3,600-5,000 posters!

## Expected Download Volumes

### Recent Additions

- 1 page: ~50 posters
- 5 pages: ~200-250 posters
- 10 pages: ~350-400 posters
- 100 pages: ~3,600-5,000 posters

### By Year

- 2025 (partial): ~500-1,000 posters (year in progress)
- 2024: ~2,135 posters
- 2023: ~2,000+ posters
- Older years: ~1,500-2,500 posters each

### Disk Space

- Average XXLG poster: ~1-3 MB
- Average XLG poster: ~400-800 KB
- 100 posters: ~100-300 MB
- 1,000 posters: ~1-3 GB
- Full year (2,000 posters): ~2-6 GB

## Tips

1. **Start small**: Test with `--latest` first (~50 posters)
2. **Use genre filters**: Narrow down to what you want
3. **Set blocklist**: Edit `genre_config.yaml` to exclude unwanted genres permanently
4. **Monitor progress**: The script shows progress and stats
5. **Interrupt safely**: Press Ctrl+C to stop - it will show stats for what completed
6. **Check TMDb quota**: Free tier has limits (~1,000 requests/day) - might hit limit on large batches

## Troubleshooting

### No Genres Showing

Make sure `TMDB_API_KEY` is set in `.env` file or environment.

### Too Many Posters Skipped

Check `genre_config.yaml` - you might have genres blocked that you want.

### Want to Exclude Specific Genres

Edit `genre_config.yaml` and set unwanted genres to `allow: false`.

### Want Only Specific Genres

Use `--genre` filter on command line instead of blocklist.
