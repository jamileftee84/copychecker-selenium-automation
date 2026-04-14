import os
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from tools.automation.src.pages.common_actions import CommonActions

class SmallTextPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.common = CommonActions(driver, wait, tool_name="Small_Text_Generator")

    def enter_text(self, input_text):
        textbox_xpath = "/html/body/section/div[1]/div/div[1]/div[4]/div/div[1]/textarea"
        textbox = self.wait.until(EC.presence_of_element_located((By.XPATH, textbox_xpath)))
        self.common.take_screenshot("BEFORE_Input_Text")
        textbox.clear()
        sleep(1.5)
        textbox.send_keys(input_text)
        sleep(3.5)
        self.common.take_screenshot("AFTER_Input_Text")

    def preview_each_style(self):
        try:
            preview_all_xpath = "/html/body/section/div[1]/div/div[2]/div[1]/div/button[2]/span"
            preview_all_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, preview_all_xpath)))
            self.common.take_screenshot("BEFORE_Preview_All")
            preview_all_btn.click()
            sleep(3.5)

            self.common.take_screenshot("AFTER_Preview_All")

            close_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[7]/div[3]/div/div[1]/div/div[2]/img")))
            self.common.take_screenshot("CLOSE_Preview_All")
            close_btn.click()
            sleep(2)

        except Exception as e:
            print(f"❌ Preview All failed: {e}")
            self.common.log_failure(str(e))

    def click_copy_and_download(self):
        try:
            ActionChains(self.driver).move_by_offset(-500, -300).click().perform()
            sleep(2)
            self.common.take_screenshot("Clicked_Before_Copy")

            copy_btn_xpath = "/html/body/section/div[1]/div/div[2]/div[2]/div/div[3]/div[1]/button"
            copy_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, copy_btn_xpath)))
            self.common.take_screenshot("BEFORE_Copy")
            copy_btn.click()
            sleep(2)
            self.common.take_screenshot("AFTER_Copy")

            ActionChains(self.driver).move_by_offset(300, 400).click().perform()
            sleep(2)
            self.common.take_screenshot("Clicked_After_Copy")

        except Exception as e:
            print(f"❌ Copy failed: {e}")
            self.common.log_failure(str(e))

        try:
            download_btn_xpath = "/html/body/section/div[1]/div/div[2]/div[1]/div/button[1]"
            download_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, download_btn_xpath)))
            self.common.take_screenshot("BEFORE_Download")
            download_btn.click()
            sleep(2)

            ActionChains(self.driver).send_keys(Keys.ENTER).perform()
            sleep(2)
            self.common.take_screenshot("AFTER_Download")

        except Exception as e:
            print(f"❌ Download failed: {e}")
            self.common.log_failure(str(e))
