from time import sleep
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from tools.automation.src.pages.pdf_to_text_page import PDFToTextPage
from tools.automation.src.pages.common_actions import CommonActions
from tools.automation.src.settings import URL

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)

try:
    common = CommonActions(driver, wait, tool_name="PDF to Text")
    sleep(5)
    common.navigate_to_tool(
        homepage_url=URL,
        tool_xpath="/html/body/header/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div[1]/ul/a[5]",
        screenshot_label="PDF_to_Text"
    )
    page = PDFToTextPage(driver, wait)
    common.smooth_scroll()
    page.upload_pdf("Train Ticket.pdf", "First_File")
    page.click_convert_button()
    sleep(5)
    common.click_download_and_start_over(
        download_xpath="/html/body/div[5]/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]",
        start_over_xpath="/html/body/div[5]/div[3]/div/div[2]/div[2]/div/div[2]/div/div[1]",)
    sleep(5)
    common.search_and_open_tool_by_name("text")
finally:
    driver.quit()
