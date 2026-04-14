
import os
from time import sleep
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from tools.automation.src.settings import IMAGE_DIR


class RemovePDFPagesPage:
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
        file_path = os.path.join(IMAGE_DIR, file_path)

        upload_container = self.wait.until(EC.presence_of_element_located((
            By.XPATH, "/html/body/section/div[1]/div[1]/div[4]/div/div/div/div[4]/div[1]/div/div/div"
        )))
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                   upload_container)

        file_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
        file_input.send_keys(os.path.abspath(file_path))
        self.take_screenshot("02_Uploaded_PDF")

    def enter_page_number_and_apply(self, page_number):
        input_box_xpath = '/html/body/section/div/div[4]/div/div/div/div[1]/div/div[2]/input'
        apply_btn_xpath = '/html/body/section/div/div[4]/div/div/div/div[2]/div'

        input_box = self.wait.until(EC.presence_of_element_located((By.XPATH, input_box_xpath)))
        input_box.clear()
        input_box.send_keys(str(page_number))
        self.take_screenshot("03_Page_Number_Entered")

        apply_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, apply_btn_xpath)))
        apply_btn.click()
        self.take_screenshot("04_Clicked_Apply")
        sleep(5)

    def click_download_and_restart(self):
        download_btn_xpath = '/html/body/div[5]/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]'
        restart_btn_xpath = '/html/body/div[5]/div[3]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]'

        download_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, download_btn_xpath)))
        download_btn.click()
        self.take_screenshot("05_Clicked_Download")
        sleep(5)

        restart_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, restart_btn_xpath)))
        restart_btn.click()
        self.take_screenshot("06_Clicked_Restart")
