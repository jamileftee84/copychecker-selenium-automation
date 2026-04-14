from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from tools.automation.src.pages.small_text_page import SmallTextPage
from tools.automation.src.pages.common_actions import CommonActions
from tools.automation.src.settings import URL

input_text = (
    "The quick brown FOX jumps over 123 lazy dogs! @#$%^&*()_+-=[]{{}}|;:',.<>?/~` ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789"
)

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)

try:
    common = CommonActions(driver, wait, tool_name="Small Text Generator")
    sleep(3)
    common.navigate_to_tool(
        homepage_url=URL,
        tool_xpath="/html/body/header/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div[2]/div[1]/ul/a[3]",
        screenshot_label="Small_Text_Generator"
    )
    sleep(10)
    page = SmallTextPage(driver, wait)

    common.smooth_scroll()
    sleep(2)

    page.enter_text(input_text)
    sleep(2)

    page.preview_each_style()
    sleep(2)

    page.click_copy_and_download()
    sleep(2)

    common.search_and_open_tool_by_name("small")
    sleep(2)

finally:
    driver.quit()
