from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from tools.automation.src.pages.text_to_ascii_page import TextToASCII
from tools.automation.src.pages.common_actions import CommonActions
from tools.automation.src.settings import URL

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)

try:
    common = CommonActions(driver, wait, tool_name="Text to ASCII")

    # Navigate via All Tools > Text to ASCII
    common.navigate_to_tool(
        homepage_url=URL,
        tool_xpath="/html/body/header/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div[2]/div[1]/ul/a[6]",
        screenshot_label="Text_to_ASCII"
    )
    sleep(5)

    # Page object
    page = TextToASCII(driver, wait)

    # Scroll and interact
    common.smooth_scroll()
    sleep(3)

    # Step 1: Enter and clear text
    page.enter_text_and_clear("Hello ASCII!")

    # Step 2: Upload .txt file
    page.upload_txt_file("Simple Data Writer.txt", label="ASCII")
    sleep(3)

    # Step 3: Copy output
    page.copy_output()
    sleep(2)

    # Step 4: Use search to revisit the tool
    common.search_and_open_tool_by_name("ascii")
    sleep(3)

finally:
    driver.quit()
