"""
Helper utilities for Naukri automation.
"""

import json
from datetime import datetime
from pathlib import Path
from core.logger import get_logger

logger = get_logger(__name__)


class Helpers:
    """Common helper functions."""
    
    @staticmethod
    def extract_job_id(url):
        """Extract job ID from Naukri URL."""
        try:
            # Naukri URLs like: https://www.naukri.com/job-listings-xyz-123456...
            import re
            match = re.search(r'-(\d+)', url)
            if match:
                return match.group(1)
            return None
        except Exception as e:
            logger.error(f"Failed to extract job ID: {e}")
            return None
    
    @staticmethod
    def sanitize_filename(filename):
        """Sanitize filename for file operations."""
        invalid_chars = r'[<>:"/\\|?*]'
        import re
        return re.sub(invalid_chars, '_', filename)
    
    @staticmethod
    def save_json(data, filepath):
        """Save data to JSON file."""
        try:
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
            logger.info(f"Data saved to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to save JSON: {e}")
            return False
    
    @staticmethod
    def load_json(filepath):
        """Load data from JSON file."""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"File not found: {filepath}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {filepath}: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to load JSON: {e}")
            return None
    
    @staticmethod
    def get_timestamp():
        """Get current timestamp as ISO string."""
        return datetime.now().isoformat()
    
    @staticmethod
    def get_date_str():
        """Get current date as YYYY-MM-DD."""
        return datetime.now().strftime("%Y-%m-%d")
    
    @staticmethod
    def format_duration(seconds):
        """Format seconds to readable duration."""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours}h {minutes}m {secs}s"
        elif minutes > 0:
            return f"{minutes}m {secs}s"
        else:
            return f"{secs}s"
    
    @staticmethod
    def extract_text(element):
        """Extract text from Selenium element safely."""
        try:
            return element.text.strip()
        except:
            return ""
    
    @staticmethod
    def retry_operation(func, max_retries=3, backoff_factor=2):
        """Retry operation with exponential backoff."""
        import time
        
        for attempt in range(max_retries):
            try:
                return func()
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = backoff_factor ** attempt
                    logger.warning(f"Attempt {attempt + 1} failed, retrying in {wait_time}s: {e}")
                    time.sleep(wait_time)
                else:
                    logger.error(f"All {max_retries} attempts failed")
                    raise


# Create singleton
helpers = Helpers()

def get_helpers():
    """Get helpers instance."""
    return helpers
