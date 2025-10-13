# Versioning Guide

This project follows [Semantic Versioning](https://semver.org/) (SemVer).

## Version Format

**MAJOR.MINOR.PATCH** (e.g., 1.0.0, 1.2.3, 2.0.0)

## Version Components

### MAJOR version (x.0.0)

Incremented when making **incompatible API changes**:
- Breaking changes to command-line arguments
- Incompatible changes to configuration file formats
- Removal of supported features
- Changes that require user action to upgrade

**Example:** 1.x.x → 2.0.0
- Renamed `--latest` to `--recent`
- Changed genre_config.yaml format
- Removed support for Python 3.7

### MINOR version (1.x.0)

Incremented when adding **new functionality** in a backward-compatible manner:
- New command-line options
- New configuration options
- New features (e.g., new download modes)
- Performance improvements

**Example:** 1.0.0 → 1.1.0
- Added support for downloading by movie name
- Added `--parallel` for concurrent downloads
- Added resume capability

### PATCH version (1.0.x)

Incremented for **backward-compatible bug fixes**:
- Fix parsing errors
- Fix download issues
- Fix documentation typos
- Security updates
- Dependency updates

**Example:** 1.0.0 → 1.0.1
- Fixed XLG dimension parsing
- Fixed genre filter case sensitivity
- Updated documentation

## Current Version

**1.0.0** - Initial production release

All core features implemented:
- TMDb API integration
- Genre blocklist and filtering
- Resolution configuration
- Duplicate detection
- Batch processing
- Multi-page support
- Fully automated CLI

## Version History

### 1.0.0 (2025-10-13)
- Initial production release
- All requested features complete and tested

## How to Update Version

1. **Update VERSION file**
   ```bash
   echo "1.1.0" > VERSION
   ```

2. **Update `__version__` in poster_downloader.py**
   ```python
   __version__ = "1.1.0"
   ```

3. **Update README.md version badge**

4. **Update CHANGELOG.md**
   - Add new section with version and date
   - List changes under Added/Changed/Fixed/Removed

5. **Commit and tag**
   ```bash
   git add -A
   git commit -m "Release v1.1.0 - Description of changes"
   git tag -a v1.1.0 -m "Release v1.1.0"
   git push origin master --tags
   ```

## Version Tracking

- **VERSION file**: Single source of truth for version number
- **poster_downloader.py**: `__version__` variable
- **README.md**: Version badge at top
- **Git tags**: v1.0.0, v1.1.0, etc.
- **CHANGELOG.md**: Detailed change history

## Examples

### Bug Fix (1.0.0 → 1.0.1)
```
Fixed issue where dimension parsing failed for certain posters
```

### New Feature (1.0.0 → 1.1.0)
```
Added --parallel flag for concurrent downloads
Added support for downloading by movie name
```

### Breaking Change (1.0.0 → 2.0.0)
```
Renamed configuration files
Changed command-line argument format
Requires Python 3.9+
```

## Release Checklist

- [ ] Update VERSION file
- [ ] Update __version__ in code
- [ ] Update README.md version
- [ ] Update CHANGELOG.md
- [ ] Run tests
- [ ] Commit changes
- [ ] Create Git tag
- [ ] Push to GitHub
- [ ] Create GitHub release (optional)

