import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from tools.automation.src.config.settings import URL, IMAGE_DIR
from tools.automation.src.pages.pdf_editor_page import PDFEditorPage
from tools.automation.src.pages.common_actions import CommonActions

# Setup
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)

try:
    # Common Actions (optional if needed separately)
    common = CommonActions(driver, wait, tool_name="PDF_Editor")
    common.navigate_to_tool(
        homepage_url=URL,
        tool_xpath="/html/body/header/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div[1]/ul/a[1]",
        screenshot_label="PDF_Editor"
    )
    sleep(2)

    # Setup paths
    pdf_file_path = os.path.abspath(os.path.join(IMAGE_DIR, "Train Ticket.pdf"))
    image_file_path = os.path.abspath(os.path.join(IMAGE_DIR, "Rezaul.JPEG"))

    # Load and test
    page = PDFEditorPage(driver, wait)
    page.upload_pdf(pdf_file_path)
    sleep(3)
    page.add_text_to_pdf()
    sleep(3)
    page.add_image_to_pdf(image_file_path)
    sleep(3)
    page.add_signature_to_pdf(image_path=image_file_path)
    page.finalize_and_download()
    sleep(2)
    page.search_and_open_pdf_editor()

finally:
    driver.quit()
    print("\nPDF Editor test completed successfully.")
