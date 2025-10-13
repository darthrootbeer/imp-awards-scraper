# Genre Blocklist Guide

The genre blocklist allows you to automatically filter out movie posters based on their genres, which is especially useful when batch-processing multiple posters.

## How It Works

When the script encounters a movie:
1. It fetches the movie's genres from TMDb
2. It checks those genres against your `genre_config.yaml` file
3. If **ANY** genre is marked as `allow: false`, the poster is **automatically skipped**
4. No download confirmation prompt is shown for blocked movies

## Configuration File

Edit `genre_config.yaml` to customize your preferences.

### Default Behavior

By default, **all genres are allowed** (`allow: true`).

### Blocking Genres

To block a genre, change its `allow` setting to `false`:

```yaml
genres:
  Horror:
    allow: false  # Block all horror movies
    description: "Designed to frighten, scare, or disgust"
```

### Example Configurations

#### Block Multiple Genres

```yaml
genres:
  Horror:
    allow: false
  Thriller:
    allow: false
  Crime:
    allow: false
```

This will skip any movie that is Horror, Thriller, or Crime.

#### Allow Only Specific Genres

To only allow certain genres, set all others to `false`:

```yaml
genres:
  Action:
    allow: true
  Science Fiction:
    allow: true
  Adventure:
    allow: true
  # Set all others to allow: false
  Animation:
    allow: false
  Comedy:
    allow: false
  # ... etc
```

## Available Genres

The configuration file includes all 19 TMDb genres:

| Genre | Description |
|-------|-------------|
| **Action** | High-energy films with physical stunts, chases, fights |
| **Adventure** | Exploration, quests, journeys to exotic locations |
| **Animation** | Animated films (hand-drawn, CGI, stop-motion) |
| **Comedy** | Humorous films designed to make audiences laugh |
| **Crime** | Criminal activities, investigations, heists |
| **Documentary** | Non-fiction films documenting reality |
| **Drama** | Serious, plot-driven narratives with character development |
| **Family** | Suitable for all ages, family-friendly content |
| **Fantasy** | Magical elements, mythical creatures, imaginary worlds |
| **History** | Historical events, periods, or figures |
| **Horror** | Designed to frighten, scare, or disgust |
| **Music** | Music-focused films, musicals, concert films |
| **Mystery** | Suspenseful investigations, puzzles to solve |
| **Romance** | Romantic relationships and love stories |
| **Science Fiction** | Futuristic concepts, space, technology, sci-fi elements |
| **TV Movie** | Films made specifically for television |
| **Thriller** | Suspenseful, tension-filled narratives |
| **War** | Military conflicts, warfare, combat |
| **Western** | American Old West, cowboys, frontier life |

## Usage Examples

### Example 1: Family-Friendly Only

```yaml
genres:
  Family:
    allow: true
  Animation:
    allow: true
  # Block potentially mature content
  Horror:
    allow: false
  Thriller:
    allow: false
  War:
    allow: false
```

### Example 2: No Romance or Musicals

```yaml
genres:
  Romance:
    allow: false
  Music:
    allow: false
  # All others remain true
```

### Example 3: Action & Sci-Fi Fan

```yaml
genres:
  Action:
    allow: true
  Science Fiction:
    allow: true
  Adventure:
    allow: true
  Fantasy:
    allow: true
  Thriller:
    allow: true
  # Block everything else
  Animation:
    allow: false
  Comedy:
    allow: false
  Crime:
    allow: false
  Documentary:
    allow: false
  Drama:
    allow: false
  Family:
    allow: false
  History:
    allow: false
  Horror:
    allow: false
  Music:
    allow: false
  Mystery:
    allow: false
  Romance:
    allow: false
  TV Movie:
    allow: false
  War:
    allow: false
  Western:
    allow: false
```

## Output Examples

### When Genres Are Allowed

```
✓ Genres: Science Fiction, Adventure, Action

Movie: Tron: Ares
Year: 2025
Poster: #1
✓ XXLG available: 2025x3000

Proceed with download? (yes/no):
```

### When Genres Are Blocked

```
✓ Genres: Science Fiction, Adventure, Action
✗ BLOCKED: Movie contains blocked genre(s): Action
  Edit genre_config.yaml to change genre settings
```

The script exits immediately without asking for confirmation.

## Tips

1. **Start permissive**: Leave all genres as `allow: true` initially
2. **Refine as needed**: Block genres you discover you don't want
3. **Comments**: Add your own comments in the YAML file with `#`
4. **Backup**: Keep a copy of your configuration if you experiment
5. **Check spelling**: Genre names must match exactly (case-sensitive)

## Batch Processing

This feature is especially powerful when you implement batch processing in the future. Instead of manually confirming/rejecting each poster, the blocklist will automatically filter out unwanted genres, saving you time.

