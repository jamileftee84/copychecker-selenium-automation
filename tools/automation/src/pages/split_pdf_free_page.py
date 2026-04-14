import os
from time import sleep
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from tools.automation.src.settings import URL, IMAGE_DIR

class SplitPDFPage:
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

    def navigate_to_tool(self):
        self.driver.get(URL)
        sleep(2)
        self.take_screenshot("01_Home")

        try:
            all_tools = self.wait.until(EC.presence_of_element_located((
                By.XPATH, '//*[@id="navigationBar"]/div[1]/div[1]/div[1]/div[1]/div[1]/button[1]'
            )))
            ActionChains(self.driver).move_to_element(all_tools).perform()
            sleep(1)

            split_pdf_tool = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "/html/body/header/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div[1]/ul/a[8]"
            )))
            split_pdf_tool.click()
            sleep(2)
            self.take_screenshot("02_Tool_Page")
        except Exception as e:
            print(f"❌ Navigation error: {e}")

    def upload_pdf(self, filename, label):
        try:
            file_path = os.path.join(IMAGE_DIR, filename)
            upload_container = self.wait.until(EC.presence_of_element_located((
                By.XPATH, "/html/body/section/div[1]/div[1]/div[5]/div/div/div/div[4]/div[1]/div/div/div"
            )))
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                       upload_container)
            file_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
            full_path = os.path.abspath(file_path)
            file_input.send_keys(full_path)
            self.take_screenshot(f"04_Upload_{label}")
            sleep(5)
        except Exception as e:
            print(f"❌ Upload error: {e}")

    def select_split_all_pages(self):
        try:
            all_pages_radio = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "/html/body/section/div/div[1]/div[3]/div/div[2]/button[1]/div"
            )))
            all_pages_radio.click()
            sleep(1)
            self.take_screenshot("05_Selected_AllPages")
        except Exception as e:
            print(f"❌ Select All Pages error: {e}")

    def click_split_button(self):
        try:
            split_btn = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "/html/body/section/div/div[2]/div/div/div/div/button"
            )))
            self.take_screenshot("06_Before_Split")
            split_btn.click()
            sleep(5)
            self.take_screenshot("07_After_Split")
        except Exception as e:
            print(f"❌ Split button error: {e}")

    def download_and_start_over(self, go_home_after=False):
        try:
            download_btn = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "/html/body/div[4]/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]"
            )))
            download_btn.click()
            self.take_screenshot("08_Downloaded")
            sleep(2)
        except Exception as e:
            print(f"❌ Download error: {e}")

        try:
            start_over_btn = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "/html/body/div[4]/div[3]/div/div[2]/div[3]/div"
            )))
            start_over_btn.click()
            sleep(2)
            ActionChains(self.driver).send_keys(Keys.ENTER).perform()
            self.take_screenshot("09_Start_Over")
        except Exception as e:
            print(f"❌ Start Over error: {e}")

        if go_home_after:
            self.navigate_to_tool()

    def select_page_range_and_split(self, page_range="2-5"):
        try:
            # Select the "Select pages to split PDF" option
            range_radio = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "/html/body/section/div/div[1]/div[3]/div/div[2]/button[2]/div"
            )))
            range_radio.click()
            sleep(1)

            # Enter the page range
            range_input = self.wait.until(EC.presence_of_element_located((
                By.XPATH, "/html/body/section/div/div[2]/div/div/div/div/div/div/div[1]/div/div[2]/input"
            )))
            range_input.clear()
            range_input.send_keys(page_range)
            sleep(1)
            self.take_screenshot("10_Selected_Page_Range")

            # Click "Split PDF by Pages" button to generate download
            split_btn = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "/html/body/section/div/div[2]/div/div/div/div/div/div/div[2]/button"
            )))
            self.take_screenshot("11_Before_Final_Split")
            split_btn.click()
            sleep(4)
            download_btn1 = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "/html/body/div[5]/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]"
            )))
            download_btn1.click()
            start_over_btn1 = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "/html/body/div[5]/div[3]/div/div[2]/div[2]/div/div[2]/div/div[1]"
            )))
            start_over_btn1.click()
            sleep(2)
            self.take_screenshot("12_After_Final_Split")

        except Exception as e:
            print(f"❌ Page range split error: {e}")
