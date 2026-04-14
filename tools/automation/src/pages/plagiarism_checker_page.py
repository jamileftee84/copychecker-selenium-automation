from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from tools.automation.src.pages.common_actions import CommonActions

class PlagiarismCheckerPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.common = CommonActions(driver, wait, tool_name="Plagiarism_Checker")

    def check_first_text(self, text="This is the first test for plagiarism. This is the first test for plagiarism."):
        try:
            # Enter text
            input_xpath = '/html/body/div[3]/div/div[4]/div/div/div[1]/textarea'
            input_box = self.wait.until(EC.element_to_be_clickable((By.XPATH, input_xpath)))
            input_box.clear()
            for char in text:
                input_box.send_keys(char)
                sleep(0.05)  # simulate human typing
            sleep(1)
            self.common.take_screenshot("01_Text_Entered")

            # Click "Check Plagiarism"
            check_btn = '/html/body/div[3]/div/div[5]/button'
            self.driver.find_element(By.XPATH, check_btn).click()
            sleep(8)
            self.common.take_screenshot("02_Report_Loaded")

        except Exception as e:
            print(f"First check failed: {e}")
            self.common.log_failure(f"First check failed: {e}")

    def interact_with_report(self):
        try:
            # Scroll to Copy button
            copy_btn_xpath = '/html/body/div[3]/div/div[6]/div[2]/div[1]/div[3]/div[3]/div[2]/div[3]/div'
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                       self.driver.find_element(By.XPATH, copy_btn_xpath))
            sleep(2)
            self.common.take_screenshot("03_Report_Visible")

            # Click "Check Grammar"
            grammar_btn_xpath = '/html/body/div[3]/div/div[6]/div[2]/div[1]/div[3]/div[3]/div[2]/div[3]/a[2]'
            self.driver.find_element(By.XPATH, grammar_btn_xpath).click()
            sleep(3)

            # Switch to new tab
            original_window = self.driver.current_window_handle
            windows = self.driver.window_handles
            for handle in windows:
                if handle != original_window:
                    self.driver.switch_to.window(handle)
                    break
            sleep(2)
            self.common.take_screenshot("04_Grammar_Tab")

            # Close new tab and switch back
            self.driver.close()
            self.driver.switch_to.window(original_window)
            sleep(2)

        except Exception as e:
            print(f"Report interaction failed: {e}")
            self.common.log_failure(f"Report interaction failed: {e}")

    def start_new_search(self, new_text="This is a new test to check again."):
        try:
            # Click Start New Search
            start_btn_xpath = '/html/body/div[3]/div/div[6]/div[2]/div[2]/div[1]/div/a'
            self.driver.find_element(By.XPATH, start_btn_xpath).click()
            sleep(2)

            # Click delete button
            delete_btn = '/html/body/div[3]/div/div[4]/div/div/div[1]/div/button'
            self.driver.find_element(By.XPATH, delete_btn).click()
            sleep(1)

            # Enter new text
            input_xpath = '/html/body/div[3]/div/div[4]/div/div/div[1]/textarea'
            input_box = self.wait.until(EC.element_to_be_clickable((By.XPATH, input_xpath)))
            input_box.clear()
            input_box.send_keys(new_text)
            sleep(1)

            # Click "Check Plagiarism" again
            check_btn = '/html/body/div[3]/div/div[5]/button'
            self.driver.find_element(By.XPATH, check_btn).click()
            sleep(8)
            self.common.take_screenshot("05_New_Report_Ready")
        except Exception as e:
            print(f"New search failed: {e}")
            self.common.log_failure(f"New search failed: {e}")

    def test_search_icon(self):
        try:
            # Click search icon
            search_icon_xpath = '/html/body/header/div/div/div[2]/div[1]/span[1]/div/div[1]/img'
            self.wait.until(EC.element_to_be_clickable((By.XPATH, search_icon_xpath))).click()
            sleep(2)

            # Enter 'plagiarism' and press Enter
            input_xpath = '/html/body/div[13]/div/div[1]/input'
            search_input = self.wait.until(EC.presence_of_element_located((By.XPATH, input_xpath)))
            search_input.send_keys("plagiarism")
            sleep(1)
            search_input.send_keys(Keys.ENTER)
            sleep(3)
            self.common.take_screenshot("06_Search_Done")
        except Exception as e:
            print(f"Search test failed: {e}")
            self.common.log_failure(f"Search test failed: {e}")
