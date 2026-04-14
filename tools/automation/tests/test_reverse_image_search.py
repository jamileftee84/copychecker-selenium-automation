import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from tools.automation.src.config.settings import URL, IMAGE_DIR
from tools.automation.src.pages.reverse_image_search_page import ReverseImageSearchPage
from tools.automation.src.pages.common_actions import CommonActions
from tools.automation.src.utils.helpers import take_screenshot, wait

# Load image files to test
images = [os.path.join(IMAGE_DIR, f) for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

# Launch browser
driver = webdriver.Chrome()
driver.maximize_window()
wait_time = WebDriverWait(driver, 15)

for image_file in images:
    print(f"\n🔍 Testing image: {image_file}")

    common = CommonActions(driver, wait_time, tool_name="Reverse_Image_Search")
    common.navigate_to_tool(
        homepage_url=URL,
        tool_xpath="/html/body/header/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div[2]/div[2]/ul/a[1]",
        screenshot_label="Reverse_Image_Search"
    )
    wait(2)

    page = ReverseImageSearchPage(driver, wait_time)

    common.smooth_scroll()
    sleep(5)

    page.upload_image(os.path.basename(image_file))
    wait(2)

    page.click_search_button()
    wait(4)

    page.explore_filters()
    wait(2)

    take_screenshot(driver, f"Final_Result_{os.path.basename(image_file)}")

    page.click_start_over()
    wait(5)

    common.search_and_open_tool_by_name("reverse")
    wait(2)

# Finalize
driver.quit()
print("\n✅ Reverse Image Search test completed successfully.")
