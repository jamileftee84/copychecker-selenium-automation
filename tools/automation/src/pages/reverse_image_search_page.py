import os
from time import sleep
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from tools.automation.src.pages.common_actions import CommonActions

class ReverseImageSearchPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.common = CommonActions(driver, wait, tool_name="Reverse_Image_Search")

    def timestamped(self, label):
        return f"screenshots/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{label}.png"

    def take_screenshot(self, label):
        path = self.timestamped(label)
        self.driver.save_screenshot(path)
        print(f"📸 Screenshot saved: {path}")

    def upload_image(self, image_filename):
        """
        Uploads an image from the local data/images folder via file input.
        """
        try:
            image_path = os.path.abspath(os.path.join("data", "images", image_filename))
            file_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))

            # JS fallback in case file input is hidden
            self.driver.execute_script("arguments[0].style.display = 'block'; arguments[0].style.opacity = 1;",
                                       file_input)

            self.take_screenshot("03_Before_Upload")
            file_input.send_keys(image_path)
            sleep(2)
            self.take_screenshot("04_After_Upload")
            print(f"✅ Uploaded image: {image_path}")

        except Exception as e:
            print(f"❌ Image upload failed: {e}")
            self.common.log_failure(f"Image upload failed: {e}")
            self.take_screenshot("Error_Upload")

    def click_search_button(self):
        try:
            search_btn_xpath = "/html/body/section/div[1]/div[1]/div[3]/div[2]/div[3]/button"
            search_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, search_btn_xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });",
                                       search_btn)
            sleep(1)
            self.take_screenshot("05_Before_Search_Click")
            self.wait.until(EC.element_to_be_clickable((By.XPATH, search_btn_xpath))).click()
            sleep(4)
            self.take_screenshot("06_After_Search_Click")
        except Exception as e:
            print(f"❌ Search button click failed: {e}")
            self.common.log_failure(f"Search button click failed: {e}")

    def explore_filters(self):
        buttons = [
            ("/html/body/section/div[1]/div[1]/div[3]/div[2]/div[5]/div/div[1]/div[3]/div[2]/div[1]/div[1]/div[2]/a",
             "Google Matches")
        ]

        for xpath, label in buttons:
            try:
                original_window = self.driver.current_window_handle
                btn = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", btn)
                sleep(1)
                self.take_screenshot(f"07_BEFORE_{label.replace(' ', '_')}")
                self.driver.execute_script("arguments[0].click();", btn)
                sleep(3)

                self.wait.until(lambda d: len(d.window_handles) > 1)
                new_tabs = [w for w in self.driver.window_handles if w != original_window]

                if new_tabs:
                    self.driver.switch_to.window(new_tabs[0])
                    sleep(2)
                    self.take_screenshot(f"08_{label.replace(' ', '_')}_New_Tab")
                    self.driver.close()
                    self.driver.switch_to.window(original_window)
                    self.take_screenshot(f"09_AFTER_{label.replace(' ', '_')}")

            except Exception as e:
                print(f"❌ Filter navigation failed for {label}: {e}")
                self.common.log_failure(f"Filter button error ({label}): {e}")

    def click_start_over(self):
        try:
            reset_xpath = "/html/body/section/div[1]/div[1]/div[3]/div[2]/a"
            reset_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, reset_xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", reset_btn)
            sleep(1)
            self.take_screenshot("10_Before_Reset")
            self.wait.until(EC.element_to_be_clickable((By.XPATH, reset_xpath)))
            self.driver.execute_script("arguments[0].click();", reset_btn)
            sleep(2)
            self.take_screenshot("11_After_Reset")
        except Exception as e:
            print(f"❌ Reset button failed: {e}")
            self.common.log_failure(f"Reset failed: {e}")