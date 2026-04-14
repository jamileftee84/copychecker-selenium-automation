from time import sleep
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from tools.automation.src.pages.pdf_to_image_page import PDFToImagePage
from tools.automation.src.pages.common_actions import CommonActions
from tools.automation.src.settings import URL

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 20)

try:
    # ✅ Common setup and navigation
    common = CommonActions(driver, wait, tool_name="PDF to Image")
    sleep(5)
    common.navigate_to_tool(
        homepage_url=URL,
        tool_xpath="/html/body/header/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div[1]/ul/a[4]",
        screenshot_label="PDF_To_Image"
    )
    sleep(10)

    # ✅ Tool interactions
    page = PDFToImagePage(driver, wait)
    common.smooth_scroll()
    page.upload_pdf("Thesis.pdf")
    page.convert_and_download()
    page.back_to_editing()

    for format in ["PNG", "TIFF", "GIF"]:
        page.change_format_and_convert(format)

    # ✅ Search-based tool access
    common.search_and_open_tool_by_name("image")
    sleep(5)

finally:
    driver.quit()
