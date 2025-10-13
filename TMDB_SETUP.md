# TMDb API Setup Instructions

This application uses The Movie Database (TMDb) API to fetch movie genre information.

## Getting Your Free API Key

1. **Create an account** at [https://www.themoviedb.org/](https://www.themoviedb.org/)

2. **Request an API key**:
   - Go to your account settings
   - Navigate to the "API" section
   - Click "Request an API Key"
   - Choose "Developer" (free tier)
   - Fill out the application form with basic details
   - Accept the terms of use

3. **Copy your API key** from the API settings page

## Setting Up the API Key

### Option 1: .env File (Recommended - Easiest)

Create a `.env` file in the project directory:

```bash
echo 'TMDB_API_KEY=your_api_key_here' > .env
```

Replace `your_api_key_here` with your actual API key. The script will automatically load it using python-dotenv.

**Note:** The `.env` file is already in `.gitignore`, so your API key won't be committed to version control.

### Option 2: Environment Variable

**For current session:**
```bash
export TMDB_API_KEY="your_api_key_here"
```

**For permanent setup (macOS/Linux):**

Add to your shell profile (`~/.zshrc` for zsh or `~/.bashrc` for bash):

```bash
echo 'export TMDB_API_KEY="your_api_key_here"' >> ~/.zshrc
source ~/.zshrc
```

### Option 3: Edit the Script Directly (Not Recommended)

Open `poster_downloader.py` and find this line near the top:

```python
TMDB_API_KEY = os.environ.get('TMDB_API_KEY', '')
```

Change it to:

```python
TMDB_API_KEY = os.environ.get('TMDB_API_KEY', 'your_api_key_here')
```

**Warning:** Don't commit this change to version control as it exposes your API key.

## Verify Setup

Run the poster downloader. If the API key is set correctly, you'll see:

```
✓ Found IMDb URL: https://www.imdb.com/title/tt6604188
  Fetching genre data from TMDb...
✓ Genres: Action, Adventure, Science Fiction
```

If the API key is missing, you'll see:

```
Warning: TMDb API key not set. Set TMDB_API_KEY environment variable.
Get your free API key at: https://www.themoviedb.org/settings/api
```

## Why TMDb?

- **Free and reliable**: No scraping, clean API responses
- **Accurate data**: Official genre classifications
- **Fast**: Direct API calls, no HTML parsing needed
- **Generous limits**: 1000+ requests per day on free tier

