"""
Configuration management for Naukri automation.
"""

import json
import os
from pathlib import Path
from core.exceptions import ConfigException
from core.logger import get_logger

logger = get_logger(__name__)


class ConfigManager:
    """Manages configuration from JSON files."""
    
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize configuration manager."""
        self.config_dir = Path(__file__).parent.parent / "config"
        self.config_file = self.config_dir / "config.json"
        self.filters_file = self.config_dir / "filters.json"
        
        if not self.config_file.exists():
            logger.warning(f"Config file not found at {self.config_file}")
            logger.info("Using default configuration")
            self._config = self._get_default_config()
        else:
            self._load_config()
    
    def _load_config(self):
        """Load configuration from JSON file."""
        try:
            with open(self.config_file, 'r') as f:
                self._config = json.load(f)
            logger.info("Configuration loaded successfully")
        except json.JSONDecodeError as e:
            raise ConfigException(f"Invalid JSON in config file: {e}")
        except Exception as e:
            raise ConfigException(f"Failed to load config: {e}")
    
    def _get_default_config(self):
        """Get default configuration."""
        return {
            "naukri": {
                "login_url": "https://www.naukri.com/",
                "email_selector": "input[id='usernameField']",
                "password_selector": "input[id='passwordField']",
                "login_button_selector": "button[id='loginButton']"
            },
            "automation": {
                "headless": False,
                "implicit_wait": 10,
                "explicit_wait": 15,
                "page_load_timeout": 20,
                "captcha_timeout": 300,
                "max_retries": 3,
                "backoff_factor": 2
            },
            "behavior": {
                "min_delay": 2,
                "max_delay": 5,
                "typing_speed": 0.1,
                "scroll_pause": 3,
                "scroll_amount": 3
            },
            "search": {
                "max_pages": 10,
                "results_per_page": 10
            },
            "filter": {
                "threshold": 70,
                "min_experience_gap": 2,
                "strict_mode": False
            },
            "storage": {
                "type": "json",
                "db_path": "data/jobs.db"
            }
        }
    
    def get(self, key, default=None):
        """Get config value by dot notation (e.g., 'naukri.login_url')."""
        keys = key.split('.')
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            if default is not None:
                return default
            raise ConfigException(f"Config key not found: {key}")
    
    def set(self, key, value):
        """Set config value by dot notation."""
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def get_all(self):
        """Get entire configuration."""
        return self._config
    
    def load_filters(self):
        """Load filter configuration."""
        try:
            if self.filters_file.exists():
                with open(self.filters_file, 'r') as f:
                    return json.load(f)
            else:
                logger.warning(f"Filters file not found at {self.filters_file}")
                return self._get_default_filters()
        except Exception as e:
            logger.error(f"Failed to load filters: {e}")
            return self._get_default_filters()
    
    def _get_default_filters(self):
        """Get default filter configuration."""
        return {
            "required_skills": ["Python", "JavaScript", "SQL"],
            "nice_to_have_skills": ["Docker", "Kubernetes", "AWS"],
            "red_flags": ["bias", "discrimination", "unpaid", "internship only"],
            "min_experience": 0,
            "max_experience": 10,
            "preferred_locations": ["Bangalore", "Mumbai", "Delhi"],
            "preferred_salary_range": [500000, 2000000],
            "filter_threshold": 70
        }
    
    def save_config(self):
        """Save current config to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self._config, f, indent=4)
            logger.info("Configuration saved successfully")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")


# Singleton instance
config_manager = ConfigManager()

def get_config():
    """Get config manager instance."""
    return config_manager
