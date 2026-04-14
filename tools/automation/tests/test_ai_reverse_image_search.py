import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from tools.automation.src.config.settings import URL, IMAGE_DIR
from tools.automation.src.pages.ai_reverse_search_page import ReverseSearchPage
from tools.automation.src.pages.common_actions import CommonActions

# Load all image files from /data/images/
images = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

# Initialize WebDriver
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)

try:
    for image_file in images:
        print(f"\n🔍 Running test for image: {image_file}")
        common = CommonActions(driver, wait, tool_name="AI Reverse Image Search")

        # Step 1: Go to homepage
        common.navigate_to_tool(
            homepage_url=URL,
            tool_xpath="/html/body/header/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div[2]/div[2]/ul/a[2]",
            screenshot_label="Text_to_ASCII"
        )
        sleep(4)

        # Step 3: Begin test actions
        page = ReverseSearchPage(driver, wait)
        page.upload_image(image_file)
        sleep(4)
        page.click_search_button()
        sleep(5)
        page.click_filter_buttons()
        sleep(5)
        page.click_start_over()
        sleep(5)

        # Step 4: Test search navigation again
        common.search_and_open_tool_by_name("ai")
        sleep(4)

finally:
    driver.quit()
    print("\n✅ Test completed for all images.")
