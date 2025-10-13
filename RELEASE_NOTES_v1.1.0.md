# Release Notes - v1.1.0

**Release Date:** 2025-10-13  
**Repository:** https://github.com/darthrootbeer/imp-awards-scraper

## Major Change: Flat Directory Structure

### What Changed

**Old structure (v1.0.0):**
```
downloads/
  2025/
    tron_ares/
      tron_ares_XXLG_2025x3000.jpg
  2021/
    dune/
      dune_XXLG_2024x3000.jpg
```

**New structure (v1.1.0):**
```
downloads/
  2025_tron_ares_XXLG_2025x3000.jpg
  2021_dune_XXLG_2024x3000.jpg
```

### Benefits

1. **Simpler browsing** - All posters in one location
2. **Natural sorting** - Files sort chronologically by year
3. **Easier backup** - No nested directory structure
4. **Faster operations** - Single folder, no subdirectories to traverse

### Filename Format

**Pattern:** `{year}_{base_name}_{SIZE}_{dimensions}.jpg`

**Examples:**
- `2025_tron_ares_ver30_XXLG_2053x3000.jpg`
- `2024_dune_part_two_XXLG_2024x3000.jpg`
- `2021_spider_man_no_way_home_ver15_XLG_1080x1350.jpg`

### Backward Compatibility

This is a **minor version** (1.x.0) change because:
- No command-line arguments changed
- No configuration format changed
- Existing downloads still work (just in old structure)
- No action required from users

### Migration Note

If you have downloads from v1.0.0:
- They will remain in the old nested structure
- New downloads will use the flat structure
- Both can coexist
- Or use `--startfresh` to rebuild with new structure

### Testing

Verified with:
- Tron: Ares (2025) → `2025_tron_ares_XXLG_2025x3000.jpg` ✓
- Dune (2021) → `2021_dune_XXLG_2024x3000.jpg` ✓
- Duplicate detection still works ✓
- Batch processing still works ✓

### Upgrade

```bash
cd imp-awards-scraper
git pull origin master
# Version automatically updated to 1.1.0
```

---

## Security Note

Your TMDb API key in `.env` is still properly protected:
- ✅ .env is in .gitignore
- ✅ .env never committed to Git
- ✅ No API keys in repository
- ✅ Clear instructions in README for users to get their own key

---

**Download the new version:**  
https://github.com/darthrootbeer/imp-awards-scraper
