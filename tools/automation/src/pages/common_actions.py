import time
from datetime import datetime
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from tools.automation.src.pages.base_page import BasePage
from tools.automation.src.config.settings import AUTOMATION_ROOT

class CommonActions(BasePage):
    def __init__(self, driver, wait, tool_name="DefaultTool"):
        super().__init__(driver, wait)
        self.tool_name = tool_name.replace(" ", "_").replace("-", "_") + "_SS"
        self.screenshot_dir = os.path.join(AUTOMATION_ROOT, "screenshots", self.tool_name)
        os.makedirs(self.screenshot_dir, exist_ok=True)
        self.fail_log_path = os.path.join(self.screenshot_dir, "fail_log.txt")

    def log_failure(self, message):
        with open(self.fail_log_path, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] {message}\n")
        print(f"Logged failure: {message}")

    def navigate_to_tool(self, homepage_url, tool_xpath, screenshot_label="Tool_Page"):
        self.driver.get(homepage_url)
        sleep(2)
        self.take_screenshot("01_Home")

        try:
            all_tools = self.wait.until(EC.presence_of_element_located((
                By.XPATH, '//*[@id="navigationBar"]/div/div/div[1]/div/div/button'
            )))
            ActionChains(self.driver).move_to_element(all_tools).perform()
            sleep(1)
        except Exception as e:
            print(f"⚠️ Could not hover All Tools: {e}")

        try:
            tool_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, tool_xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", tool_link)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, tool_xpath))).click()
            tool_link.click()
            sleep(2)
            self.take_screenshot(f"02_{screenshot_label}")
        except Exception as e:
            print(f"Could not click {screenshot_label}: {e}")
            self.take_screenshot(f"ERROR_{screenshot_label}")

    def timestamped(self, label):
        return os.path.join(self.screenshot_dir, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{label}.png")

    def take_screenshot(self, label):
        path = self.timestamped(label)
        self.driver.save_screenshot(path)
        print(f"Screenshot saved: {path}")

    def smooth_scroll(self):
        try:
            self.driver.execute_script("window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });")
            time.sleep(2)
            self.driver.execute_script("window.scrollTo({ top: 0, behavior: 'smooth' });")
            time.sleep(2)
            self.take_screenshot("Smooth_Scroll")
        except Exception as e:
            print(f"Smooth scroll failed: {e}")

    def click_download_and_start_over(self, download_xpath, start_over_xpath, press_enter=False):
        try:
            # Click Download button
            download_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, download_xpath)))
            self.take_screenshot("Before_Download")
            download_btn.click()
            time.sleep(2)
            self.take_screenshot("After_Download")
        except Exception as e:
            print(f"Download button click failed: {e}")

        try:
            # Click Start Over button
            start_over_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, start_over_xpath)))
            self.take_screenshot("Before_Start_Over")
            start_over_btn.click()
            time.sleep(1)

            # Press ENTER if required
            if press_enter:
                ActionChains(self.driver).send_keys(Keys.ENTER).perform()

            self.take_screenshot("After_Start_Over")

        except Exception as e:
            print(f"Start Over button click failed: {e}")

    def search_and_open_tool_by_name(self, tool_name: str):
        """
        Uses the header search to find and open a tool by typing its name.

        Args:
            tool_name (str): The name of the tool to search and open, e.g., "small", "pdf to word".
        """
        try:
            # ✅ Step 1: Click the search icon (magnifying glass)
            search_icon_xpath = "/html/body/header/div/div/div[2]/div[1]/span[1]/div/div/img"
            search_icon = self.wait.until(EC.element_to_be_clickable((By.XPATH, search_icon_xpath)))
            self.take_screenshot(f"{tool_name}_01_Before_Click_Search_Icon")
            search_icon.click()
            sleep(1)

            # ✅ Step 2: Type the tool name into the input box
            search_input_xpath = "/html/body/header/div/div/div[2]/div[1]/span[1]/div/div[1]/input"
            search_box = self.wait.until(EC.presence_of_element_located((By.XPATH, search_input_xpath)))
            self.take_screenshot(f"{tool_name}_02_Before_Type")
            search_box.send_keys(tool_name)
            sleep(2)  # Wait for dropdown to populate

            # ✅ Step 3: Press Enter to navigate
            search_box.send_keys(Keys.ENTER)
            self.take_screenshot(f"{tool_name}_03_After_Enter")
            sleep(3)  # Allow page to load

        except Exception as e:
            print(f"Search navigation failed for '{tool_name}': {e}")

    def rename_before_download(self, name_icon_xpath, input_box_xpath, new_name="Test_Tool"):
        """
        Clicks the name-change icon, clears the existing name, and sets a new name before downloading.
        Args:
            name_icon_xpath (str): XPath to the name edit icon
            input_box_xpath (str): XPath to the editable input box
            new_name (str): The new name to set (e.g., "Test_MergePDF")
        """
        try:
            self.take_screenshot("Before_Name_Edit_Click")

            # Step 1: Click the name edit icon
            name_icon = self.wait.until(EC.element_to_be_clickable((By.XPATH, name_icon_xpath)))
            name_icon.click()
            sleep(5)

            # Step 2: Wait for and clear the input box
            name_input = self.wait.until(EC.presence_of_element_located((By.XPATH, input_box_xpath)))
            name_input.send_keys(Keys.COMMAND + "a")  # or use Keys.COMMAND on macOS if needed
            name_input.send_keys(Keys.BACKSPACE)
            name_input.clear()
            sleep(1.5)

            # Step 3: Enter new name
            name_input.send_keys(new_name)
            sleep(5)
            self.take_screenshot("After_Name_Change")

        except Exception as e:
            self.take_screenshot("ERROR_Name_Edit")
            print(f"Rename before download failed: {e}")
            self.log_failure(f"Rename before download failed: {e}")
