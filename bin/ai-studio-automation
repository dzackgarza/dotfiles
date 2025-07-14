#!/usr/bin/env python3
"""
Simple script to automate Google AI Studio queries
Requires: pip install selenium pyperclip undetected-chromedriver
"""

import time
import random
import pyperclip
import os
import sys
import argparse
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def setup_driver():
    """Setup undetected Chrome driver with session persistence"""
    
    # Create user data directory if it doesn't exist
    user_data_dir = os.path.expanduser("~/.ai-studio-selenium")
    if not os.path.exists(user_data_dir):
        os.makedirs(user_data_dir)
    
    try:
        options = uc.ChromeOptions()
        options.add_argument(f"--user-data-dir={user_data_dir}")
        options.add_argument("--no-first-run")
        options.add_argument("--no-default-browser-check")
        options.add_argument("--disable-extensions")
        
        # Create undetected Chrome driver
        driver = uc.Chrome(options=options, version_main=None)
        
        # Set realistic viewport
        driver.set_window_size(1366, 768)
        
        return driver
        
    except Exception as e:
        print(f"Error setting up driver: {e}")
        print("If you see 'User data directory is already in use', close all Chrome instances and try again.")
        raise

def human_like_delay(min_delay=0.5, max_delay=2.0):
    """Add human-like delays"""
    time.sleep(random.uniform(min_delay, max_delay))

def type_like_human(element, text):
    """Type text with human-like delays"""
    element.clear()
    human_like_delay(0.2, 0.5)
    
    for char in text:
        element.send_keys(char)
        # Random micro-delays between characters
        if random.random() < 0.1:  # 10% chance of brief pause
            time.sleep(random.uniform(0.05, 0.2))

def wait_for_streaming_complete(driver, max_wait_minutes=5):
    """
    Wait for AI streaming response to complete by monitoring text changes
    This is the critical function that ensures we get the full response
    """
    print("Waiting for AI streaming response to complete...")
    
    # Revised parameters for more robust streaming detection
    max_wait_seconds = max_wait_minutes * 60
    check_interval = 3  # Increased: Check every 3 seconds
    stable_duration = 15  # Increased: Text must be stable for 15 seconds
    min_total_wait = 20  # New: Always wait at least 20 seconds before considering stable
    
    # Find the response container - try multiple selectors
    response_selectors = [
        "ms-chat-turn",  # Main chat turn container
        "[data-testid='chat-turn']",
        ".response-container",
        ".ai-response",
        ".message-content"
    ]
    
    response_container = None
    for selector in response_selectors:
        try:
            containers = driver.find_elements(By.CSS_SELECTOR, selector)
            if containers:
                response_container = containers[-1]  # Get the last (most recent) response
                break
        except:
            continue
    
    if not response_container:
        print("Could not find response container. Will wait using fallback method...")
        time.sleep(30)  # Fallback: just wait 30 seconds
        return True
    
    print(f"Found response container: {response_container.tag_name}")
    
    # Monitor text changes
    previous_text = ""
    last_change_time = time.time()
    total_wait_time = 0
    min_wait_enforced = False
    
    while total_wait_time < max_wait_seconds:
        try:
            # Get current text content
            current_text = response_container.text
            current_time = time.time()
            
            # Check if text has changed
            if current_text != previous_text:
                print(f"Text changed (length: {len(current_text)})")
                previous_text = current_text
                last_change_time = current_time
            
            # Check if text has been stable long enough
            time_since_last_change = current_time - last_change_time
            
            # Enforce minimum wait before considering stable
            if total_wait_time < min_total_wait:
                if not min_wait_enforced:
                    print(f"Enforcing minimum wait of {min_total_wait} seconds before checking for stability...")
                    min_wait_enforced = True
            elif time_since_last_change >= stable_duration and len(current_text) > 0:
                print(f"✓ Text stable for {stable_duration} seconds. Response appears complete.")
                return True
            
            # Show progress
            if total_wait_time % 10 == 0:  # Every 10 seconds
                print(f"Still waiting... ({total_wait_time}s elapsed, {time_since_last_change:.1f}s since last change)")
            
            time.sleep(check_interval)
            total_wait_time += check_interval
            
        except Exception as e:
            print(f"Error monitoring text: {e}")
            time.sleep(check_interval)
            total_wait_time += check_interval
    
    print(f"Timeout after {max_wait_minutes} minutes. Response may be incomplete.")
    return False

def find_and_click_copy_markdown(driver):
    """Find and click the Copy Markdown button with multiple strategies"""
    
    # First, find and click the options button
    options_selectors = [
        "ms-chat-turn-options button[mat-icon-button]",
        "button[aria-label*='More options']",
        "button[aria-label*='Open options']",
        ".turn-options-button",
        "button:has(.more_vert)"
    ]
    
    options_button = None
    for selector in options_selectors:
        try:
            buttons = driver.find_elements(By.CSS_SELECTOR, selector)
            if buttons:
                options_button = buttons[-1]  # Get the last (most recent) button
                break
        except:
            continue
    
    if not options_button:
        print("Could not find options button")
        return False
    
    # Click options button
    print("Clicking options button...")
    driver.execute_script("arguments[0].scrollIntoView(true);", options_button)
    human_like_delay(0.3, 0.7)
    
    try:
        options_button.click()
    except:
        # Try JavaScript click if regular click fails
        driver.execute_script("arguments[0].click();", options_button)
    
    human_like_delay(0.5, 1.0)
    
    # Now find and click Copy Markdown
    copy_markdown_selectors = [
        "button:has(.copy-markdown-button)",
        "button:has(.markdown_copy)",
        ".mat-mdc-menu-item:has(.markdown_copy)",
        "button[mat-menu-item]:has(.markdown_copy)"
    ]
    
    copy_button = None
    for selector in copy_markdown_selectors:
        try:
            copy_button = driver.find_element(By.CSS_SELECTOR, selector)
            break
        except:
            continue
    
    # Fallback: search by text content
    if not copy_button:
        menu_items = driver.find_elements(By.CSS_SELECTOR, ".mat-mdc-menu-item, button[mat-menu-item]")
        for item in menu_items:
            if "markdown" in item.text.lower():
                copy_button = item
                break
    
    if copy_button:
        print("Clicking Copy Markdown...")
        try:
            copy_button.click()
        except:
            driver.execute_script("arguments[0].click();", copy_button)
        return True
    else:
        print("Could not find Copy Markdown button")
        return False

