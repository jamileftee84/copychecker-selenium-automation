import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from tools.automation.src.config.settings import URL, IMAGE_DIR
from tools.automation.src.pages.sign_pdf_page import SignPDF
from tools.automation.src.pages.common_actions import CommonActions

# Setup
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)

try:
    # Init commons
    common = CommonActions(driver, wait, tool_name="Sign PDF")
    common.navigate_to_tool(
        homepage_url=URL,
        tool_xpath="/html/body/header/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div[1]/ul/a[2]",
        screenshot_label="Sign_PDF"
    )
    sleep(2)

    # Init page
    page = SignPDF(driver, wait)
    pdf_file_path = os.path.abspath(os.path.join(IMAGE_DIR, "Train Ticket.pdf"))
    image_path = os.getenv(
        "SIGN_IMAGE_PATH",
        os.path.abspath(os.path.join(IMAGE_DIR, "Majnu_bhai_art.png")),
    )

    # Upload file
    page.upload_pdf(pdf_file_path)
    sleep(2)

    # Sign using all three tabs
    page.sign_with_type_tab()
    sleep(5)
    page.sign_with_draw_tab()
    sleep(5)
    page.sign_with_upload_image(image_path)
    sleep(5)

    # Apply and download
    page.finalize_and_download()
    sleep(10)

    # Repeat: click New, accept alert, upload again, and close popup
    page.click_new_and_reupload(pdf_file_path)
    sleep(3)
    common.search_and_open_tool_by_name("Sign")
    sleep(2)

finally:
    sleep(2)
    driver.quit()
    print("\n✅ Sign PDF test completed successfully.")
