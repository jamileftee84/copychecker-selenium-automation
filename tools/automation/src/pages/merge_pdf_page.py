import os
from time import sleep
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from tools.automation.src.settings import URL, IMAGE_DIR

class MergePDFPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        os.makedirs("screenshots", exist_ok=True)

    def timestamped(self, label):
        return f"screenshots/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{label}.png"

    def take_screenshot(self, label):
        path = self.timestamped(label)
        self.driver.save_screenshot(path)
        print(f"Screenshot saved: {path}")

    def navigate_to_tool(self):
        self.driver.get(URL)
        sleep(2)
        self.take_screenshot("01_Home")

        try:
            all_tools = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="navigationBar"]/div[1]/div[1]/div[1]/div[1]/div[1]/button[1]')
            ))
            ActionChains(self.driver).move_to_element(all_tools).perform()
            sleep(1)

            merge_tool = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/header/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div[1]/ul/a[9]")
            ))
            merge_tool.click()
            sleep(2)
            self.take_screenshot("02_Tool_Page")
        except Exception as e:
            print(f"❌ Navigation error: {e}")

    def upload_pdfs(self, filename1, filename2, label="Both"):
        try:
            file_path1 = os.path.join(IMAGE_DIR, filename1)
            file_path2 = os.path.join(IMAGE_DIR, filename2)

            upload_container = self.wait.until(EC.presence_of_element_located((
                By.XPATH, "/html/body/section/div[1]/div[1]/div[5]/div/div/div/div[4]/div[1]/div/div/div"
            )))
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                upload_container
            )

            file_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
            full_path1 = os.path.abspath(file_path1)
            full_path2 = os.path.abspath(file_path2)

            file_input.send_keys(f"{full_path1}\n{full_path2}")
            self.take_screenshot(f"04_Upload_{label}")
            sleep(5)
        except Exception as e:
            print(f"Upload error: {e}")

    def click_views(self):
        try:
            pages_view = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/section/div/div[1]/div[2]/div[2]/div/div/div[1]/div")
            ))
            pages_view.click()
            self.take_screenshot("05_Pages_View")
            sleep(2)

            files_view = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/section/div/div[1]/div[2]/div[2]/div/div/div[2]/div")
            ))
            files_view.click()
            self.take_screenshot("06_Files_View")
            sleep(2)

        except Exception as e:
            print(f"View buttons error: {e}")

    def zoom_in_out(self, times=15):
        try:
            zoom_in = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/section/div/div[1]/div[2]/div[4]/div/div/button[2]")
            ))
            for i in range(times):
                zoom_in.click()
                sleep(0.3)
            self.take_screenshot("07_Zoomed_In")

            zoom_out = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/section/div/div[1]/div[2]/div[4]/div/div/button[1]")
            ))
            for i in range(times):
                zoom_out.click()
                sleep(0.3)
            self.take_screenshot("08_Zoomed_Out")

        except Exception as e:
            print(f"Zoom error: {e}")

    def merge_and_download(self):
        try:
            merge_btn = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/section/div/div[3]/div/div[2]/div/button")
            ))
            merge_btn.click()
            sleep(5)
            self.take_screenshot("09_Merge_Clicked")

            download_btn = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[4]/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]")
            ))
            download_btn.click()
            self.take_screenshot("10_Downloaded")
            sleep(2)

        except Exception as e:
            print(f"Merge/download error: {e}")

    def back_to_editing(self):
        try:
            back_to_editing_btn = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[5]/div[3]/div/div[2]/div[2]/div/div[2]/div/div[1]")
            ))
            back_to_editing_btn.click()
            sleep(5)
            ActionChains(self.driver).send_keys(Keys.ENTER).perform()
            self.take_screenshot("11_Back_to_Editing")
        except Exception as e:
            print(f"Start Over error: {e}")
