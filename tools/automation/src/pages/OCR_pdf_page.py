import os
from time import sleep
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from tools.automation.src.settings import URL, IMAGE_DIR


class OCRPDF:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        os.makedirs("screenshots", exist_ok=True)

    def timestamped(self, label):
        return f"screenshots/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{label}.png"

    def take_screenshot(self, label):
        path = self.timestamped(label)
        self.driver.save_screenshot(path)
        print(f"📸 Screenshot saved: {path}")

    def upload_pdf(self, filename, label=""):
        try:
            file_path = os.path.join(IMAGE_DIR, filename)
            # Scroll to the upload container area
            upload_container_xpath = "/html/body/section/div[1]/div[1]/div[4]/div/div/div/div/div/div[4]/div/div/div"
            upload_container = self.wait.until(EC.presence_of_element_located((By.XPATH, upload_container_xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                       upload_container)
            self.take_screenshot(f"03_Scrolled_To_Upload_{label}")
            sleep(2)

            # Try locating the file input (global if needed)
            try:
                file_input = upload_container.find_element(By.XPATH, ".//input[@type='file']")
            except:
                file_input = self.driver.find_element(By.XPATH, "//input[@type='file']")

            # Ensure file input is interactable
            self.driver.execute_script("arguments[0].style.display = 'block';", file_input)
            full_path = os.path.abspath(file_path)
            file_input.send_keys(full_path)

            self.take_screenshot(f"04_Upload_Started_{label}")
            sleep(6)
            self.take_screenshot(f"05_Upload_Completed_{label}")
            sleep(6)

        except Exception as e:
            print(f"❌ Upload error: {e}")

    def recognize_text_btn(self):
        try:
            sleep(15)  # Wait to ensure upload is complete before interacting

            recognize_text_btn_xpath = "/html/body/section/div/div[3]/div[2]/div"
            recognize_text_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, recognize_text_btn_xpath)))

            # Scroll to the Convert button smoothly
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                       recognize_text_btn)
            sleep(2)  # Let scroll finish

            self.take_screenshot("05_Before_Convert")
            recognize_text_btn.click()
            sleep(30)  # Wait for conversion process
            self.take_screenshot("06_After_Convert")

        except Exception as e:
            print(f"❌ Convert error: {e}")
