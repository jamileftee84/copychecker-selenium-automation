"""
Automated UI Test: Happy Birthday Fonts Tool
--------------------------------------------
This script automates testing of the Happy Birthday Fonts tool on CopyChecker.
It follows best practices in structure, timing, and clarity to ensure easy team collaboration.

Maintained for: Bitbucket-ready structure
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from tools.automation.src.pages.happy_birthday_page import HappyBirthdayFontsPage
from time import sleep
from tools.automation.src.pages.common_actions import CommonActions

# Initialize Chrome WebDriver using webdriver-manager (auto-download latest driver)
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)

try:
    common = CommonActions(driver, wait, tool_name="Happy Birthday Fonts")
    # Instantiate the page object for Happy Birthday Fonts tool
    page = HappyBirthdayFontsPage(driver, wait)

    # Navigate to the tool from homepage > All Tools > Happy Birthday Fonts
    page.go_to_tool()
    sleep(2)  # Small delay to allow initial animation/load

    # Scroll down and click "Start Writing Your Birthday Messages" button
    page.scroll_to_start_button_and_click()
    sleep(2)

    # Clear input box if any text exists from prior session
    page.clear_input()
    sleep(2)

    # Type a default birthday message
    page.enter_message()
    sleep(2)

    # Click "All Preview" to display all font styles in modal and close it afterward
    page.click_all_preview()
    sleep(2)

    # Copy all available font styles (up to 20)
    copied = page.copy_all_fonts()
    sleep(2)

    # Clear the input again to simulate reset
    page.clear_input()
    sleep(2)

    # Paste the previously copied message back into input
    page.paste_text_back(copied or "Fallback birthday message")
    sleep(5)

    common.search_and_open_tool_by_name("happy")

finally:
    # Cleanly close browser after test
    driver.quit()
