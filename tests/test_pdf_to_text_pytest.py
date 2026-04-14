import pytest

from tools.automation.src.pages.common_actions import CommonActions
from tools.automation.src.pages.pdf_to_text_page import PDFToTextPage


@pytest.mark.ui
def test_pdf_to_text_smoke(driver, wait, base_url):
    common = CommonActions(driver, wait, tool_name="PDF to Text")
    common.navigate_to_tool(
        homepage_url=base_url,
        tool_xpath="/html/body/header/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div[1]/ul/a[5]",
        screenshot_label="PDF_to_Text",
    )

    page = PDFToTextPage(driver, wait)
    page.upload_pdf("Train Ticket.pdf", "Pytest")
    assert page.is_convert_button_visible()
