# Resolution Configuration Guide

The resolution configuration allows you to control which poster sizes the script will download.

## Configuration File

Edit `resolution_config.yaml` to customize which resolutions you want.

## Available Resolutions

The script supports four resolution sizes in priority order (highest to lowest):

| Resolution | Typical Size | Description | Availability |
|------------|--------------|-------------|--------------|
| **XXXLG** | 3000x4500+ | Extra-extra-extra large | Very rare |
| **XXLG** | 2025x3000 | Extra-extra large | Most common high-res |
| **XLG** | 1013x1500 | Extra large | Common fallback |
| **LG** | 675x1000 | Large (standard) | Lower quality |

## How It Works

The script:

1. Loads `resolution_config.yaml` at startup
2. Checks what resolutions are available on the poster page
3. Downloads the **highest resolution** that is both:
   - Available on the page
   - Enabled in your configuration

## Default Configuration

```yaml
resolutions:
  XXXLG:
    allow: true   # Enabled (will download if available)
  XXLG:
    allow: true   # Enabled (most common)
  XLG:
    allow: true   # Enabled (good fallback)
  LG:
    allow: false  # Disabled (too low quality)
```

With these settings:

- Downloads XXXLG if available (rare)
- Falls back to XXLG if available (common)
- Falls back to XLG if XXLG not available
- Skips LG even if it's the only size available

## Example Configurations

### Highest Quality Only (XXLG+)

```yaml
# Highest quality only
resolutions:
  XXXLG:
    allow: true
  XXLG:
    allow: true
  XLG:
    allow: false   # Disable XLG
  LG:
    allow: false
```

Result: Only downloads XXLG or XXXLG. Skips posters that only have XLG.

### Maximum Coverage (Accept All)

```yaml
# Accept all sizes
resolutions:
  XXXLG:
    allow: true
  XXLG:
    allow: true
  XLG:
    allow: true
  LG:
    allow: true    # Enable even LG
```

Result: Downloads any available size. Gets the most posters possible.

### XLG Only (Balanced)

```yaml
# XLG only
resolutions:
  XXXLG:
    allow: false
  XXLG:
    allow: false
  XLG:
    allow: true    # Only XLG
  LG:
    allow: false
```

Result: Only downloads XLG size. Skips XXLG and LG.

## Output Examples

### When Resolution Is Enabled

```text
Movie: Tron: Ares
Year: 2025
Poster: #1
✓ XXLG available: 2025x3000
Downloading: http://www.impawards.com/2025/posters/tron_ares_xxlg.jpg
✓ Saved to: downloads/2025/tron_ares/tron_ares_XXLG_2025x3000.jpg
```

### When Resolution Is Disabled

```text
Movie: Predator: Badlands
Year: 2025
Poster: #12
  XLG available but disabled in resolution_config.yaml
✗ No enabled resolutions found - SKIPPING
  Edit resolution_config.yaml to enable resolutions
```

### Multiple Resolutions Available

If a poster has both XXLG and XLG:

- With both enabled: Downloads XXLG (higher priority)
- With only XLG enabled: Downloads XLG
- With both disabled: Skips the poster

## Startup Message

When the script runs, it shows which resolutions are enabled:

```text
============================================================
IMP Awards Poster Downloader
============================================================

  Resolution settings: XXXLG, XXLG, XLG enabled
```

This confirms your configuration was loaded correctly.

## Use Cases

### Archival Quality Collection

Only accept the absolute highest quality:

```yaml
XXXLG: allow: true
XXLG: allow: true
XLG: allow: false
LG: allow: false
```

### Bandwidth-Conscious Downloading

Skip the huge files, stick with XLG:

```yaml
XXXLG: allow: false
XXLG: allow: false
XLG: allow: true
LG: allow: false
```

### Complete Collection

Get everything, regardless of size:

```yaml
# Enable all four resolutions
XXXLG: allow: true
XXLG: allow: true
XLG: allow: true
LG: allow: true
```

## Tips

1. **Default is good**: XXXLG + XXLG + XLG covers 99% of posters
2. **LG is usually too small**: Only enable for maximum coverage
3. **XXXLG is rare**: Worth enabling, won't download much extra
4. **Test your settings**: Use `--latest` to test configuration
5. **Combine with genre filter**: Resolution and genre filters work together

## File Naming

Downloaded files include the resolution in the name:

```text
tron_ares_XXLG_2025x3000.jpg
predator_badlands_ver12_XLG_1080x1350.jpg
movie_name_XXXLG_3000x4500.jpg
```

This makes it easy to identify what resolution you downloaded.
