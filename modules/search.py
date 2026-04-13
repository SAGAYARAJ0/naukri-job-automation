"""
Job search module for Naukri automation.
Handles job search, extraction, and pagination.
"""

import time
import urllib.parse
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from core.logger import get_logger
from core.config_manager import get_config
from core.exceptions import SearchException
from utils.human_behavior import get_human_behavior
from utils.helpers import get_helpers

logger = get_logger(__name__)
config = get_config()
behavior = get_human_behavior()
helpers = get_helpers()


class SearchModule:
    """Handles job search on Naukri."""
    
    def __init__(self, driver):
        """Initialize search module."""
        self.driver = driver
        self.base_url = "https://www.naukri.com/search"
        self.job_listings = []
        self._current_selector = (By.XPATH, "//div[contains(@class, 'jobTuple')]")  # Default selector
    
    def search_jobs(self, keywords, location, experience, max_pages=None):
        """
        Search for jobs on Naukri.
        
        Args:
            keywords: List of job keywords
            location: Job location
            experience: Years of experience
            max_pages: Maximum pages to parse
        
        Returns:
            List of job listings
        """
        logger.info(f"Starting job search: {keywords}, {location}, {experience} years")
        
        try:
            max_pages = max_pages or config.get('search.max_pages')
            self.job_listings = []
            
            search_url = self._build_search_url(keywords, location, experience)
            logger.info(f"Search URL: {search_url}")
            
            page = 1
            while page <= max_pages:
                try:
                    logger.info(f"Parsing page {page}")
                    
                    paginated_url = f"{search_url}&pageNo={page}"
                    self.driver.get(paginated_url)
                    
                    # Wait for job cards
                    time.sleep(3)
                    self._wait_for_job_cards()
                    
                    # Human-like browsing
                    behavior.random_delay(2, 4)
                    behavior.scroll_page(self.driver, pause=2)
                    
                    # Extract jobs
                    extracted = self._extract_job_listings()
                    logger.info(f"Found {extracted} jobs on page {page}")
                    
                    if extracted == 0:
                        logger.info("No more jobs found, stopping pagination")
                        break
                    
                    # Check for next page
                    if not self._has_next_page():
                        logger.info("Last page reached")
                        break
                    
                    behavior.random_delay(3, 6)
                    page += 1
                
                except StaleElementReferenceException:
                    logger.warning("Stale element, retrying page")
                    continue
                except TimeoutException:
                    logger.warning("Page load timeout, assuming end of results")
                    break
                except Exception as e:
                    logger.error(f"Error on page {page}: {e}")
                    break
            
            logger.info(f"Search complete: {len(self.job_listings)} total jobs found")
            return self.job_listings
        
        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise SearchException(f"Job search failed: {e}")
    
    def _build_search_url(self, keywords, location, experience):
        """Build Naukri search URL."""
        try:
            params = {
                'query': ' '.join(keywords) if isinstance(keywords, list) else keywords,
                'location': location,
                'experience': experience
            }
            
            query_string = urllib.parse.urlencode(params)
            url = f"{self.base_url}?{query_string}"
            
            return url
        except Exception as e:
            logger.error(f"Failed to build search URL: {e}")
            raise SearchException(f"URL building failed: {e}")
    
    def _wait_for_job_cards(self, timeout=15):
        """Wait for job cards to load."""
        logger.debug("Waiting for job cards to load")
        
        try:
            import selenium.webdriver.support.expected_conditions as EC
            from selenium.webdriver.support.ui import WebDriverWait
            
            wait = WebDriverWait(self.driver, timeout)
            
            # Try multiple selectors in order
            selectors_to_try = [
                (By.XPATH, "//div[contains(@class, 'jobTuple')]"),  # Original
                (By.CSS_SELECTOR, "div.jobTuple"),  # CSS version
                (By.XPATH, "//article[contains(@class, 'jobCard')]"),  # Alternative
                (By.CSS_SELECTOR, "article"),  # Generic article
                (By.XPATH, "//div[@itemtype]"),  # Microdata format
            ]
            
            last_error = None
            for selector_type, selector in selectors_to_try:
                try:
                    selector_name = selector_type.name if hasattr(selector_type, 'name') else str(selector_type)
                    logger.debug(f"Trying selector: {selector_name} = {selector}")
                    wait.until(EC.presence_of_all_elements_located((selector_type, selector)))
                    logger.debug(f"Job cards found using: {selector}")
                    self._current_selector = (selector_type, selector)
                    return
                except TimeoutException as e:
                    last_error = e
                    continue
            
            logger.warning(f"Job cards did not load with any selector")
            if last_error:
                raise last_error
        except TimeoutException:
            logger.warning("Job cards did not load within timeout")
            raise
    
    def _extract_job_listings(self):
        """Extract job listings from page."""
        logger.debug("Extracting job listings")
        
        try:
            # Use the selector that worked, or fallback to original
            selector_type, selector = getattr(self, '_current_selector', (By.XPATH, "//div[contains(@class, 'jobTuple')]"))
            
            job_elements = self.driver.find_elements(selector_type, selector)
            
            if len(job_elements) == 0:
                logger.warning(f"No job elements found with {selector}")
                return 0
            
            extracted_count = 0
            for job_element in job_elements:
                try:
                    job_data = self._parse_job_element(job_element)
                    if job_data:
                        self.job_listings.append(job_data)
                        extracted_count += 1
                except StaleElementReferenceException:
                    logger.debug("Stale element in job extraction")
                    continue
                except Exception as e:
                    logger.debug(f"Failed to parse job element: {e}")
                    continue
            
            logger.debug(f"Extracted {extracted_count} jobs")
            return extracted_count
        
        except Exception as e:
            logger.error(f"Failed to extract job listings: {e}")
            return 0
    
    def _parse_job_element(self, element):
        """Parse individual job element."""
        try:
            # Extract job details
            job_id = self._extract_text(element, "//@data-id") or ""
            title = self._extract_text(element, ".//a[@class='jobTitle']")
            company = self._extract_text(element, ".//span[contains(@class, 'companyName')]")
            location = self._extract_text(element, ".//span[contains(@class, 'locWc')]")
            
            # Get job URL
            job_link = element.find_element(By.XPATH, ".//a[@class='jobTitle']")
            job_url = job_link.get_attribute('href')
            
            if not title or not job_url:
                return None
            
            job_data = {
                'job_id': job_id,
                'title': title,
                'company': company,
                'location': location,
                'url': job_url,
                'found_at': helpers.get_timestamp()
            }
            
            logger.debug(f"Parsed job: {title} at {company}")
            return job_data
        
        except Exception as e:
            logger.debug(f"Error parsing job element: {e}")
            return None
    
    def _extract_text(self, element, xpath_or_selector):
        """Extract text from element."""
        try:
            if xpath_or_selector.startswith("."):
                sub_element = element.find_element(By.XPATH, xpath_or_selector)
            else:
                sub_element = element.find_element(By.XPATH, xpath_or_selector)
            
            return sub_element.text.strip() if sub_element else ""
        except:
            return ""
    
    def _has_next_page(self):
        """Check if next page button exists and is enabled."""
        try:
            next_button = self.driver.find_element(By.XPATH, "//a[@rel='next']")
            return next_button is not None
        except:
            return False
    
    def filter_jobs(self, filter_module, filter_rules):
        """Filter extracted jobs using filter module."""
        logger.info(f"Filtering {len(self.job_listings)} jobs")
        
        filtered = []
        for job in self.job_listings:
            try:
                # Get job description if needed
                result = filter_module.filter_job(job, filter_rules)
                if result['decision']:
                    filtered.append({**job, 'filter_score': result['score']})
            except Exception as e:
                logger.debug(f"Filter error for {job.get('title')}: {e}")
                continue
        
        logger.info(f"Filtered to {len(filtered)} jobs")
        return filtered


# Singleton instance
search_module = None

def get_search_module(driver):
    """Get search module instance."""
    global search_module
    if search_module is None:
        search_module = SearchModule(driver)
    return search_module
