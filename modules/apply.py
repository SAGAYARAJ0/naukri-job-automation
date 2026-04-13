"""
Job application module for Naukri automation.
Handles applying to jobs and managing application status.
"""

import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from core.logger import get_logger
from core.config_manager import get_config
from core.exceptions import ApplyException, AlreadyAppliedException, ExternalRedirectException
from utils.human_behavior import get_human_behavior
from utils.helpers import get_helpers

logger = get_logger(__name__)
config = get_config()
behavior = get_human_behavior()
helpers = get_helpers()


class ApplyModule:
    """Handles job applications on Naukri."""
    
    def __init__(self, driver, storage_module):
        """Initialize apply module."""
        self.driver = driver
        self.storage = storage_module
        self.max_retries = config.get('automation.max_retries', 3)
    
    def apply_to_job(self, job_data, retry_count=None):
        """
        Apply to a job.
        
        Args:
            job_data: Job dictionary with URL
            retry_count: Number of retries
        
        Returns:
            {status, message, timestamp}
        """
        job_url = job_data.get('url')
        job_id = helpers.extract_job_id(job_url)
        
        logger.info(f"Attempting to apply to job: {job_data.get('title')}")
        
        retry_count = retry_count or self.max_retries
        
        for attempt in range(retry_count):
            try:
                # Check if already applied
                if self.storage.is_already_applied(job_id):
                    logger.info(f"Already applied to job {job_id}")
                    return {
                        'status': 'already_applied',
                        'message': 'Already applied to this job',
                        'timestamp': helpers.get_timestamp()
                    }
                
                # Navigate to job
                logger.debug(f"Navigating to {job_url}")
                self.driver.get(job_url)
                time.sleep(3)
                
                # Find apply button
                apply_button = self._find_apply_button()
                if not apply_button:
                    logger.error("Apply button not found")
                    return {
                        'status': 'failed',
                        'message': 'Apply button not found',
                        'timestamp': helpers.get_timestamp()
                    }
                
                # Click apply
                behavior.scroll_to_element(self.driver, apply_button)
                behavior.random_delay(1, 2)
                behavior.click_with_offset(self.driver, apply_button)
                
                logger.debug("Apply button clicked")
                time.sleep(2)
                
                # Check for external redirect
                if self._check_external_redirect(job_url):
                    logger.warning("External redirect detected")
                    return {
                        'status': 'external',
                        'message': 'Job redirect to external site',
                        'timestamp': helpers.get_timestamp()
                    }
                
                # Verify application
                if self._verify_application():
                    # Save to storage
                    self.storage.save_applied_job(
                        job_id, 
                        job_data.get('title'),
                        job_url,
                        'success'
                    )
                    
                    logger.info(f"Successfully applied to job {job_id}")
                    return {
                        'status': 'success',
                        'message': 'Application submitted successfully',
                        'timestamp': helpers.get_timestamp()
                    }
                
                else:
                    logger.warning(f"Application verification failed, attempt {attempt + 1}/{retry_count}")
                    if attempt < retry_count - 1:
                        behavior.random_delay(5, 10)
                        continue
                    else:
                        return {
                            'status': 'failed',
                            'message': 'Application verification failed after retries',
                            'timestamp': helpers.get_timestamp()
                        }
            
            except AlreadyAppliedException:
                return {
                    'status': 'already_applied',
                    'message': 'Already applied to this job',
                    'timestamp': helpers.get_timestamp()
                }
            
            except ExternalRedirectException:
                return {
                    'status': 'external',
                    'message': 'Job redirects to external site',
                    'timestamp': helpers.get_timestamp()
                }
            
            except TimeoutException:
                logger.warning(f"Timeout on attempt {attempt + 1}/{retry_count}")
                if attempt < retry_count - 1:
                    behavior.random_delay(5, 10)
                    continue
            
            except Exception as e:
                logger.error(f"Error on attempt {attempt + 1}: {e}")
                if attempt < retry_count - 1:
                    behavior.random_delay(5, 10)
                    continue
        
        return {
            'status': 'failed',
            'message': f'Failed after {retry_count} attempts',
            'timestamp': helpers.get_timestamp()
        }
    
    def _find_apply_button(self):
        """Find and return apply button."""
        try:
            selectors = [
                "//button[contains(text(), 'Apply')]",
                "//a[contains(text(), 'Apply')]",
                "//button[@data-testid='applyButton']",
                "//button[contains(@class, 'apply')]"
            ]
            
            for selector in selectors:
                try:
                    element = self.driver.find_element(By.XPATH, selector)
                    if element and element.is_displayed():
                        logger.debug(f"Apply button found with selector: {selector}")
                        return element
                except:
                    continue
            
            logger.debug("No apply button found")
            return None
        
        except Exception as e:
            logger.error(f"Error finding apply button: {e}")
            return None
    
    def _check_external_redirect(self, original_url):
        """Check if page redirected to external site."""
        try:
            current_url = self.driver.current_url
            
            # If URL changed significantly, might be external
            if 'naukri.com' in original_url and 'naukri.com' not in current_url:
                logger.warning(f"Redirect detected: {original_url} -> {current_url}")
                raise ExternalRedirectException(f"External redirect: {current_url}")
            
            return False
        
        except ExternalRedirectException:
            raise
        except Exception as e:
            logger.warning(f"Redirect check error: {e}")
            return False
    
    def _verify_application(self):
        """Verify if application was successful."""
        try:
            time.sleep(2)
            
            # Look for success message
            success_indicators = [
                "//div[contains(text(), 'Applied')]",
                "//div[contains(text(), 'applied')]",
                "//span[contains(text(), 'Applied')]",
                "//div[contains(text(), 'successfully')]"
            ]
            
            for indicator in success_indicators:
                try:
                    element = self.driver.find_element(By.XPATH, indicator)
                    if element:
                        logger.info("Success indicator found")
                        return True
                except:
                    continue
            
            # Alternative: Check if apply button still exists and is enabled
            apply_button = self._find_apply_button()
            if not apply_button:
                logger.info("Apply button no longer visible, assuming success")
                return True
            
            logger.warning("Could not verify application success")
            return False
        
        except Exception as e:
            logger.warning(f"Verification error: {e}")
            return False


# Singleton instance
apply_module = None

def get_apply_module(driver, storage_module):
    """Get apply module instance."""
    global apply_module
    if apply_module is None:
        apply_module = ApplyModule(driver, storage_module)
    return apply_module
