#!/usr/bin/env python
"""
Diagnostic script to check what's on the Naukri search page
"""

from selenium.webdriver.common.by import By
from core.driver_manager import get_driver_manager
from utils.helpers import get_helpers
import time

print("\nNAUKRI SEARCH PAGE DIAGNOSTIC")
print("="*70 + "\n")

try:
    # Load saved session
    driver = get_driver_manager().get_driver()
    driver.get("https://www.naukri.com/")
    time.sleep(2)
    
    cookies_file = "data/naukri_cookies.json"
    cookies = get_helpers().load_json(cookies_file)
    
    if cookies:
        for cookie in cookies:
            try:
                driver.add_cookie(cookie)
            except:
                pass
    
    # Navigate to search
    url = "https://www.naukri.com/search?query=Python&location=Bangalore&experience=3"
    print(f"Navigating to: {url}\n")
    driver.get(url)
    time.sleep(8)  # Wait for page to fully load
    
    # Get page info
    print(f"Current URL: {driver.current_url}")
    print(f"Page title: {driver.title}")
    print(f"Page height: {driver.execute_script('return document.body.scrollHeight')}px\n")
    
    # Check for error messages
    print("Checking for error messages:")
    errors = driver.find_elements(By.XPATH, "//*[contains(text(), 'error' or contains(text(), 'Error' or contains(text(), 'ERROR')))]")
    if errors:
        print(f"  Found {len(errors)} error elements")
        for err in errors[:3]:
            print(f"    - {err.text}")
    else:
        print("  No error messages found")
    
    # Check for job-related elements
    print("\nSearching for job-related elements:")
    
    patterns = [
        ("div.jobTuple", "div.jobTuple selector"),
        ("div[class*='job']", "Divs with 'job' in class"),
        ("article", "Article tags"),
        (".jobCard", "jobCard class"),
        ("a[href*='/job']", "Links with /job in href"),
        ("span[class*='jobTitle']", "Job title spans"),
    ]
    
    for selector, desc in patterns:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            status = f"✓ Found {len(elements)}" if elements else "✗ Found 0"
            print(f"  {desc}: {status}")
            if elements and len(elements) > 0:
                print(f"      First: {elements[0].text[:80]}")
        except:
            print(f"  {desc}: Error")
    
    # Check page structure
    print("\nPage structure:")
    main_areas = driver.find_elements(By.XPATH, "//div[@role='main'] | //main | //[contains(@class, 'content')]")
    print(f"  Main content areas: {len(main_areas)}")
    
    # Check HTML size
    html = driver.page_source
    print(f"\nPage HTML size: {len(html)} bytes")
    
    # Take screenshot
    print("\nTaking screenshot...")
    screenshot = driver.save_screenshot("naukri_search_page.png")
    print("Screenshot saved to: naukri_search_page.png")
    
    print("\n" + "="*70)
    print("Keeping browser open for manual inspection...")
    print("Press Ctrl+C to close and review findings\n")
    time.sleep(60)
    
except KeyboardInterrupt:
    print("\nClosed by user")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    try:
        get_driver_manager().close_driver()
    except:
        pass
