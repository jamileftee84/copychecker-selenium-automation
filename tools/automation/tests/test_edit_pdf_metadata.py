from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from tools.automation.src.pages.edit_pdf_metadata_page import EditPDFMetadataPage
from tools.automation.src.pages.common_actions import CommonActions
from tools.automation.src.settings import URL

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)

try:
    common = CommonActions(driver, wait, tool_name="Edit PDF Metadata")
    sleep(5)
    common.navigate_to_tool(
        homepage_url=URL,
        tool_xpath="/html/body/header/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div[1]/ul/a[12]",
        screenshot_label="Edit_PDF_Metadata"
    )
    sleep(20)
    page = EditPDFMetadataPage(driver, wait)
    common.smooth_scroll()
    page.upload_pdf("Train Ticket.pdf")  # Change to your valid test PDF if needed
    sleep(40)
    page.remove_metadata_and_download()
    sleep(10)
    page.change_metadata_and_download()
    sleep(10)
    common.search_and_open_tool_by_name("word")
    sleep(1)

finally:
    driver.quit()
