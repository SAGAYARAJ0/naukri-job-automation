"""
WebDriver management for Naukri automation.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from core.exceptions import DriverException
from core.config_manager import get_config
from core.logger import get_logger

logger = get_logger(__name__)


class DriverManager:
    """Manages Selenium WebDriver lifecycle."""
    
    _instance = None
    _driver = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DriverManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize driver manager."""
        self.config = get_config()
    
    def get_driver(self, use_headless=None):
        """Get or create WebDriver instance."""
        if self._driver is not None:
            logger.debug("Returning existing WebDriver instance")
            return self._driver
        
        try:
            headless = use_headless if use_headless is not None else self.config.get('automation.headless')
            logger.info(f"Creating Chrome WebDriver (headless={headless})")
            
            options = webdriver.ChromeOptions()
            
            if headless:
                options.add_argument('--headless')
            
            # Common options
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            
            self._driver = webdriver.Chrome(options=options)
            
            # Set timeouts
            implicit_wait = self.config.get('automation.implicit_wait')
            page_load_timeout = self.config.get('automation.page_load_timeout')
            
            self._driver.implicitly_wait(implicit_wait)
            self._driver.set_page_load_timeout(page_load_timeout)
            
            logger.info("WebDriver created successfully")
            return self._driver
        
        except Exception as e:
            logger.error(f"Failed to create WebDriver: {e}")
            raise DriverException(f"Failed to initialize WebDriver: {e}")
    
    def quit_driver(self):
        """Quit WebDriver gracefully."""
        if self._driver is not None:
            try:
                logger.info("Quitting WebDriver")
                self._driver.quit()
                self._driver = None
                logger.info("WebDriver quit successfully")
            except Exception as e:
                logger.error(f"Error quitting driver: {e}")
    
    def save_cookies(self, filepath):
        """Save cookies to file."""
        if self._driver is None:
            raise DriverException("No active driver")
        
        try:
            import json
            cookies = self._driver.get_cookies()
            with open(filepath, 'w') as f:
                json.dump(cookies, f)
            logger.info(f"Cookies saved to {filepath}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def load_cookies(self, filepath):
        """Load cookies from file."""
        if self._driver is None:
            raise DriverException("No active driver")
        
        try:
            import json
            with open(filepath, 'r') as f:
                cookies = json.load(f)
            for cookie in cookies:
                try:
                    self._driver.add_cookie(cookie)
                except Exception as e:
                    logger.warning(f"Failed to add cookie: {e}")
            logger.info(f"Cookies loaded from {filepath}")
        except Exception as e:
            logger.error(f"Failed to load cookies: {e}")
    
    def wait_for_element(self, by, value, timeout=None):
        """Wait for element to be present."""
        if self._driver is None:
            raise DriverException("No active driver")
        
        try:
            timeout = timeout or self.config.get('automation.explicit_wait')
            wait = WebDriverWait(self._driver, timeout)
            element = wait.until(lambda x: x.find_element(by, value))
            logger.debug(f"Element found: {by}={value}")
            return element
        except Exception as e:
            logger.error(f"Element not found: {by}={value}")
            raise DriverException(f"Element not found: {e}")
    
    def __del__(self):
        """Cleanup on object destruction."""
        self.quit_driver()


# Singleton instance
driver_manager = DriverManager()

def get_driver_manager():
    """Get driver manager instance."""
    return driver_manager
