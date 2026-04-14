from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from tools.automation.src.pages.csv_to_txt_page import CSVToTXT
from tools.automation.src.pages.common_actions import CommonActions
from tools.automation.src.settings import URL

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)

try:
    common = CommonActions(driver, wait, tool_name="CSV to TXT")
    sleep(5)
    common.navigate_to_tool(
        homepage_url=URL,
        tool_xpath="/html/body/header/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div[2]/div[1]/ul/a[5]/span",
        screenshot_label="CSV_to_TXT"
    )
    sleep(5)
    page = CSVToTXT(driver, wait)
    common.smooth_scroll()
    sleep(5)

    # Upload 2 CSV files
    page.upload_csv("file_sizes_report_smallPDF.csv", label="CSV")
    sleep(10)

    page.upload_csv("ImagePaths.csv", label="CSV")
    sleep(5)

    # Convert and complete flow
    page.convert_and_download()
    sleep(10)

    # Go to another tool as a check
    common.search_and_open_tool_by_name("CSV")
    sleep(3)

finally:
    driver.quit()
