"""
Input validators for Naukri automation.
"""

import re
from core.exceptions import ConfigException
from core.logger import get_logger

logger = get_logger(__name__)


class Validators:
    """Input validation utilities."""
    
    @staticmethod
    def validate_email(email):
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise ConfigException(f"Invalid email format: {email}")
        return True
    
    @staticmethod
    def validate_url(url):
        """Validate URL format."""
        pattern = r'^https?://'
        if not re.match(pattern, url):
            raise ConfigException(f"Invalid URL format: {url}")
        return True
    
    @staticmethod
    def validate_experience(years):
        """Validate years of experience."""
        try:
            exp = int(years)
            if exp < 0 or exp > 100:
                raise ValueError
            return True
        except:
            raise ConfigException(f"Invalid experience value: {years}")
    
    @staticmethod
    def validate_keywords(keywords):
        """Validate keywords list."""
        if not keywords or len(keywords) == 0:
            raise ConfigException("Keywords list is empty")
        if not all(isinstance(k, str) for k in keywords):
            raise ConfigException("All keywords must be strings")
        return True
    
    @staticmethod
    def validate_location(location):
        """Validate location string."""
        if not location or len(location.strip()) == 0:
            raise ConfigException("Location cannot be empty")
        return True
    
    @staticmethod
    def validate_job_url(url):
        """Validate Naukri job URL."""
        if 'naukri.com' not in url:
            logger.warning(f"URL may not be from Naukri: {url}")
        Validators.validate_url(url)
        return True


# Create singleton
validators = Validators()

def get_validators():
    """Get validators instance."""
    return validators
