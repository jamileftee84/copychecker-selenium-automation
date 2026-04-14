import os
import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tools.automation.src.pages.common_actions import CommonActions
from tools.automation.src.settings import IMAGE_DIR

class ReverseSearchPage:
    """
    Page Object for the AI Reverse Image Search tool.
    Encapsulates interactions with the UI for maintainable and readable test automation.
    """

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.common = CommonActions(driver, wait, tool_name="AI_Reverse_Image_Search")

    def upload_image(self, image_filename):
        """
        Uploads an image from the local data/images folder via file input.
        """
        try:
            image_path = os.path.abspath(os.path.join(IMAGE_DIR, image_filename))
            file_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))

            self.common.take_screenshot("01_BEFORE_Upload")
            file_input.send_keys(image_path)
            time.sleep(2)
            self.common.take_screenshot("02_AFTER_Upload")

        except Exception as e:
            print(f"❌ Image upload failed: {e}")
            self.common.take_screenshot("ERROR_Upload")

    def click_search_button(self):
        """
        Clicks the 'Search with AI' button after uploading the image.
        Also handles ad overlay issue before clicking.
        """
        try:
            # Hide any ad overlays
            self.driver.execute_script(
                "document.querySelectorAll('ins.adsbygoogle').forEach(ad => ad.style.display = 'none');")
            search_btn = self.wait.until(EC.presence_of_element_located((
                By.XPATH, "/html/body/section/div[1]/div[1]/div[5]/div"
            )))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", search_btn)
            time.sleep(1.5)
            self.common.take_screenshot("03_BEFORE_Search_Click")
            self.driver.execute_script("arguments[0].click();", search_btn)
            time.sleep(5)
            self.common.take_screenshot("04_AFTER_Search_Click")

        except Exception as e:
            print(f"❌ Search button click failed: {e}")
            self.common.take_screenshot("ERROR_Search_Click")

    def click_filter_buttons(self):
        """
        Clicks each of the four filter tabs:
        Partial Matches, Websites, Similar, and About.
        Takes a screenshot before and after each click.
        """
        buttons = [
            {"label": "Partial_Matches", "xpath": "/html/body/section/div/div/div/div[2]/div/div[1]/div/button[2]"},
            {"label": "Websites", "xpath": "/html/body/section/div/div/div/div[2]/div/div[1]/div/button[3]"},
            {"label": "Similar", "xpath": "/html/body/section/div/div/div/div[2]/div/div[1]/div/button[4]"},
            {"label": "About", "xpath": "/html/body/section/div/div/div/div[2]/div/div[1]/div/button[5]"}
        ]

        for btn in buttons:
            try:
                element = self.wait.until(EC.presence_of_element_located((By.XPATH, btn["xpath"])))
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(2.5)
                self.common.take_screenshot(f"05_BEFORE_{btn['label']}")
                self.driver.execute_script("arguments[0].click();", element)
                print(f"✅ Clicked: {btn['label']}")
                time.sleep(5)
                self.common.take_screenshot(f"06_AFTER_{btn['label']}")

            except Exception as e:
                print(f"❌ Failed to click {btn['label']}: {e}")

    def click_start_over(self):
        """
        Clicks the 'Start Over' button to reset the UI.
        """
        try:
            start_over = self.wait.until(EC.presence_of_element_located((
                By.XPATH, "/html/body/section/div/div/div/div[1]/div[2]"
            )))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", start_over)
            time.sleep(1.5)
            self.common.take_screenshot("07_BEFORE_Start_Over")
            self.driver.execute_script("arguments[0].click();", start_over)
            time.sleep(2)
            self.common.take_screenshot("08_AFTER_Start_Over")

        except Exception as e:
            print(f"❌ Start Over failed: {e}")
