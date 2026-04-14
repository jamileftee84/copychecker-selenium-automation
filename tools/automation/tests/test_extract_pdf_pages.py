from time import sleep
from tools.automation.src.settings import URL
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from tools.automation.src.pages.extract_pdf_pages_page import ExtractPDFPagesPage
from tools.automation.src.pages.common_actions import CommonActions

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)

try:
    common = CommonActions(driver, wait, tool_name="Extract PDF Metadata")
    common.navigate_to_tool(
        homepage_url=URL,
        tool_xpath="/html/body/header/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div[1]/ul/a[7]/span",
        screenshot_label="Extract PDF Pages"
    )
    page = ExtractPDFPagesPage(driver, wait)
    common.smooth_scroll()
    page.upload_pdf("Thesis.pdf")  # Replace with your PDF file path
    page.extract_custom_pages("2-5")
    page.extract_by_mode("All Odd Pages")
    page.extract_by_mode("All Even Pages")
    page.start_over()
    sleep(10)
    common.search_and_open_tool_by_name("extract")

finally:
    driver.quit()
