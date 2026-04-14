import os
from time import sleep
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from tools.automation.src.settings import URL, IMAGE_DIR

class ExtractPDFPagesPage:
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
            upload_container_xpath = "/html/body/section/div[1]/div[1]/div[5]/div/div/div/div[4]/div[1]/div/div/div"
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

    def extract_custom_pages(self, page_range):
        try:
            input_box = self.wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/section/div/div[5]/div/div/div[1]/div[2]/input")))
            input_box.clear()
            input_box.send_keys(page_range)
            sleep(1)
            self.take_screenshot("05_Entered_Custom_Pages")

            extract_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div[5]/div/div/div[2]/div")))
            extract_btn.click()
            sleep(4)
            self.take_screenshot("06_Custom_Extracted")

            self.download()
        except Exception as e:
            print(f"❌ Extract custom pages error: {e}")

    def extract_by_mode(self, mode_label):
        try:
            # Back to Editing
            back_btn = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "/html/body/div[5]/div[3]/div/div[2]/div[2]/div/div[2]/div/div[1]"
            )))
            back_btn.click()
            sleep(2)

            # Use correct XPath based on mode_label
            if mode_label.lower() == "all odd pages":
                mode_xpath = "/html/body/section/div/div[5]/div/div/div[1]/div[1]/div[2]/button[1]"
            elif mode_label.lower() == "all even pages":
                mode_xpath = "/html/body/section/div/div[5]/div/div/div[1]/div[1]/div[2]/button[2]"
            else:
                print(f"❌ Unsupported mode: {mode_label}")
                return

            # Select mode
            mode_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, mode_xpath)))
            mode_btn.click()
            sleep(2)
            self.take_screenshot(f"07_Selected_{mode_label.replace(' ', '_')}")

            # Click Extract Pages
            extract_btn = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "/html/body/section/div/div[5]/div/div/div[2]/div"
            )))
            extract_btn.click()
            sleep(4)
            self.take_screenshot(f"08_Extracted_{mode_label.replace(' ', '_')}")

            self.download()

        except Exception as e:
            print(f"❌ Extract {mode_label} pages error: {e}")

    def download(self):
        try:
            download_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]")))
            self.take_screenshot("09_Before_Download")
            download_btn.click()
            sleep(3)
            self.take_screenshot("10_After_Download")
        except Exception as e:
            print(f"❌ Download failed: {e}")

    def start_over(self):
        try:
            start_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[3]/div/div[2]/div[2]/div/div[2]/div/div[1]")))
            start_btn.click()
            sleep(1)
            ActionChains(self.driver).send_keys(Keys.ENTER).perform()
            sleep(2)
            self.take_screenshot("11_Start_Over")
        except Exception as e:
            print(f"❌ Start Over failed: {e}")
