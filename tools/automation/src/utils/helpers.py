import os
from time import sleep
from selenium.webdriver.common.by import By

# Utility: Wait for a specified number of seconds (default = 3)
def wait(seconds=3):
    """Pause execution for a specified number of seconds."""
    sleep(seconds)


# Utility: Take a screenshot and save it to the screenshots/ directory
def take_screenshot(driver, filename):
    """
    Capture a screenshot using the current driver and save it with the given filename.

        driver: Selenium WebDriver instance.
        filename: Name of the screenshot file (should include .png).
    """
    # Ensure screenshot directory exists
    os.makedirs("screenshots", exist_ok=True)

    # Define the full file path
    path = os.path.join("screenshots", filename)

    # Capture screenshot
    driver.save_screenshot(path)
    print(f"📸 Screenshot saved: {path}")