def query_ai_studio(query_text, max_wait_minutes=5, non_interactive=False):
    """Main function to query AI Studio and copy markdown response"""
    driver = None
    copied_content = None
    
    try:
        driver = setup_driver()
        
        # Navigate to AI Studio
        print("Opening Google AI Studio...")
        driver.get("https://aistudio.google.com/")
        
        # Wait for page to load
        print("Waiting for page to load...")
        human_like_delay(3, 6)
        
        # Check if we need to log in
        if "accounts.google.com" in driver.current_url or "Sign in" in driver.page_source:
            if non_interactive:
                print("ERROR: Not authenticated and running in non-interactive mode. Exiting.")
                return False, None
            print("Please log in to Google AI Studio in the browser window...")
            print("After logging in, press Enter to continue...")
            input()
            
            # Navigate back to AI Studio if needed
            if "aistudio.google.com" not in driver.current_url:
                driver.get("https://aistudio.google.com/")
                human_like_delay(3, 5)
        
        # Find the textarea for input
        print("Looking for input field...")
        textarea_selector = "textarea.textarea.gmat-body-medium"
        
        try:
            wait = WebDriverWait(driver, 20)
            textarea = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, textarea_selector)))
        except:
            print("Could not find the specific textarea. Trying generic textarea...")
            textarea = driver.find_element(By.TAG_NAME, "textarea")
        
        # Click on textarea to focus
        print("Clicking on input field...")
        textarea.click()
        human_like_delay(0.3, 0.8)
        
        # Type the query with human-like behavior
        print(f"Entering query: {query_text}")
        type_like_human(textarea, query_text)
        
        human_like_delay(1, 2)
        
        # Submit with Ctrl+Enter
        print("Submitting query with Ctrl+Enter...")
        ActionChains(driver).key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(Keys.CONTROL).perform()
        
        # Wait for streaming response to complete
        if wait_for_streaming_complete(driver, max_wait_minutes):
            print("✓ Response appears complete!")
        else:
            print("⚠ Response may be incomplete, but proceeding...")
        
        # Additional safety wait
        human_like_delay(2, 4)
        
        # Find and click Copy Markdown
        if find_and_click_copy_markdown(driver):
            human_like_delay(0.5, 1.0)
            
            # Get the copied content
            try:
                copied_content = pyperclip.paste()
                print("✓ Markdown response copied to clipboard!")
                print(f"Response length: {len(copied_content)} characters")
                print(f"Response preview: {copied_content[:200]}...")
                
                # Save to file as backup
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"ai_studio_response_{timestamp}.md"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(copied_content)
                print(f"✓ Response saved to '{filename}'")
                
                return True, copied_content
                
            except Exception as e:
                print(f"Could not access clipboard: {e}")
                return False, None
        else:
            print("Could not find Copy Markdown button")
            return False, None
        
    except Exception as e:
        print(f"Error: {e}")
        print("The script encountered an error. The browser will remain open for manual interaction.")
        return False, None
    
    finally:
        if driver:
            if not non_interactive:
                print("\nBrowser will remain open to preserve session.")
                print("Close the browser window when you're done, or press Enter to close it now.")
                input()
            driver.quit()

def main():
    parser = argparse.ArgumentParser(description="Automate Google AI Studio queries.")
    parser.add_argument('--wait-time', type=int, default=5, help='Max wait time in minutes (default: 5)')
    args = parser.parse_args()
    non_interactive = not sys.stdin.isatty()
    if non_interactive:
        query = sys.stdin.read().strip()
        if not query:
            print("No query provided on stdin. Exiting.")
            sys.exit(1)
    else:
        print("Google AI Studio Automation Script")
        print("===================================")
        query = input("Enter your query for Google AI Studio: ").strip()
        if not query:
            print("No query provided. Exiting.")
            sys.exit(1)
        try:
            wait_time = input("Max wait time in minutes (default: 5): ").strip()
            if wait_time:
                args.wait_time = int(wait_time)
        except ValueError:
            pass
        print(f"Will wait up to {args.wait_time} minutes for response completion.")
    success, copied_content = query_ai_studio(query, args.wait_time, non_interactive=non_interactive)
    if non_interactive and copied_content:
        print("\n--- AI Studio Markdown Response ---\n")
        print(copied_content)
    if success:
        print("✓ Task completed successfully!")
    else:
        print("⚠ Task completed with issues. Check the output above.")

if __name__ == "__main__":
    main() 