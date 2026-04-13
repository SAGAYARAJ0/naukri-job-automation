#!/usr/bin/env python
"""
Find correct CSS selectors for Naukri job search results
"""

from selenium.webdriver.common.by import By
from core.driver_manager import get_driver_manager
from core.logger import get_logger
from modules.login import LoginModule
from core.config_manager import get_config
import time

logger = get_logger(__name__)
config = get_config()

print("\n" + "="*70)
print("NAUKRI JOB SEARCH SELECTOR FINDER")
print("="*70 + "\n")

try:
    # Get driver
    driver = get_driver_manager().get_driver()
    
    # Load cookies (assuming login already happened)
    from utils.helpers import get_helpers
    helpers = get_helpers()
    
    cookies_file = "data/naukri_cookies.json"
    print("Loading saved session cookies...")
    
    driver.get("https://www.naukri.com/")
    time.sleep(1)
    
    cookies = helpers.load_json(cookies_file)
    if cookies:
        for cookie in cookies:
            try:
                driver.add_cookie(cookie)
            except:
                pass
        print("✓ Cookies loaded\n")
    
    # Navigate to search results
    print("Navigating to search results...")
    search_url = "https://www.naukri.com/search?query=Python&location=Bangalore&experience=3"
    driver.get(search_url)
    time.sleep(5)
    
    print("✓ Search page loaded\n")
    
    # Inspect job cards
    print("Inspecting job card elements...\n")
    print("-" * 70)
    
    # Find all div elements that might contain jobs
    divs = driver.find_elements(By.TAG_NAME, "div")
    print(f"Found {len(divs)} div elements\n")
    
    # Look for common job card patterns
    potential_selectors = [
        ("div.jobTuple", "Job tuple divs"),
        ("article", "Article tags"),
        ("div[class*='job']", "Divs with 'job' class"),
        ("div[class*='card']", "Divs with 'card' class"),
        ("li.jobCard", "List items with jobCard class"),
    ]
    
    print("Checking potential job card selectors:\n")
    for selector, desc in potential_selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if elements:
                print(f"✓ {desc}")
                print(f"  Selector: {selector}")
                print(f"  Count: {len(elements)}")
                if len(elements) > 0:
                    first = elements[0]
                    job_title = first.text[:100] if first.text else "No text"
                    print(f"  First job: {job_title}")
                print()
        except:
            pass
    
    # Look for specific elements within jobs
    print("-" * 70)
    print("\nLooking for job details within job containers:\n")
    
    # Try to find job title, company, location
    try:
        job_containers = driver.find_elements(By.CSS_SELECTOR, "div.jobTuple")
        if job_containers:
            print(f"Found {len(job_containers)} job containers using 'div.jobTuple'\n")
            
            if len(job_containers) > 0:
                first_job = job_containers[0]
                
                # Find title
                try:
                    title = first_job.find_element(By.CSS_SELECTOR, "a[title]")
                    print(f"Job Title: {title.text}")
                    print(f"  Selector: div.jobTuple a[title]")
                except:
                    print("Could not find title")
                
                # Find company
                try:
                    company = first_job.find_element(By.CSS_SELECTOR, "div.company")
                    print(f"Company: {company.text}")
                    print(f"  Selector: div.jobTuple div.company")
                except:
                    print("Could not find company")
                
                # Find location
                try:
                    location = first_job.find_element(By.CSS_SELECTOR, "div.location")
                    print(f"Location: {location.text}")
                    print(f"  Selector: div.jobTuple div.location")
                except:
                    print("Could not find location")
    except:
        pass
    
    print("\n" + "-" * 70)
    print("\nInstructions:")
    print("1. Update config/filters.json with correct job card selector")
    print("2. Update modules/search.py with correct selectors")
    print("3. Run: python main.py\n")
    
    print("Browser will stay open for 30 seconds...")
    time.sleep(30)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    logger.error(f"Search selector finder failed: {e}")
    import traceback
    traceback.print_exc()
finally:
    try:
        get_driver_manager().close_driver()
    except:
        pass
