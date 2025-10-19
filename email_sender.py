#!/usr/bin/env python3
"""
Email notification system for IMP Awards Poster Downloader
Sends daily digest emails with poster thumbnails and links to full-size images

Version: 1.3.0
"""

import os
import smtplib
import json
import time
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image
import io
from typing import List, Dict, Optional, Tuple, Any

# Load environment variables
load_dotenv()

# ============================================================
# CONFIGURATION CONSTANTS
# ============================================================

# Email tracking file
EMAIL_TRACKING_FILE = 'email_tracking.json'

# Email configuration
DEFAULT_SMTP_SERVER = 'smtp.gmail.com'
DEFAULT_SMTP_PORT = 587
DEFAULT_MAX_SIZE_MB = 40

# Image settings
THUMBNAIL_MAX_WIDTH = 800
JPEG_QUALITY = 85

# Retry settings
MAX_EMAIL_RETRIES = 3
EMAIL_RETRY_DELAY = 5  # seconds

# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================
# EMAIL SENDER CLASS
# ============================================================

class EmailSender:
    """Handles email notifications for newly downloaded posters."""
    
    def __init__(self):
        """Initialize email sender with configuration from environment variables."""
        self.smtp_server = os.getenv('SMTP_SERVER', DEFAULT_SMTP_SERVER)
        self.smtp_port = int(os.getenv('SMTP_PORT', str(DEFAULT_SMTP_PORT)))
        self.username = os.getenv('SMTP_USERNAME', '')
        self.password = os.getenv('SMTP_PASSWORD', '')
        self.email_from = os.getenv('EMAIL_FROM', self.username)
        self.email_to = os.getenv('EMAIL_TO', self.username)
        self.max_size_mb = int(os.getenv('EMAIL_MAX_SIZE_MB', str(DEFAULT_MAX_SIZE_MB)))
        
        if not self.username or not self.password:
            raise ValueError(
                "Email credentials not configured. Please set SMTP_USERNAME and SMTP_PASSWORD in .env file.\n"
                "See EMAIL_SETUP.md for detailed setup instructions."
            )
    
    def load_email_tracking(self) -> Dict[str, Any]:
        """
        Load tracking data of which posters have been emailed.
        
        Returns:
            Dictionary containing sent_posters list and last_sent timestamp
        """
        if os.path.exists(EMAIL_TRACKING_FILE):
            try:
                with open(EMAIL_TRACKING_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Could not load email tracking: {e}")
        
        return {'sent_posters': [], 'last_sent': None}
    
    def save_email_tracking(self, tracking_data: Dict[str, Any]) -> None:
        """
        Save tracking data of sent posters.
        
        Args:
            tracking_data: Dictionary with sent_posters and last_sent
        """
        try:
            with open(EMAIL_TRACKING_FILE, 'w') as f:
                json.dump(tracking_data, f, indent=2)
        except Exception as e:
            logger.warning(f"Could not save email tracking: {e}")
    
    def mark_posters_as_sent(self, poster_files: List[str]) -> None:
        """
        Mark posters as sent in tracking file.
        
        Args:
            poster_files: List of poster file paths that were sent
        """
        tracking = self.load_email_tracking()
        tracking['sent_posters'].extend(poster_files)
        tracking['last_sent'] = datetime.now().isoformat()
        self.save_email_tracking(tracking)
    
    def get_unsent_posters(self, all_posters: List[str]) -> List[str]:
        """
        Filter out posters that have already been emailed.
        
        Args:
            all_posters: List of poster file paths
            
        Returns:
            List of unsent poster file paths
        """
        tracking = self.load_email_tracking()
        sent_set = set(tracking['sent_posters'])
        return [p for p in all_posters if p not in sent_set]
    
    def create_thumbnail(self, image_path: str, max_width: int = THUMBNAIL_MAX_WIDTH) -> Optional[bytes]:
        """
        Create thumbnail from image file.
        
        Args:
            image_path: Path to original image
            max_width: Maximum width for thumbnail (maintains aspect ratio)
            
        Returns:
            Bytes of thumbnail image (JPEG) or None if failed
        """
        try:
            with Image.open(image_path) as img:
                # Calculate new dimensions maintaining aspect ratio
                width, height = img.size
                if width > max_width:
                    new_width = max_width
                    new_height = int((max_width / width) * height)
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Convert to RGB if necessary (for JPEG)
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                # Save to bytes
                thumb_bytes = io.BytesIO()
                img.save(thumb_bytes, format='JPEG', quality=JPEG_QUALITY)
                thumb_bytes.seek(0)
                return thumb_bytes.read()
        except Exception as e:
            logger.warning(f"  Warning: Could not create thumbnail for {image_path}: {e}")
            return None
    
    def extract_poster_metadata(self, filename: str) -> Dict[str, str]:
        """
        Extract metadata from poster filename.
        
        Format: 2025_tron_ares_XXLG_2025x3000.jpg
        
        Args:
            filename: Poster filename
            
        Returns:
            Dictionary with year, movie_name, resolution, dimensions, poster_number
        """
        # Remove extension and split
        name = Path(filename).stem
        parts = name.split('_')
        
        if len(parts) < 3:
            return {
                'year': 'Unknown',
                'movie_name': name,
                'resolution': 'Unknown',
                'dimensions': '',
                'poster_number': ''
            }
        
        year = parts[0]
        dimensions = parts[-1]  # Last part is dimensions
        resolution = parts[-2]  # Second to last is resolution
        
        # Everything in between is the movie name
        movie_name_parts = parts[1:-2]
        movie_name = ' '.join(movie_name_parts).replace('_', ' ').title()
        
        # Extract poster number if it exists (e.g., ver2, ver12)
        poster_number = ''
        for part in reversed(movie_name_parts):
            if part.startswith('ver'):
                poster_number = part.replace('ver', '#')
                break
        
        return {
            'year': year,
            'movie_name': movie_name,
            'resolution': resolution,
            'dimensions': dimensions,
            'poster_number': poster_number if poster_number else '#1'
        }
    
    def construct_source_url(self, filename: str) -> Optional[str]:
        """
        Construct the IMP Awards source URL for the full-size poster.
        
        Format: http://www.impawards.com/2025/posters/tron_ares_xxlg.jpg
        
        Args:
            filename: Poster filename
            
        Returns:
            Full URL to source image or None
        """
        name = Path(filename).stem
        parts = name.split('_')
        
        if len(parts) < 3:
            return None
        
        year = parts[0]
        # Reconstruct the base name with resolution suffix
        # Remove year prefix and dimensions suffix
        middle_parts = parts[1:-1]  # Everything except year and dimensions
        base_name = '_'.join(middle_parts).lower()
        
        return f"http://www.impawards.com/{year}/posters/{base_name}.jpg"
    
    def batch_posters_by_size(self, poster_files: List[str]) -> List[List[str]]:
        """
        Split posters into batches that don't exceed max email size.
        
        Args:
            poster_files: List of poster file paths
            
        Returns:
            List of batches, where each batch is a list of file paths
        """
        batches = []
        current_batch = []
        current_size = 0
        max_size_bytes = self.max_size_mb * 1024 * 1024
        
        for poster_file in poster_files:
            if not os.path.exists(poster_file):
                logger.warning(f"  Poster file not found, skipping: {poster_file}")
                continue
                
            file_size = os.path.getsize(poster_file)
            # Estimate thumbnail size (roughly 10-20% of original)
            estimated_thumb_size = file_size * 0.15
            
            # If adding this poster would exceed limit, start new batch
            if current_size + estimated_thumb_size > max_size_bytes and current_batch:
                batches.append(current_batch)
                current_batch = [poster_file]
                current_size = estimated_thumb_size
            else:
                current_batch.append(poster_file)
                current_size += estimated_thumb_size
        
        # Add the last batch
        if current_batch:
            batches.append(current_batch)
        
        return batches
    
    def create_email_html(self, poster_files: List[str], batch_num: int = 1, 
                         total_batches: int = 1) -> str:
        """
        Create HTML email body with thumbnails and metadata.
        
        Args:
            poster_files: List of poster file paths to include
            batch_num: Current batch number (for subject line)
            total_batches: Total number of batches
            
        Returns:
            HTML string for email body
        """
        html_parts = ['<html><body style="font-family: Arial, sans-serif;">']
        
        # Header
        if total_batches > 1:
            html_parts.append(f'<h2>IMP Awards Daily Update ({batch_num} of {total_batches})</h2>')
        else:
            html_parts.append('<h2>IMP Awards Daily Update</h2>')
        
        html_parts.append(f'<p style="color: #666;">Date: {datetime.now().strftime("%B %d, %Y")}</p>')
        html_parts.append(f'<p style="color: #666;">Posters in this email: {len(poster_files)}</p>')
        html_parts.append('<hr style="border: 1px solid #ddd; margin: 20px 0;">')
        
        # Add each poster
        for i, poster_file in enumerate(poster_files):
            metadata = self.extract_poster_metadata(poster_file)
            source_url = self.construct_source_url(poster_file)
            
            # Movie title and year
            html_parts.append(f'<h3 style="margin-bottom: 5px;">{metadata["movie_name"]} ({metadata["year"]})</h3>')
            
            # Poster number
            html_parts.append(f'<p style="margin-top: 5px; color: #666;">Poster {metadata["poster_number"]}</p>')
            
            # Thumbnail with link to full-size source
            cid = f'poster{i}'
            if source_url:
                html_parts.append(f'<a href="{source_url}" target="_blank">')
                html_parts.append(f'<img src="cid:{cid}" style="max-width: 600px; height: auto; display: block; margin: 10px 0;" alt="{metadata["movie_name"]}">')
                html_parts.append('</a>')
                html_parts.append(f'<p style="font-size: 12px; color: #999;">Click image to view full size ({metadata["dimensions"]})</p>')
            else:
                html_parts.append(f'<img src="cid:{cid}" style="max-width: 600px; height: auto; display: block; margin: 10px 0;" alt="{metadata["movie_name"]}">')
            
            # Separator
            html_parts.append('<br><hr style="border: 1px solid #ddd; margin: 20px 0;"><br>')
        
        # Footer
        html_parts.append('<p style="color: #999; font-size: 12px; margin-top: 30px;">This is an automated email from IMP Awards Poster Downloader</p>')
        html_parts.append('</body></html>')
        
        return '\n'.join(html_parts)
    
    def send_email_batch(self, poster_files: List[str], batch_num: int = 1, 
                        total_batches: int = 1, subject_prefix: str = "") -> bool:
        """
        Send one email with a batch of posters, with retry logic.
        
        Args:
            poster_files: List of poster file paths to include
            batch_num: Current batch number (for subject line)
            total_batches: Total number of batches
            
        Returns:
            True if sent successfully, False otherwise
        """
        for attempt in range(1, MAX_EMAIL_RETRIES + 1):
            try:
                # Create message
                msg = MIMEMultipart('related')
                
                # Subject
                date_str = datetime.now().strftime("%B %d, %Y")
                poster_count = len(poster_files)
                count_token = f"[{poster_count}]"
                if total_batches > 1:
                    subject = f"{count_token} • IMP Update {date_str} ({batch_num} of {total_batches})"
                else:
                    subject = f"{count_token} • IMP Update {date_str}"
                if subject_prefix:
                    subject = f"{subject_prefix.strip()} {subject}".strip()
                
                msg['Subject'] = subject
                msg['From'] = self.email_from
                msg['To'] = self.email_to
                
                # Create HTML body
                html_body = self.create_email_html(poster_files, batch_num, total_batches)
                msg.attach(MIMEText(html_body, 'html'))
                
                # Attach thumbnails as inline images
                for i, poster_file in enumerate(poster_files):
                    thumbnail_data = self.create_thumbnail(poster_file)
                    if thumbnail_data:
                        image = MIMEImage(thumbnail_data)
                        image.add_header('Content-ID', f'<poster{i}>')
                        image.add_header('Content-Disposition', 'inline')
                        msg.attach(image)
                
                # Send email
                logger.info(f"\nSending email {batch_num}/{total_batches}...")
                logger.info(f"  To: {self.email_to}")
                logger.info(f"  Subject: {subject}")
                
                with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=30) as server:
                    server.starttls()
                    server.login(self.username, self.password)
                    server.send_message(msg)
                
                logger.info(f"  ✓ Email sent successfully!")
                return True
                
            except Exception as e:
                if attempt < MAX_EMAIL_RETRIES:
                    wait_time = EMAIL_RETRY_DELAY * attempt
                    logger.warning(f"  ✗ Error sending email (attempt {attempt}/{MAX_EMAIL_RETRIES}): {e}")
                    logger.info(f"  Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"  ✗ Failed to send email after {MAX_EMAIL_RETRIES} attempts: {e}")
                    logger.error("  Troubleshooting:")
                    logger.error("  1. Check your email credentials in .env file")
                    logger.error("  2. For Gmail, use an App Password (not your regular password)")
                    logger.error("  3. Verify SMTP_SERVER and SMTP_PORT are correct")
                    logger.error("  4. Check your internet connection")
                    return False
        
        return False
    
    def send_poster_updates(self, poster_files: List[str], subject_prefix: str = "") -> int:
        """
        Send email updates for new posters with batching support.
        
        Args:
            poster_files: List of poster file paths
            
        Returns:
            Number of emails sent successfully
        """
        if not poster_files:
            logger.info("No new posters to email")
            return 0
        
        # Filter to only unsent posters
        unsent_posters = self.get_unsent_posters(poster_files)
        
        if not unsent_posters:
            logger.info(f"All {len(poster_files)} posters have already been emailed")
            return 0
        
        logger.info(f"\n{'='*60}")
        logger.info(f"PREPARING EMAIL UPDATE")
        logger.info(f"{'='*60}")
        logger.info(f"New posters to email: {len(unsent_posters)}")
        
        # Batch posters by size
        batches = self.batch_posters_by_size(unsent_posters)
        total_batches = len(batches)
        
        if total_batches > 1:
            logger.info(f"Posters will be sent in {total_batches} emails ({self.max_size_mb}MB limit per email)")
        
        # Send each batch
        emails_sent = 0
        for batch_num, batch in enumerate(batches, 1):
            if self.send_email_batch(batch, batch_num, total_batches, subject_prefix=subject_prefix):
                emails_sent += 1
                # Mark this batch as sent
                self.mark_posters_as_sent(batch)
            else:
                logger.warning(f"  Skipping remaining batches due to email failure")
                break
        
        logger.info(f"\n{'='*60}")
        logger.info(f"EMAIL UPDATE COMPLETE")
        logger.info(f"{'='*60}")
        logger.info(f"Emails sent: {emails_sent}/{total_batches}")
        logger.info(f"Posters delivered: {len(unsent_posters) if emails_sent == total_batches else 'Partial'}")
        logger.info(f"{'='*60}\n")
        
        return emails_sent


# ============================================================
# TEST FUNCTION
# ============================================================

def test_email_sender() -> None:
    """Test function to verify email configuration."""
    try:
        sender = EmailSender()
        logger.info(f"Email sender configured:")
        logger.info(f"  SMTP Server: {sender.smtp_server}:{sender.smtp_port}")
        logger.info(f"  From: {sender.email_from}")
        logger.info(f"  To: {sender.email_to}")
        logger.info(f"  Max size per email: {sender.max_size_mb}MB")
        logger.info(f"\n✓ Email sender ready!")
    except ValueError as e:
        logger.error(f"\n✗ Configuration error: {e}")
        logger.error("Please check your .env file and see EMAIL_SETUP.md for help.")
        return


if __name__ == "__main__":
    test_email_sender()
