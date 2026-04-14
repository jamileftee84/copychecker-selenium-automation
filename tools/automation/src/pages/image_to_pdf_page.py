import os
import sys
from time import sleep
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from tools.automation.src.settings import URL, IMAGE_DIR  # ✅ import from settings

class ImageToPDFPage:
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

            self.take_screenshot(f"04_Upload_{label}")
            sleep(5)

        except Exception as e:
            print(f"❌ Upload failed: {e}")

    def add_more_image(self, filename, label="Image2"):
        try:
            file_path = os.path.join(IMAGE_DIR, filename)

            add_btn = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "/html/body/section/div[2]/div[3]/div/div/div/div[1]/div[1]/label"
            )))
            sleep(3)

            file_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
            file_input.send_keys(os.path.abspath(file_path))

            self.take_screenshot(f"05_Upload_{label}")
            sleep(4)

        except Exception as e:
            print(f"❌ Add More Image failed: {e}")

    def zoom_in_out(self, times=15):
        try:
            zoom_in = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "/html/body/section/div[2]/div[2]/div[1]/div/div/button[2]"
            )))
            for _ in range(times):
                zoom_in.click()
                sleep(0.2)
            self.take_screenshot("06_Zoomed_In")

            zoom_out = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "/html/body/section/div[2]/div[2]/div[1]/div/div/button[1]"
            )))
            for _ in range(times):
                zoom_out.click()
                sleep(0.2)
            self.take_screenshot("07_Zoomed_Out")

        except Exception as e:
            print(f"❌ Zoom interaction failed: {e}")

    def convert_to_pdf(self):
        try:
            convert_btn = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "/html/body/section/div[3]/div/div[3]/button"
            )))
            convert_btn.click()
            sleep(5)
            self.take_screenshot("08_Converted")

        except Exception as e:
            print(f"❌ Convert to PDF failed: {e}")


