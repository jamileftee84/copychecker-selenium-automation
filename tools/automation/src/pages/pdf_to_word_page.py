import os
from time import sleep
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from tools.automation.src.settings import URL, IMAGE_DIR
from tools.automation.src.pages.common_actions import CommonActions

class PDFToWordPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        os.makedirs("screenshots", exist_ok=True)
        self.common = CommonActions(driver, wait)

    def timestamped(self, label):
        return f"screenshots/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{label}.png"

    def take_screenshot(self, label):
        path = self.timestamped(label)
        self.driver.save_screenshot(path)
        print(f"📸 Screenshot saved: {path}")

    def upload_image(self, filename, label="Image1"):
        try:
            file_path = os.path.join(IMAGE_DIR, filename)

            upload_container = self.wait.until(EC.presence_of_element_located((
                By.XPATH, "/html/body/section/div[1]/div[1]/div[4]/div/div/div/div[4]/div[1]/div/div/div"
            )))
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                       upload_container)

            file_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
            file_input.send_keys(os.path.abspath(file_path))
            sleep(30)

            self.take_screenshot(f"04_Upload_{label}")
            sleep(5)

        except Exception as e:
            print(f"❌ Upload failed: {e}")

    def convert_and_download(self, layout_xpath, label):
        try:
            layout_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, layout_xpath)))
            layout_button.click()
            sleep(5)
            self.take_screenshot(f"04_Converted_{label}")

            # Wait for the download button to be present and visible
            download_btn_xpath = "/html/body/div[5]/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]"
            download_btn = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, download_btn_xpath))
            )
            download_btn.click()
            sleep(2)
            self.take_screenshot(f"05_Downloaded_{label}")

        except Exception as e:
            print(f"❌ Convert or download failed for {label}: {e}")

    def click_back_to_editing(self):
        try:
            back_btn = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "/html/body/div[5]/div[3]/div/div[2]/div[2]/div/div[2]/div/div[1]"
            )))
            back_btn.click()
            sleep(2)
            self.take_screenshot("06_Back_To_Editing")
        except Exception as e:
            print(f"❌ Back to editing failed: {e}")

    def click_start_over(self):
        try:
            start_over = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "/html/body/div[5]/div[3]/div/div[2]/div[3]/div"
            )))
            start_over.click()
            sleep(1)
            ActionChains(self.driver).send_keys(Keys.ENTER).perform()
            self.take_screenshot("07_Start_Over")
        except Exception as e:
            print(f"❌ Start over failed: {e}")
