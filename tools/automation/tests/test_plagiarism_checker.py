from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from tools.automation.src.config.settings import URL
from tools.automation.src.pages.plagiarism_checker_page import PlagiarismCheckerPage
from tools.automation.src.pages.common_actions import CommonActions


options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)
driver.maximize_window()
wait = WebDriverWait(driver, 15)

try:
    common = CommonActions(driver, wait, tool_name="Plagiarism Checker")
    page = PlagiarismCheckerPage(driver, wait)

    # Open site (auto lands on Plagiarism Checker)
    driver.get(URL)
    wait.until(lambda d: d.find_element("tag name", "textarea"))

    page.check_first_text()
    sleep(2)
    page.interact_with_report()
    sleep(2)
    page.start_new_search()
    sleep(2)
    common.search_and_open_tool_by_name("plagiarism")
    sleep(2)

finally:
    driver.quit()
    print("\nPlagiarism Checker test completed successfully.")
