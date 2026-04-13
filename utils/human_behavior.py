"""
Human behavior simulation to avoid bot detection.
"""

import time
import random
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from core.config_manager import get_config
from core.logger import get_logger

logger = get_logger(__name__)


class HumanBehavior:
    """Simulates human-like behavior to avoid bot detection."""
    
    def __init__(self):
        """Initialize with config."""
        self.config = get_config()
        self.min_delay = self.config.get('behavior.min_delay')
        self.max_delay = self.config.get('behavior.max_delay')
        self.typing_speed = self.config.get('behavior.typing_speed')
        self.scroll_pause = self.config.get('behavior.scroll_pause')
        self.scroll_amount = self.config.get('behavior.scroll_amount')
    
    def random_delay(self, min_delay=None, max_delay=None):
        """Sleep for random duration."""
        min_delay = min_delay or self.min_delay
        max_delay = max_delay or self.max_delay
        
        delay = random.uniform(min_delay, max_delay)
        logger.debug(f"Random delay: {delay:.2f}s")
        time.sleep(delay)
    
    def type_text_slowly(self, element, text):
        """Type text character by character with human-like speed."""
        logger.debug(f"Typing text slowly: {text[:20]}...")
        
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(self.typing_speed * 0.5, self.typing_speed * 1.5))
    
    def scroll_page(self, driver, direction="down", pause=None):
        """Scroll page like human."""
        pause = pause or self.scroll_pause
        
        logger.debug(f"Scrolling {direction}")
        
        if direction.lower() == "down":
            driver.execute_script(f"window.scrollBy(0, {self.scroll_amount * 100});")
        elif direction.lower() == "up":
            driver.execute_script(f"window.scrollBy(0, -{self.scroll_amount * 100});")
        
        time.sleep(random.uniform(pause * 0.5, pause * 1.5))
    
    def scroll_to_element(self, driver, element):
        """Scroll to element smoothly."""
        logger.debug("Scrolling to element")
        
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(random.uniform(1, 2))
    
    def click_with_offset(self, driver, element):
        """Click element with realistic mouse movement."""
        logger.debug("Clicking element with offset")
        
        actions = ActionChains(driver)
        # Move to element with slight offset
        x_offset = random.randint(-5, 10)
        y_offset = random.randint(-5, 10)
        
        actions.move_to_element_with_offset(element, x_offset, y_offset)
        self.random_delay(0.2, 0.5)
        actions.click()
        actions.perform()
    
    def move_mouse_randomly(self, driver):
        """Move mouse to random position on page."""
        logger.debug("Moving mouse randomly")
        
        actions = ActionChains(driver)
        x = random.randint(100, 800)
        y = random.randint(100, 600)
        
        actions.move_by_offset(x, y)
        actions.perform()
    
    def pause_for_captcha(self, timeout=None):
        """Pause execution for manual CAPTCHA solving."""
        timeout = timeout or self.config.get('automation.captcha_timeout')
        
        logger.warning("CAPTCHA detected! Please solve it manually.")
        logger.info(f"Waiting for {timeout}s for CAPTCHA to be solved...")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            time.sleep(5)
            elapsed = int(time.time() - start_time)
            remaining = timeout - elapsed
            logger.info(f"Waiting... {remaining}s remaining")
        
        logger.info("CAPTCHA timeout reached")
    
    def natural_mouse_movement(self, driver, target_x, target_y, steps=10):
        """Move mouse naturally to target using bezier curve."""
        logger.debug(f"Natural mouse movement to ({target_x}, {target_y})")
        
        actions = ActionChains(driver)
        
        for i in range(steps):
            x = target_x * (i / steps)
            y = target_y * (i / steps)
            actions.move_by_offset(x, y)
            time.sleep(0.05)
        
        actions.perform()


# Singleton instance
human_behavior = HumanBehavior()

def get_human_behavior():
    """Get human behavior instance."""
    return human_behavior
