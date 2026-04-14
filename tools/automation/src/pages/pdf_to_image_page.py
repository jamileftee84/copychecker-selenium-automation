import os
from time import sleep
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from tools.automation.src.settings import IMAGE_DIR

class PDFToImagePage:
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

    def upload_pdf(self, file_path):
        try:
            file_path = os.path.join(IMAGE_DIR, file_path)
            # ✅ Scroll to the upload container
            upload_container_xpath = "/html/body/section/div[1]/div[1]/div[4]/div/div/div/div[4]/div[1]/div/div/div"
            upload_container = self.wait.until(EC.presence_of_element_located((By.XPATH, upload_container_xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                       upload_container)
            self.take_screenshot("05_Scrolled_To_Upload_Area")
            sleep(2)

            # ✅ Upload the file
            file_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
            file_input.send_keys(os.path.abspath(file_path))

            self.take_screenshot("06_PDF_Upload_Started")
            sleep(6)
            self.take_screenshot("07_PDF_Upload_Complete")

        except Exception as e:
            print(f"❌ PDF upload failed: {e}")

    def convert_and_download(self):
        try:
            convert_btn = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/section/div/div[4]/div/div/div/div[2]/div")
            ))
            self.take_screenshot("07_Before_Convert")
            convert_btn.click()
            sleep(5)
            self.take_screenshot("08_After_Convert")

            download_btn = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[4]/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]")
            ))
            self.take_screenshot("09_Before_Download")
            download_btn.click()
            sleep(2)
            self.take_screenshot("10_After_Download")
        except Exception as e:
            print(f"❌ Convert/Download failed: {e}")

    def back_to_editing(self):
        try:
            back_btn = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[4]/div[3]/div/div[2]/div[2]/div/div[2]/div/div[1]")
            ))
            self.take_screenshot("11_Before_Back")
            back_btn.click()
            sleep(2)
            self.take_screenshot("12_After_Back")
        except Exception as e:
            print(f"❌ Back to editing failed: {e}")

    def change_format_and_convert(self, format_label):
        try:
            # ✅ Dictionary of exact XPaths for each format
            format_xpath_map = {
                "PNG": "/html/body/section/div/div[4]/div/div/div/div[1]/div[2]/div[2]",
                "TIFF": "/html/body/section/div/div[4]/div/div/div/div[1]/div[2]/div[3]",
                "GIF": "/html/body/section/div/div[4]/div/div/div/div[1]/div[2]/div[4]",
            }

            xpath = format_xpath_map.get(format_label.upper())
            if not xpath:
                print(f"❌ Unknown format: {format_label}")
                return

            format_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", format_btn)
            sleep(5)
            self.take_screenshot(f"13_Selected_{format_label}")
            format_btn.click()
            sleep(5)

            self.convert_and_download()
            self.back_to_editing()
            sleep(5)

        except Exception as e:
            print(f"❌ Format switch failed for {format_label}: {e}")

    def start_over(self):
        try:
            restart_btn = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[4]/div[3]/div/div[2]/div[3]/div")
            ))
            restart_btn.click()
            sleep(1)
            ActionChains(self.driver).send_keys(Keys.ENTER).perform()
            self.take_screenshot("14_Start_Over")
        except Exception as e:
            print(f"❌ Start Over failed: {e}")
