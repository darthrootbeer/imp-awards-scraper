#!/usr/bin/env python3
"""
IMP Awards Poster Scraper
Downloads the highest resolution movie poster from a given poster page URL.
Priority: XXXLG > XXLG > XLG > LG (configurable)

Version: 1.0.0
Repository: https://github.com/darthrootbeer/imp-awards-scraper
"""

__version__ = "1.0.0"

import requests
from bs4 import BeautifulSoup
import os
import re
import sys
import json
import yaml
import argparse
from urllib.parse import urljoin
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# TMDb API Configuration
# Get your free API key at: https://www.themoviedb.org/settings/api
TMDB_API_KEY = os.environ.get('TMDB_API_KEY', '')  # Loaded from .env file or environment variable
TMDB_BASE_URL = 'https://api.themoviedb.org/3'

# Configuration files
GENRE_CONFIG_FILE = 'genre_config.yaml'
RESOLUTION_CONFIG_FILE = 'resolution_config.yaml'


class PosterDownloader:
    def __init__(self, base_url="http://www.impawards.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive'
        })
        self.genre_config = self.load_genre_config()
        self.resolution_config = self.load_resolution_config()
    
    def load_genre_config(self):
        """
        Load genre configuration from YAML file.
        
        Returns:
            dict: Genre configuration with allow/block settings
        """
        try:
            if os.path.exists(GENRE_CONFIG_FILE):
                with open(GENRE_CONFIG_FILE, 'r') as f:
                    config = yaml.safe_load(f)
                    return config.get('genres', {})
            else:
                print(f"  Note: {GENRE_CONFIG_FILE} not found. All genres will be allowed.")
                return {}
        except Exception as e:
            print(f"  Warning: Could not load {GENRE_CONFIG_FILE}: {e}")
            return {}
    
    def load_resolution_config(self):
        """
        Load resolution configuration from YAML file.
        
        Returns:
            dict: Resolution configuration with allow settings
        """
        try:
            if os.path.exists(RESOLUTION_CONFIG_FILE):
                with open(RESOLUTION_CONFIG_FILE, 'r') as f:
                    config = yaml.safe_load(f)
                    resolutions = config.get('resolutions', {})
                    
                    # Show which resolutions are enabled
                    enabled = [name for name, settings in resolutions.items() 
                              if isinstance(settings, dict) and settings.get('allow', True)]
                    if enabled:
                        print(f"  Resolution settings: {', '.join(enabled)} enabled")
                    
                    return resolutions
            else:
                print(f"  Note: {RESOLUTION_CONFIG_FILE} not found. Default: XXLG > XLG")
                # Default configuration
                return {
                    'XXXLG': {'allow': True},
                    'XXLG': {'allow': True},
                    'XLG': {'allow': True},
                    'LG': {'allow': False}
                }
        except Exception as e:
            print(f"  Warning: Could not load {RESOLUTION_CONFIG_FILE}: {e}")
            # Default configuration
            return {
                'XXXLG': {'allow': True},
                'XXLG': {'allow': True},
                'XLG': {'allow': True},
                'LG': {'allow': False}
            }
    
    def check_genre_blocklist(self, genres):
        """
        Check if any of the movie's genres are blocked.
        
        Args:
            genres: List of genre strings
            
        Returns:
            tuple: (is_blocked: bool, blocked_genres: list)
        """
        if not self.genre_config:
            return False, []
        
        blocked = []
        for genre in genres:
            genre_setting = self.genre_config.get(genre, {})
            if isinstance(genre_setting, dict):
                if not genre_setting.get('allow', True):
                    blocked.append(genre)
        
        return len(blocked) > 0, blocked
    
    def check_genre_filter(self, movie_genres, required_genres):
        """
        Check if movie matches required genre filter (AND logic).
        
        Args:
            movie_genres: List of genre strings from the movie
            required_genres: List of required genre strings (all must match)
            
        Returns:
            tuple: (matches: bool, missing_genres: list)
        """
        if not required_genres:
            return True, []
        
        # Convert to case-insensitive comparison
        movie_genres_lower = [g.lower() for g in movie_genres]
        
        missing = []
        for required in required_genres:
            required_lower = required.lower()
            if required_lower not in movie_genres_lower:
                missing.append(required)
        
        return len(missing) == 0, missing
    
    def get_older_page_link(self, soup):
        """
        Extract the "older" page link from a latest/archive page.
        
        Args:
            soup: BeautifulSoup object of the page
            
        Returns:
            str: Relative URL to older page (e.g., 'page1637.html') or None
        """
        # Look for link with "older" text
        for link in soup.find_all('a', href=True):
            if 'older' in link.get_text().lower():
                href = link['href']
                # Should be format: page1637.html or " page1637.html"
                href = href.strip()
                if 'page' in href and '.html' in href:
                    return href
        return None
    
    def get_recent_posters(self, latest_url="http://www.impawards.com/archives/latest.html", num_pages=1):
        """
        Fetch all poster URLs from the latest additions page(s).
        
        Args:
            latest_url: URL to the latest additions page
            num_pages: Number of recent pages to process (default: 1)
            
        Returns:
            list: List of full poster page URLs from all requested pages
        """
        all_poster_links = []
        current_url = latest_url
        
        for page_num in range(1, num_pages + 1):
            print(f"\nFetching recent additions page {page_num}/{num_pages}: {current_url}")
            
            try:
                response = self.session.get(current_url)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'lxml')
                
                # Find all links that match poster pattern: ../YEAR/poster_name.html
                poster_links = []
                
                # Look for links in thumbnail divs (class="minimal_thumb")
                for div in soup.find_all('div', class_='minimal_thumb'):
                    link = div.find('a', href=True)
                    if link:
                        href = link['href']
                        # Pattern: ../2025/movie_name.html
                        if href.startswith('../') and '.html' in href:
                            # Convert relative URL to full URL
                            # ../2025/tron_ares.html -> http://www.impawards.com/2025/tron_ares.html
                            clean_href = href.replace('../', '')
                            full_url = f"{self.base_url}/{clean_href}"
                            poster_links.append(full_url)
                
                print(f"  ✓ Found {len(poster_links)} posters on this page")
                all_poster_links.extend(poster_links)
                
                # If we need more pages, find the "older" link
                if page_num < num_pages:
                    older_link = self.get_older_page_link(soup)
                    if older_link:
                        # Construct next URL
                        current_url = f"http://www.impawards.com/archives/{older_link}"
                    else:
                        print(f"  Warning: Could not find 'older' link. Stopping at page {page_num}")
                        break
                
            except Exception as e:
                print(f"  ✗ Error fetching page {page_num}: {e}")
                break
        
        print(f"\n✓ Total: {len(all_poster_links)} posters across {min(page_num, num_pages)} page(s)")
        
        return all_poster_links
    
    def get_year_posters(self, year):
        """
        Fetch all poster URLs for a specific year.
        
        Args:
            year: Year to fetch posters for (e.g., 2024)
            
        Returns:
            list: List of full poster page URLs
        """
        # Use the "std.html" page which shows all posters on one page
        year_url = f"{self.base_url}/{year}/std.html"
        print(f"\nFetching all posters for {year} from: {year_url}")
        
        try:
            response = self.session.get(year_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Find all links in the page
            poster_links = []
            
            for link in soup.find_all('a', href=True):
                href = link['href']
                # Look for poster links: movie_name.html, movie_name_ver2.html, etc.
                # Exclude navigation links (alpha1.html, alpha2.html, std.html, etc.)
                if (href.endswith('.html') and 
                    not href.startswith('/') and 
                    not href.startswith('http') and
                    not href.startswith('#') and
                    'alpha' not in href and
                    'std' not in href):
                    
                    full_url = f"{self.base_url}/{year}/{href}"
                    poster_links.append(full_url)
            
            # Remove duplicates (each poster appears twice in the HTML)
            poster_links = list(dict.fromkeys(poster_links))
            
            print(f"✓ Found {len(poster_links)} posters for year {year}")
            
            return poster_links
            
        except Exception as e:
            print(f"✗ Error fetching posters for year {year}: {e}")
            return []

    def parse_poster_page(self, url):
        """
        Parse a poster page and extract available resolution information.
        
        Returns:
            dict: {
                'movie_name': str,
                'year': str,
                'poster_number': str,
                'xxlg': {'link': str, 'dimensions': str} or None,
                'xlg': {'link': str, 'dimensions': str} or None,
                'base_name': str
            }
        """
        response = self.session.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Extract movie title and year from page title
        # Format: "Tron: Ares Movie Poster (#1 of 31) - IMP Awards"
        title_tag = soup.find('title')
        if title_tag:
            title_text = title_tag.text
            # Extract movie name and poster number
            match = re.search(r'(.+?) Movie Poster \(#(\d+) of \d+\)', title_text)
            if match:
                movie_name = match.group(1).strip()
                poster_number = match.group(2)
            else:
                movie_name = "Unknown"
                poster_number = "1"
        
        # Extract year from breadcrumb or URL
        year_match = re.search(r'/(\d{4})/', url)
        year = year_match.group(1) if year_match else "unknown"
        
        # Extract base name from URL
        # Format: http://www.impawards.com/2025/tron_ares.html
        url_match = re.search(r'/(\d{4})/([^/]+)\.html$', url)
        base_name = url_match.group(2) if url_match else None
        
        # Find "other sizes:" section
        # Looking for: other sizes: <a href = tron_ares_xlg.html>1013x1500</a> / <a href = tron_ares_xxlg.html>2025x3000</a>
        page_text = soup.get_text()
        
        result = {
            'movie_name': movie_name,
            'year': year,
            'poster_number': poster_number,
            'base_name': base_name,
            'xxxlg': None,
            'xxlg': None,
            'xlg': None,
            'lg': None
        }
        
        # Find all links in the "other sizes:" section
        # Look for the paragraph containing "other sizes:"
        for p in soup.find_all('p', class_='small'):
            if 'other sizes:' in p.get_text():
                # Find all links within this section
                for link in p.find_all('a'):
                    href = link.get('href', '')
                    dimensions = link.get_text().strip()
                    
                    # Only process links that have dimension text (e.g., "1080x1350")
                    # This filters out the second <a> tag that wraps the image
                    if not dimensions or 'x' not in dimensions:
                        continue
                    
                    # Check for all possible resolution sizes
                    if '_xxxlg.html' in href:
                        result['xxxlg'] = {
                            'link': href,
                            'dimensions': dimensions
                        }
                    elif '_xxlg.html' in href:
                        result['xxlg'] = {
                            'link': href,
                            'dimensions': dimensions
                        }
                    elif '_xlg.html' in href:
                        result['xlg'] = {
                            'link': href,
                            'dimensions': dimensions
                        }
                    elif '_lg.html' in href:
                        result['lg'] = {
                            'link': href,
                            'dimensions': dimensions
                        }
        
        return result

    def extract_imdb_url(self, soup):
        """
        Extract IMDb URL from the poster page.
        
        Args:
            soup: BeautifulSoup object of the poster page
            
        Returns:
            str: IMDb URL or None if not found
        """
        # Look for IMDb link: <a href = http://www.imdb.com/title/tt6604188 target = _blank>IMDb</a>
        for link in soup.find_all('a'):
            href = link.get('href', '')
            if 'imdb.com/title/' in href:
                # Ensure it uses https
                if href.startswith('http://'):
                    href = href.replace('http://', 'https://')
                elif not href.startswith('https://'):
                    href = 'https://' + href
                return href
        return None

    def get_genres_from_tmdb(self, imdb_id):
        """
        Fetch genre information from TMDb API using IMDb ID.
        
        Args:
            imdb_id: IMDb ID (e.g., 'tt6604188')
            
        Returns:
            list: List of genre strings, or empty list if not found
        """
        if not TMDB_API_KEY:
            print("  Warning: TMDb API key not set. Set TMDB_API_KEY environment variable.")
            print("  Get your free API key at: https://www.themoviedb.org/settings/api")
            return []
        
        try:
            # Use TMDb /find endpoint to search by IMDb ID
            url = f"{TMDB_BASE_URL}/find/{imdb_id}"
            params = {
                'api_key': TMDB_API_KEY,
                'external_source': 'imdb_id'
            }
            
            print(f"  Fetching genre data from TMDb...")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Check movie_results first (most common)
            movie_results = data.get('movie_results', [])
            if movie_results:
                movie = movie_results[0]
                genre_ids = movie.get('genre_ids', [])
                
                # Fetch genre names from genre IDs
                return self.get_genre_names_from_ids(genre_ids)
            
            return []
        except Exception as e:
            print(f"  Warning: Could not fetch TMDb data: {e}")
            return []
    
    def get_genre_names_from_ids(self, genre_ids):
        """
        Convert TMDb genre IDs to genre names.
        
        Args:
            genre_ids: List of genre IDs
            
        Returns:
            list: List of genre names
        """
        # TMDb genre mappings (as of 2024)
        genre_map = {
            28: 'Action', 12: 'Adventure', 16: 'Animation', 35: 'Comedy',
            80: 'Crime', 99: 'Documentary', 18: 'Drama', 10751: 'Family',
            14: 'Fantasy', 36: 'History', 27: 'Horror', 10402: 'Music',
            9648: 'Mystery', 10749: 'Romance', 878: 'Science Fiction',
            10770: 'TV Movie', 53: 'Thriller', 10752: 'War', 37: 'Western'
        }
        
        return [genre_map.get(gid, f'Unknown ({gid})') for gid in genre_ids]

    def construct_image_url(self, resolution_link, year):
        """
        Construct the image URL from the resolution HTML link.
        
        Args:
            resolution_link: Link to resolution page (e.g., 'tron_ares_xxlg.html')
            year: Year folder (e.g., '2025')
            
        Returns:
            str: Full URL to the actual image file
        """
        # Extract base name and suffix from link
        # e.g., 'tron_ares_xxlg.html' -> 'tron_ares_xxlg'
        base_with_suffix = resolution_link.replace('.html', '')
        
        # Construct image URL: http://www.impawards.com/{year}/posters/{base_with_suffix}.jpg
        image_url = f"{self.base_url}/{year}/posters/{base_with_suffix}.jpg"
        
        return image_url

    def check_file_exists(self, file_path):
        """
        Check if a file already exists and is valid.
        
        Args:
            file_path: Path to check
            
        Returns:
            bool: True if file exists and has content, False otherwise
        """
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            if file_size > 0:
                return True
        return False
    
    def download_image(self, url, save_path, skip_if_exists=True):
        """
        Download an image from URL to save_path.
        
        Args:
            url: Image URL
            save_path: Local file path to save to
            skip_if_exists: Skip download if file already exists (default: True)
            
        Returns:
            tuple: (success: bool, already_existed: bool)
        """
        # Check if file already exists
        if skip_if_exists and self.check_file_exists(save_path):
            file_size = os.path.getsize(save_path)
            print(f"✓ Already downloaded: {save_path} ({file_size:,} bytes)")
            return True, True
        
        print(f"Downloading: {url}")
        response = self.session.get(url, stream=True)
        response.raise_for_status()
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Download and save
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        file_size = os.path.getsize(save_path)
        print(f"✓ Saved to: {save_path} ({file_size:,} bytes)")
        return True, False

    def process_poster_page(self, url, output_dir="downloads", prompt_confirm=True, required_genres=None, skip_existing=True):
        """
        Process a single poster page: parse, identify best resolution, and download.
        
        Args:
            url: Poster page URL
            output_dir: Base directory for downloads
            prompt_confirm: Whether to ask for confirmation before downloading (default: True)
            required_genres: List of required genres (AND logic) or None to skip filter
            skip_existing: Whether to skip already downloaded files (default: True)
            
        Returns:
            tuple: (success: bool, already_existed: bool)
        """
        # Parse the page
        print(f"\nFetching poster page: {url}")
        response = self.session.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Extract IMDb URL and get genres
        imdb_url = self.extract_imdb_url(soup)
        genres = []
        
        if imdb_url:
            print(f"✓ Found IMDb URL: {imdb_url}")
            # Extract IMDb ID from URL (e.g., tt6604188 from https://www.imdb.com/title/tt6604188/)
            imdb_id_match = re.search(r'title/(tt\d+)', imdb_url)
            if imdb_id_match:
                imdb_id = imdb_id_match.group(1)
                genres = self.get_genres_from_tmdb(imdb_id)
                if genres:
                    print(f"✓ Genres: {', '.join(genres)}")
                    
                    # Check genre filter (if specified)
                    if required_genres:
                        matches, missing = self.check_genre_filter(genres, required_genres)
                        if not matches:
                            print(f"✗ FILTERED: Movie missing required genre(s): {', '.join(missing)}")
                            print(f"  Required: {', '.join(required_genres)}")
                            return False, False
                    
                    # Check genre blocklist
                    is_blocked, blocked_genres = self.check_genre_blocklist(genres)
                    if is_blocked:
                        print(f"✗ BLOCKED: Movie contains blocked genre(s): {', '.join(blocked_genres)}")
                        print(f"  Edit {GENRE_CONFIG_FILE} to change genre settings")
                        return False, False
                else:
                    print("  No genre information found")
            else:
                print("  Could not extract IMDb ID from URL")
        else:
            print("✗ No IMDb URL found on poster page")
        
        # Parse poster info
        info = self.parse_poster_page(url)
        
        print(f"\nMovie: {info['movie_name']}")
        print(f"Year: {info['year']}")
        print(f"Poster: #{info['poster_number']}")
        
        # Determine which resolution to download based on configuration
        # Priority order: XXXLG > XXLG > XLG > LG
        selected_size = None
        selected_info = None
        
        # Check resolutions in priority order
        resolution_priority = [
            ('xxxlg', 'XXXLG'),
            ('xxlg', 'XXLG'),
            ('xlg', 'XLG'),
            ('lg', 'LG')
        ]
        
        for res_key, res_name in resolution_priority:
            if info.get(res_key):
                # Check if this resolution is enabled in config
                res_config = self.resolution_config.get(res_name, {})
                is_allowed = res_config.get('allow', True) if isinstance(res_config, dict) else True
                
                if is_allowed:
                    selected_size = res_key
                    selected_info = info[res_key]
                    print(f"✓ {res_name} available: {selected_info['dimensions']}")
                    break
                else:
                    print(f"  {res_name} available but disabled in {RESOLUTION_CONFIG_FILE}")
        
        if not selected_size:
            print(f"✗ No enabled resolutions found - SKIPPING")
            print(f"  Edit {RESOLUTION_CONFIG_FILE} to enable resolutions")
            return False, False
        
        # Ask user for confirmation (if not in batch mode)
        if prompt_confirm:
            print()
            response = input("Proceed with download? (yes/no): ").strip().lower()
            if response not in ['yes', 'y']:
                print("Download cancelled by user")
                return False, False
        
        # Construct the image URL from the resolution link
        download_url = self.construct_image_url(
            selected_info['link'],
            info['year']
        )
        
        # Create save path: downloads/{year}/{movie_name}/{base_name}_{SIZE}_{dimensions}.jpg
        # Example: downloads/2025/tron_ares/tron_ares_ver2_XXLG_2025x3000.jpg
        # Sanitize movie name for filesystem
        safe_movie_name = re.sub(r'[^\w\s-]', '', info['movie_name']).strip().replace(' ', '_').lower()
        
        filename = f"{info['base_name']}_{selected_size.upper()}_{selected_info['dimensions']}.jpg"
        
        save_path = os.path.join(
            output_dir,
            info['year'],
            safe_movie_name,
            filename
        )
        
        # Download (with duplicate detection)
        success, already_existed = self.download_image(download_url, save_path, skip_if_exists=skip_existing)
        return success, already_existed


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='IMP Awards Poster Downloader - Download high-resolution movie posters',
        epilog='If no arguments provided, interactive menu will be shown.'
    )
    parser.add_argument('--latest', action='store_true',
                        help='Download all posters from the recent additions page')
    parser.add_argument('--year', type=int, metavar='YEAR',
                        help='Download all posters for a specific year (e.g., --year=2024)')
    parser.add_argument('--genre', action='append', metavar='GENRE',
                        help='Filter by genre (can be used multiple times for AND logic, e.g., --genre=animation --genre=comedy)')
    parser.add_argument('--pages', type=int, metavar='N',
                        help='Number of recent pages to process (use with --latest, e.g., --latest --pages=5)')
    parser.add_argument('--startfresh', action='store_true',
                        help='Clear downloads folder and start fresh')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("IMP Awards Poster Downloader")
    print("=" * 60)
    print()
    
    # Handle --startfresh flag
    skip_existing = not args.startfresh  # Disable duplicate checking if starting fresh
    
    if args.startfresh:
        import shutil
        downloads_dir = 'downloads'
        if os.path.exists(downloads_dir):
            print(f"🗑️  Clearing downloads folder...")
            shutil.rmtree(downloads_dir)
            print(f"✓ Downloads folder cleared\n")
        else:
            print(f"ℹ️  Downloads folder doesn't exist yet\n")
    
    downloader = PosterDownloader()
    
    # Check for command-line mode
    if args.latest:
        # Process recent additions via command line (auto-confirm for automation)
        num_pages = args.pages if args.pages else 1
        process_recent_additions(downloader, required_genres=args.genre, num_pages=num_pages, auto_confirm=True, skip_existing=skip_existing)
        return
    elif args.year:
        # Process specific year via command line (auto-confirm for automation)
        process_year_posters(downloader, args.year, required_genres=args.genre, auto_confirm=True, skip_existing=skip_existing)
        return
    
    # Interactive menu mode
    print("What would you like to do?")
    print()
    print("1. Process recent additions (latest.html)")
    print("2. Download single poster (enter URL)")
    print("3. Download all posters for a specific year")
    print("4. Download all posters for a specific movie (coming soon)")
    print()
    
    choice = input("Enter choice (1-4): ").strip()
    print()
    
    if choice == '1':
        # Process recent additions
        process_recent_additions(downloader)
    elif choice == '2':
        # Single poster download
        url = input("Enter poster page URL: ").strip()
        
        if not url:
            print("✗ No URL provided")
            sys.exit(1)
        
        if not url.startswith('http'):
            print("✗ URL must start with http:// or https://")
            sys.exit(1)
        
        print()
        try:
            success, already_existed = downloader.process_poster_page(url)
            if success:
                if already_existed:
                    print("\n✓ Already downloaded!")
                else:
                    print("\n✓ Download complete!")
            else:
                sys.exit(1)
        except Exception as e:
            print(f"\n✗ Error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    elif choice == '3':
        year = input("Enter year (e.g., 2024): ").strip()
        try:
            year_int = int(year)
            process_year_posters(downloader, year_int)
        except ValueError:
            print("✗ Invalid year")
            sys.exit(1)
    elif choice == '4':
        print("This feature is coming soon!")
        sys.exit(0)
    else:
        print("✗ Invalid choice")
        sys.exit(1)


def process_recent_additions(downloader, required_genres=None, num_pages=1, auto_confirm=False, skip_existing=True):
    """
    Process all posters from the recent additions page(s).
    
    Args:
        downloader: PosterDownloader instance
        required_genres: List of required genres (AND logic) or None
        num_pages: Number of recent pages to process (default: 1)
        auto_confirm: If True, skip confirmation prompt (for command-line mode)
        skip_existing: Whether to skip already downloaded files (default: True)
    """
    # Get list of recent posters
    poster_urls = downloader.get_recent_posters(num_pages=num_pages)
    
    if not poster_urls:
        print("✗ No posters found on recent additions page")
        return
    
    print(f"\nReady to process {len(poster_urls)} posters from recent additions")
    if required_genres:
        print(f"Genre filter: Movies must match ALL of: {', '.join(required_genres)}")
    print("Posters will be filtered by your genre blocklist settings")
    print()
    
    if not auto_confirm:
        response = input(f"Continue with batch processing? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            print("Cancelled by user")
            return
    
    print("\n" + "=" * 60)
    print("Starting batch processing...")
    print("=" * 60)
    
    stats = {
        'total': len(poster_urls),
        'downloaded': 0,
        'already_downloaded': 0,
        'skipped': 0,
        'blocked': 0,
        'errors': 0
    }
    
    for i, url in enumerate(poster_urls, 1):
        print(f"\n[{i}/{stats['total']}] Processing: {url}")
        print("-" * 60)
        
        try:
            success = downloader.process_poster_page(url, prompt_confirm=False, required_genres=required_genres)
            if success:
                stats['downloaded'] += 1
            else:
                stats['skipped'] += 1
        except KeyboardInterrupt:
            print("\n\n✗ Interrupted by user")
            break
        except Exception as e:
            print(f"✗ Error processing poster: {e}")
            stats['errors'] += 1
            continue
    
    # Final statistics
    print("\n" + "=" * 60)
    print("BATCH PROCESSING COMPLETE")
    print("=" * 60)
    print(f"Total posters:        {stats['total']}")
    print(f"New downloads:        {stats['downloaded']}")
    print(f"Already downloaded:   {stats['already_downloaded']}")
    print(f"Skipped:              {stats['skipped']}")
    print(f"Errors:               {stats['errors']}")
    print("=" * 60)


def process_year_posters(downloader, year, required_genres=None, auto_confirm=False, skip_existing=True):
    """
    Process all posters from a specific year.
    
    Args:
        downloader: PosterDownloader instance
        year: Year to process (int)
        required_genres: List of required genres (AND logic) or None
        auto_confirm: If True, skip confirmation prompt (for command-line mode)
        skip_existing: Whether to skip already downloaded files (default: True)
    """
    # Get list of posters for the year
    poster_urls = downloader.get_year_posters(year)
    
    if not poster_urls:
        print(f"✗ No posters found for year {year}")
        return
    
    print(f"\nReady to process {len(poster_urls)} posters from {year}")
    if required_genres:
        print(f"Genre filter: Movies must match ALL of: {', '.join(required_genres)}")
    print("Posters will be filtered by your genre blocklist settings")
    print()
    
    if not auto_confirm:
        response = input(f"Continue with batch processing? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            print("Cancelled by user")
            return
    
    print("\n" + "=" * 60)
    print(f"Starting batch processing for {year}...")
    print("=" * 60)
    
    stats = {
        'total': len(poster_urls),
        'downloaded': 0,
        'already_downloaded': 0,
        'skipped': 0,
        'blocked': 0,
        'errors': 0
    }
    
    for i, url in enumerate(poster_urls, 1):
        print(f"\n[{i}/{stats['total']}] Processing: {url}")
        print("-" * 60)
        
        try:
            success = downloader.process_poster_page(url, prompt_confirm=False, required_genres=required_genres)
            if success:
                stats['downloaded'] += 1
            else:
                stats['skipped'] += 1
        except KeyboardInterrupt:
            print("\n\n✗ Interrupted by user")
            break
        except Exception as e:
            print(f"✗ Error processing poster: {e}")
            stats['errors'] += 1
            continue
    
    # Final statistics
    print("\n" + "=" * 60)
    print(f"BATCH PROCESSING COMPLETE FOR {year}")
    print("=" * 60)
    print(f"Total posters:        {stats['total']}")
    print(f"New downloads:        {stats['downloaded']}")
    print(f"Already downloaded:   {stats['already_downloaded']}")
    print(f"Skipped:              {stats['skipped']}")
    print(f"Errors:               {stats['errors']}")
    print("=" * 60)


if __name__ == "__main__":
    main()

