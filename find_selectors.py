#!/usr/bin/env python
"""
Find correct CSS selectors for Naukri login page
Run this to inspect the page and find working selectors
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.driver_manager import get_driver_manager
from core.logger import get_logger

logger = get_logger(__name__)

print("\n" + "="*70)
print("NAUKRI SELECTOR FINDER")
print("="*70 + "\n")

print("Opening https://www.naukri.com/ in browser...")
print("⏳ Please WAIT - browser will open automatically...\n")

try:
    # Initialize Chrome WebDriver using project's driver manager
    driver = get_driver_manager().get_driver()
    
    import time
    
    # Try direct login URL first
    print("Trying direct login URL...")
    driver.get("https://www.naukri.com/naukri/user/login")
    time.sleep(3)
    
    # Check if page has login form
    try:
        driver.find_element(By.ID, "usernameField")
        print("✓ Login page found via direct URL\n")
    except:
        print("Not found, trying alternative login URL...")
        driver.get("https://www.naukri.com/")
        time.sleep(2)
        
        # Try to find and click login link
        try:
            login_link = driver.find_element(By.LINK_TEXT, "Login")
            login_link.click()
            print("✓ Clicked login link\n")
            time.sleep(2)
        except:
            print("Could not find login link, checking current page...\n")
    
    print("Inspecting login form elements...\n")
    print("-" * 70)
    
    # Find all input fields
    inputs = driver.find_elements(By.TAG_NAME, "input")
    print(f"Found {len(inputs)} input fields:\n")
    
    for i, inp in enumerate(inputs):
        input_id = inp.get_attribute("id")
        input_name = inp.get_attribute("name")
        input_type = inp.get_attribute("type")
        input_class = inp.get_attribute("class")
        input_placeholder = inp.get_attribute("placeholder")
        
        print(f"Input #{i+1}:")
        if input_id:
            print(f"  id: '{input_id}' → Selector: input[id='{input_id}']")
        if input_name:
            print(f"  name: '{input_name}' → Selector: input[name='{input_name}']")
        if input_type:
            print(f"  type: '{input_type}'")
        if input_class:
            print(f"  class: '{input_class}' → Selector: input.{input_class.split()[0]}")
        if input_placeholder:
            print(f"  placeholder: '{input_placeholder}'")
        print()
    
    # Find all buttons
    buttons = driver.find_elements(By.TAG_NAME, "button")
    print("-" * 70)
    print(f"Found {len(buttons)} buttons:\n")
    
    for i, btn in enumerate(buttons):
        btn_id = btn.get_attribute("id")
        btn_name = btn.get_attribute("name")
        btn_class = btn.get_attribute("class")
        btn_text = btn.text.strip()
        btn_type = btn.get_attribute("type")
        
        if btn_text or btn_id or btn_name:  # Only show if has meaningful content
            print(f"Button #{i+1}:")
            if btn_id:
                print(f"  id: '{btn_id}' → Selector: button[id='{btn_id}']")
            if btn_name:
                print(f"  name: '{btn_name}' → Selector: button[name='{btn_name}']")
            if btn_class:
                print(f"  class: '{btn_class}' → Selector: button.{btn_class.split()[0]}")
            if btn_text:
                print(f"  text: '{btn_text}'")
            if btn_type:
                print(f"  type: '{btn_type}'")
            print()
    
    print("-" * 70)
    print("\n📌 INSTRUCTIONS:")
    print("1. Copy the selectors from above")
    print("2. Update config/config.json with the correct selectors")
    print("3. Replace:")
    print("   - 'email_selector' with the email input selector")
    print("   - 'password_selector' with the password input selector")
    print("   - 'login_button_selector' with the login button selector")
    print("\n4. Run: python main.py\n")
    
    print("Browser will stay open for 30 seconds so you can inspect manually...")
    print("(Press Ctrl+C to close sooner)")
    
    time.sleep(30)
    
except KeyboardInterrupt:
    print("\n\n✓ Closed by user")
except Exception as e:
    print(f"\n❌ Error: {e}")
    logger.error(f"Selector finder failed: {e}")
finally:
    try:
        get_driver_manager().close_driver()
        print("✓ Browser closed\n")
    except:
        pass
