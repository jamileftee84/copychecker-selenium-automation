import os
from time import sleep
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from tools.automation.src.settings import URL, IMAGE_DIR
from tools.automation.src.pages.common_actions import CommonActions

class EditPDFMetadataPage:
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

    def upload_pdf(self, filename, label="Image1"):
        try:
            file_path = os.path.join(IMAGE_DIR, filename)
            upload_container = self.wait.until(EC.presence_of_element_located((
                By.XPATH, "/html/body/section/div[1]/div[1]/div[5]/div/div/div/div[4]/div[1]/div/div/div"
            )))
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                       upload_container)

            file_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
            file_input.send_keys(os.path.abspath(file_path))

            self.take_screenshot(f"04_Upload_{label}")
            sleep(5)

        except Exception as e:
            print(f"❌ Upload failed: {e}")

    def remove_metadata_and_download(self):
        try:
            remove_btn = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "/html/body/section/div/div[1]/div[3]/div/div[2]/div[1]/div"
            )))
            remove_btn.click()
            sleep(3)
            self.take_screenshot("04_Removed_Metadata")

            rename_icon_xpath = "/html/body/div[5]/div[3]/div/div[2]/div[2]/div/div[1]/div/div[1]/img"
            rename_input_xpath = "/html/body/div[5]/div[3]/div/div[2]/div[2]/div/div[1]/div/div[2]/input"
            self.common.rename_before_download(rename_icon_xpath, rename_input_xpath, "Test_EditPDFMetaData1")

            sleep(2)

            self.common.click_download_and_start_over(
                download_xpath="/html/body/div[5]/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]",
                start_over_xpath="/html/body/div[5]/div[3]/div/div[2]/div[2]/div/div[2]/div/div[1]"
            )
        except Exception as e:
            print(f"❌ Remove metadata failed: {e}")

    def change_metadata_and_download(self):
        try:
            change_btn = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "/html/body/section/div/div[1]/div[3]/div/div[2]/div[2]/div"
            )))
            change_btn.click()
            sleep(5)
            self.take_screenshot("05_Change_Metadata_Selected")

            add_new_field = self.wait.until(EC.presence_of_element_located((By.XPATH,  "/html/body/section/div/div/div[3]/button[1]")))
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                       add_new_field)
            sleep(2)

            mod_date = self.wait.until(EC.presence_of_element_located((By.XPATH,  "/html/body/section/div/div/div[3]/div[8]/label")))
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                       mod_date)
            sleep(2)

            # Scroll to cross icon
            cross_icon = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "/html/body/section/div/div/div[3]/div[8]/button"
            )))
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", cross_icon)
            sleep(2)
            cross_icon.click()

            # Click Update Metadata
            update_btn = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "/html/body/section/div/div/div[3]/button[2]"
            )))
            update_btn.click()
            sleep(4)
            self.take_screenshot("06_Metadata_Updated")

            rename_icon_xpath = "/html/body/div[5]/div[3]/div/div[2]/div[2]/div/div[1]/div/div[1]/img"
            rename_input_xpath = "/html/body/div[5]/div[3]/div/div[2]/div[2]/div/div[1]/div/div[2]/input"
            self.common.rename_before_download(rename_icon_xpath, rename_input_xpath, "Test_EditPDFMetaData2")
            sleep(2)

            self.common.click_download_and_start_over(
                download_xpath="/html/body/div[5]/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]",
                start_over_xpath="/html/body/div[5]/div[3]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]",
                press_enter=True
            )

        except Exception as e:
            print(f"❌ Change metadata failed: {e}")
