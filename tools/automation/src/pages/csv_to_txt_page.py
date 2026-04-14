import os
from time import sleep
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from tools.automation.src.settings import URL, IMAGE_DIR
from tools.automation.src.pages.common_actions import CommonActions

class CSVToTXT:
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

    def upload_csv(self, filename, label="CSV"):
        try:
            file_path = os.path.join(IMAGE_DIR, filename)

            # Step 1: Wait for and scroll to upload area
            file_input = self.wait.until(EC.presence_of_element_located((
                By.XPATH, "//input[@type='file']"
            )))
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                       file_input)
            sleep(1)

            self.driver.execute_script("arguments[0].style.display = 'block'; arguments[0].style.opacity = 1;",
                                       file_input)
            sleep(1.5)

            # Step 3: Send file to input
            file_input.send_keys(os.path.abspath(file_path))
            print(f"✅ Uploaded file: {file_path}")
            sleep(2)

        except Exception as e:
            print(f"❌ CSV upload failed: {e}")

    def convert_and_download(self):
        try:
            # Click Convert button
            convert_btn = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "/html/body/section/div/div/div[1]/div/div[3]/div/div/div[2]/div[2]/div"
            )))
            convert_btn.click()
            sleep(3)
            self.take_screenshot("05_Converted")

            # Rename file
            rename_icon_xpath = "/html/body/div[5]/div[3]/div/div[2]/div[2]/div/div[1]/div/div[1]/img"
            rename_input_xpath = "/html/body/div[5]/div[3]/div/div[2]/div[2]/div/div[1]/div/div[2]/input"
            self.common.rename_before_download(rename_icon_xpath, rename_input_xpath, "Test_CSVtoTXT")

            sleep(2)

            # Click Preview
            preview_btn = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "/html/body/div[5]/div[3]/div/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div[2]/button[1]"
            )))
            preview_btn.click()
            sleep(2)
            self.take_screenshot("06_Preview")

            # Click Back button
            back_btn = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "/html/body/div[5]/div[3]/div/div[2]/div[2]/div/div[3]/div/div[1]"
            )))
            back_btn.click()
            sleep(2)
            self.take_screenshot("07_Back_From_Preview")

            # Click Download button
            download_btn_xpath = "/html/body/div[5]/div[3]/div/div[2]/div[2]/div/div[3]/div/div[2]"
            start_over_btn_xpath = "/html/body/div[5]/div[3]/div/div[2]/div[2]/div/div[3]/div/div[1]"
            self.common.click_download_and_start_over(
                download_xpath=download_btn_xpath,
                start_over_xpath=start_over_btn_xpath
            )

        except Exception as e:
            print(f"❌ Convert and download flow failed: {e}")
