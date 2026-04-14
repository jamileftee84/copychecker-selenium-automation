import os
from time import sleep
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from tools.automation.src.settings import IMAGE_DIR
from tools.automation.src.pages.common_actions import CommonActions

class TextToASCII:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.common = CommonActions(driver, wait, tool_name="Text_to_ASCII")

    def timestamped(self, label):
        return f"screenshots/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{label}.png"

    def take_screenshot(self, label):
        path = self.timestamped(label)
        self.driver.save_screenshot(path)
        print(f"📸 Screenshot saved: {path}")

    def enter_text_and_clear(self, text="Test ASCII"):
        try:
            input_box_xpath = "/html/body/section/div[1]/div[4]/div[1]/div/div/div[1]/div[1]/textarea"
            clear_btn_xpath = "/html/body/section/div[1]/div[4]/div[1]/div/div/div[1]/div[1]/button"

            # Enter text
            input_box = self.wait.until(EC.presence_of_element_located((By.XPATH, input_box_xpath)))
            input_box.clear()
            input_box.send_keys(text)
            sleep(5)
            self.take_screenshot("01_Text_Entered")

            # Clear text
            clear_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, clear_btn_xpath)))
            clear_btn.click()
            sleep(2)
            self.take_screenshot("02_Text_Cleared")

        except Exception as e:
            print(f"Enter and clear text failed: {e}")
            self.common.log_failure(str(e))

    def upload_txt_file(self, filename, label="ASCII"):
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
            print(f"File upload failed: {e}")

    def copy_output(self):
        try:
            copy_btn_xpath = "/html/body/section/div[1]/div[4]/div[1]/div/div/div[1]/div[2]/button"
            copy_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, copy_btn_xpath)))
            copy_btn.click()
            sleep(3)
            self.take_screenshot("04_Output_Copied")
        except Exception as e:
            print(f"Copy output failed: {e}")
            self.common.log_failure(str(e))
