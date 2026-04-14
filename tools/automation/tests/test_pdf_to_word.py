from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from tools.automation.src.pages.pdf_to_word_page import PDFToWordPage
from tools.automation.src.pages.common_actions import CommonActions
from tools.automation.src.settings import URL  # ✅ Add if not already there


driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)

try:
    common = CommonActions(driver, wait, tool_name="PDF to Word")
    common.navigate_to_tool(
        homepage_url=URL,
        tool_xpath="/html/body/header/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div[1]/ul/a[11]/span",
        screenshot_label="PDF_to_Word"
    )

    sleep(15)

    page = PDFToWordPage(driver, wait)
    common.smooth_scroll()

    sleep(5)
    page.upload_image("Train Ticket.pdf")

    sleep(10)

    page.convert_and_download(
        layout_xpath="/html/body/section/div/div/div[3]/div/div[2]/div[1]/div",
        label="Keep_Layout"
    )

    sleep(60)

    page.click_back_to_editing()

    sleep(5)

    page.convert_and_download(
        layout_xpath="/html/body/section/div/div/div[3]/div/div[2]/div[2]/div",
        label="Optimized_Layout"
    )
    page.click_back_to_editing()
    sleep(15)

    common.search_and_open_tool_by_name("word")

finally:
    driver.quit()
