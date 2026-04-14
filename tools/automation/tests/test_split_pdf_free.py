from time import sleep
from tools.automation.src.settings import URL
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from tools.automation.src.pages.split_pdf_free_page import SplitPDFPage
from tools.automation.src.pages.common_actions import CommonActions

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)

try:
    common = CommonActions(driver, wait, tool_name="Split PDF Free")
    common.navigate_to_tool(
        homepage_url=URL,
        tool_xpath="/html/body/header/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div[1]/ul/a[8]",
        screenshot_label="Split PDF"
    )
    sleep(5)
    page = SplitPDFPage(driver, wait)
    common.smooth_scroll()
    # ✅ First option: All pages
    page.upload_pdf("Thesis.pdf", label="AllPages")
    page.select_split_all_pages()
    page.click_split_button()
    page.download_and_start_over(go_home_after=True)  # ✅ Go to home and reload tool

    # ✅ Second option: Range 2-5
    page.upload_pdf("Thesis.pdf", label="PageRange")
    page.select_page_range_and_split("2-5")

    sleep(10)
    common.search_and_open_tool_by_name("split")

finally:
    driver.quit()
