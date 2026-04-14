from time import sleep
from tools.automation.src.settings import URL
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from tools.automation.src.pages.merge_pdf_page import MergePDFPage
from tools.automation.src.pages.common_actions import CommonActions

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)

try:
    common = CommonActions(driver, wait, tool_name="Merge PDF")
    common.navigate_to_tool(
        homepage_url=URL,
        tool_xpath="/html/body/header/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div[1]/ul/a[9]",
        screenshot_label="Merge PDF"
    )
    sleep(5)
    page = MergePDFPage(driver, wait)
    common.smooth_scroll()
    page.upload_pdfs("Thesis.pdf", "Train Ticket.pdf")
    page.click_views()
    page.zoom_in_out()
    page.merge_and_download()
    sleep(10)
    page.back_to_editing()
    sleep(10)
    common.search_and_open_tool_by_name("merge")

finally:
    driver.quit()
