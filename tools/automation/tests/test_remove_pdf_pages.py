from time import sleep

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from tools.automation.src.pages.remove_pdf_pages_page import RemovePDFPagesPage
from tools.automation.src.pages.common_actions import CommonActions
from tools.automation.src.settings import URL

# ✅ Setup driver
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 20)

try:
    # ✅ Common actions and navigation
    common = CommonActions(driver, wait, tool_name="Remove PDF Pages")
    sleep(5)
    common.navigate_to_tool(
        homepage_url=URL,
        tool_xpath="/html/body/header/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div[1]/ul/a[3]/span",
        screenshot_label="Remove_PDF_Pages"
    )

    sleep(20)

    # ✅ Tool-specific interactions
    page = RemovePDFPagesPage(driver, wait)
    common.smooth_scroll()
    page.upload_pdf("Thesis.pdf")  # Replace with a valid test file path
    sleep(10)
    page.enter_page_number_and_apply(page_number=2)
    sleep(5)
    page.click_download_and_restart()
    sleep(10)
    common.search_and_open_tool_by_name("remove")
    sleep(5)

finally:
    driver.quit()
