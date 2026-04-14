from time import sleep
from tools.automation.src.settings import URL

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from tools.automation.src.pages.OCR_pdf_page import OCRPDF
from tools.automation.src.pages.common_actions import CommonActions

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)
try:
    common = CommonActions(driver, wait, tool_name="OCR PDF")
    sleep(5)
    common.navigate_to_tool(
        homepage_url=URL,
        tool_xpath="/html/body/header/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div[1]/ul/a[6]/span",
        screenshot_label="OCR PDF"
    )
    page = OCRPDF(driver, wait)
    common.smooth_scroll()
    page.upload_pdf("Train Ticket.pdf", "First_File")
    page.recognize_text_btn()
    sleep(15)
    common.click_download_and_start_over(
        download_xpath="/html/body/div[5]/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]",
        start_over_xpath="/html/body/div[5]/div[3]/div/div[2]/div[2]/div/div[2]/div/div[1]", )
    sleep(10)
    common.search_and_open_tool_by_name("OCR")
finally:
    driver.quit()