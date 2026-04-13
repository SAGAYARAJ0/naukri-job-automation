"""
Login module for Naukri automation.
Handles authentication, CAPTCHA, and session management.
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from core.logger import get_logger
from core.config_manager import get_config
from core.exceptions import LoginException, CaptchaRequiredException, SessionExpiredException
from utils.human_behavior import get_human_behavior
from utils.helpers import get_helpers

logger = get_logger(__name__)
config = get_config()
behavior = get_human_behavior()
helpers = get_helpers()


class LoginModule:
    """Handles Naukri login, CAPTCHA, and session management."""
    
    def __init__(self, driver):
        """Initialize login module."""
        self.driver = driver
        self.login_url = config.get('naukri.login_url')
        self.cookies_file = "data/naukri_cookies.json"
    
    def login(self, email, password, use_saved_session=True):
        """
        Main login function.
        
        Args:
            email: User email
            password: User password
            use_saved_session: Try to use saved cookies first
        
        Returns:
            dict: {status, message, cookies}
        """
        logger.info("Starting login process")
        
        try:
            # Try using saved session
            if use_saved_session:
                if self._try_load_session():
                    logger.info("Successfully loaded saved session")
                    return {"status": "success", "message": "Loaded from saved session"}
            
            # Perform fresh login
            return self._perform_fresh_login(email, password)
        
        except CaptchaRequiredException as e:
            logger.warning(f"CAPTCHA required during login: {e}")
            return {"status": "captcha_required", "message": str(e)}
        
        except Exception as e:
            logger.error(f"Login failed: {e}")
            return {"status": "failed", "message": str(e)}
    
    def _perform_fresh_login(self, email, password):
        """Perform fresh login with credentials."""
        logger.info("Performing fresh login")
        
        # Navigate to login page
        self._navigate_to_login()
        
        # Enter credentials
        self._enter_credentials(email, password)
        
        # Check for CAPTCHA
        if self._check_captcha():
            behavior.pause_for_captcha()
        
        # Verify login success
        if not self._verify_login_success():
            raise LoginException("Login verification failed")
        
        # Save cookies
        cookies = self._save_cookies()
        
        logger.info("Login successful")
        return {"status": "success", "message": "Login successful", "cookies": cookies}
    
    def _navigate_to_login(self):
        """Navigate to Naukri login page/modal."""
        logger.info(f"Navigating to {self.login_url}")
        
        try:
            self.driver.get(self.login_url)
            time.sleep(2)
            
            # Try to find and click the login link to open modal
            try:
                logger.info("Looking for login link to open modal...")
                login_link = self.driver.find_element(By.LINK_TEXT, "Login")
                behavior.random_delay(0.5, 1.5)
                login_link.click()
                logger.info("Clicked login link")
                time.sleep(2)
            except NoSuchElementException:
                logger.info("No login link found, checking if login form already visible...")
                # Maybe the form is already visible or on direct URL
                pass
            
            logger.info("Login page/modal ready")
        except TimeoutException:
            raise LoginException("Login page load timeout")
    
    def _enter_credentials(self, email, password):
        """Enter email and password."""
        logger.info("Entering credentials")
        
        try:
            # Get email field
            email_selector = config.get('naukri.email_selector')
            email_field = self.driver.find_element(By.CSS_SELECTOR, email_selector)
            
            # Clear and enter email
            email_field.clear()
            behavior.type_text_slowly(email_field, email)
            logger.debug(f"Email entered: {email}")
            
            behavior.random_delay(1, 2)
            
            # Get password field
            password_selector = config.get('naukri.password_selector')
            password_field = self.driver.find_element(By.CSS_SELECTOR, password_selector)
            
            # Clear and enter password
            password_field.clear()
            behavior.type_text_slowly(password_field, password)
            logger.debug("Password entered")
            
            behavior.random_delay(1, 2)
            
            # Click login button
            login_button_selector = config.get('naukri.login_button_selector')
            login_button = self.driver.find_element(By.CSS_SELECTOR, login_button_selector)
            
            behavior.scroll_to_element(self.driver, login_button)
            behavior.random_delay(0.5, 1)
            behavior.click_with_offset(self.driver, login_button)
            
            logger.info("Login button clicked")
            behavior.random_delay(3, 5)
        
        except NoSuchElementException as e:
            raise LoginException(f"Login element not found: {e}")
        except Exception as e:
            raise LoginException(f"Failed to enter credentials: {e}")
    
    def _check_captcha(self):
        """Check if CAPTCHA appeared."""
        logger.debug("Checking for CAPTCHA")
        
        try:
            # Common CAPTCHA indicators
            captcha_indicators = [
                "//div[contains(text(), 'captcha')]",
                "//iframe[@title='reCAPTCHA']",
                "//div[@id='recaptcha']"
            ]
            
            for xpath in captcha_indicators:
                elements = self.driver.find_elements(By.XPATH, xpath)
                if elements:
                    logger.warning("CAPTCHA detected")
                    raise CaptchaRequiredException("CAPTCHA required")
            
            return False
        
        except CaptchaRequiredException:
            raise
        except:
            return False
    
    def _verify_login_success(self):
        """Verify if login was successful."""
        logger.info("Verifying login success")
        
        try:
            # Check for successful login indicators
            # Look for dashboard or profile elements
            time.sleep(3)
            
            current_url = self.driver.current_url
            logger.debug(f"Current URL: {current_url}")
            
            # Check if redirected away from login page
            if 'login' not in current_url:
                logger.info("Successfully logged in")
                return True
            
            # Try alternate verification
            try:
                profile_element = self.driver.find_element(By.XPATH, "//div[contains(@class, 'profile')]")
                if profile_element:
                    logger.info("Profile element found, login successful")
                    return True
            except:
                pass
            
            logger.error("Could not verify login success")
            return False
        
        except Exception as e:
            logger.error(f"Error verifying login: {e}")
            return False
    
    def _save_cookies(self):
        """Save session cookies."""
        logger.info("Saving cookies")
        
        try:
            import json
            cookies = self.driver.get_cookies()
            helpers.save_json(cookies, self.cookies_file)
            logger.info(f"Cookies saved: {len(cookies)} cookies")
            return cookies
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
            return []
    
    def _try_load_session(self):
        """Try to load session from saved cookies."""
        logger.info("Attempting to load saved session")
        
        try:
            cookies = helpers.load_json(self.cookies_file)
            if not cookies:
                return False
            
            # Navigate to Naukri first
            self.driver.get(self.login_url)
            time.sleep(2)
            
            # Add cookies
            for cookie in cookies:
                try:
                    self.driver.add_cookie(cookie)
                except Exception as e:
                    logger.debug(f"Failed to add cookie: {e}")
            
            # Refresh page
            self.driver.refresh()
            time.sleep(3)
            
            # Verify session is still valid
            if self._verify_login_success():
                logger.info("Session restored from cookies")
                return True
            else:
                logger.warning("Saved session is invalid")
                return False
        
        except Exception as e:
            logger.debug(f"Failed to load session: {e}")
            return False
    
    def logout(self):
        """Logout from Naukri."""
        logger.info("Logging out")
        
        try:
            self.driver.delete_all_cookies()
            logger.info("Logged out successfully")
            return True
        except Exception as e:
            logger.error(f"Logout failed: {e}")
            return False


# Singleton instance
login_module = None

def get_login_module(driver):
    """Get login module instance."""
    global login_module
    if login_module is None:
        login_module = LoginModule(driver)
    return login_module
