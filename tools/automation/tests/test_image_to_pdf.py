from time import sleep

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from tools.automation.src.pages.image_to_pdf_page import ImageToPDFPage
from tools.automation.src.pages.common_actions import CommonActions
from tools.automation.src.settings import URL


driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)

try:
    page = ImageToPDFPage(driver, wait)
    common = CommonActions(driver, wait, tool_name="Image to PDF")

    # ✅ Navigate to tool using common method
    common.navigate_to_tool(
        homepage_url=URL,
        tool_xpath="/html/body/header/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div[1]/ul/a[10]",
        # 👈 Image to PDF tool XPath
        screenshot_label="ImageToPDF"
    )
    sleep(5)

    # ✅ Reusable scrolling
    common.smooth_scroll()

    # ✅ Upload two images
    page.upload_image("Majnu_bhai_art.png")
    sleep(15)
    page.add_more_image("Rezaul.JPEG")

    # Zoom interaction
    page.zoom_in_out()

    # Convert and download
    page.convert_to_pdf()

    rename_icon_xpath = "/html/body/div[4]/div[3]/div/div[2]/div[2]/div/div[1]/div/div[1]/img"
    rename_input_xpath = "/html/body/div[4]/div[3]/div/div[2]/div[2]/div/div[1]/div/div[2]/input"
    common.rename_before_download(rename_icon_xpath, rename_input_xpath, "Test_ImagetoPDF")
    sleep(5)

    # ✅ Reusable download + restart + Enter
    common.click_download_and_start_over(
        download_xpath="/html/body/div[4]/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]",
        start_over_xpath="/html/body/div[4]/div[3]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]",
    )
    sleep(10)
    common.search_and_open_tool_by_name("image")
    sleep(5)

finally:
    driver.quit()
