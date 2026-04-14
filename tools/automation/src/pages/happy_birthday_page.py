import os
from time import sleep
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from tools.automation.src.settings import URL

class HappyBirthdayFontsPage:
    """
    Page Object Model class for automating the Happy Birthday Fonts tool
    located on the CopyChecker platform.
    """

    def __init__(self, driver, wait):
        """
        Initializes the page object.
        :param driver: Selenium WebDriver instance
        :param wait: WebDriverWait instance
        """
        self.driver = driver
        self.wait = wait
        os.makedirs("screenshots", exist_ok=True)

    def timestamped(self, label):
        """Returns a timestamped filename for screenshot saving."""
        return f"screenshots/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{label}.png"

    def take_screenshot(self, label):
        """Takes a screenshot and prints confirmation."""
        path = self.timestamped(label)
        self.driver.save_screenshot(path)
        print(f"📸 Screenshot saved: {path}")

    def go_to_tool(self):
        """
        Navigates from homepage to Happy Birthday Fonts tool using the nav menu.
        """
        self.driver.get(URL)
        sleep(2)
        self.take_screenshot("BEFORE_Nav_HappyBirthday")

        try:
            # Hover over 'All Tools' to reveal dropdown
            all_tools = self.wait.until(EC.presence_of_element_located((
                By.XPATH, '//*[@id="navigationBar"]/div[1]/div[1]/div[1]/div[1]/div[1]/button[1]/span[1]'
            )))
            ActionChains(self.driver).move_to_element(all_tools).perform()
            sleep(1)

            # Click on Happy Birthday Fonts link
            tool_link = self.wait.until(EC.presence_of_element_located((
                By.XPATH, "/html/body/header/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div[2]/div[1]/ul/a[6]"
            )))
            self.driver.execute_script("arguments[0].click();", tool_link)
            sleep(2)
            self.take_screenshot("AFTER_Nav_HappyBirthday")

        except Exception as e:
            print(f"❌ Navigation to Happy Birthday Fonts failed: {e}")
            self.take_screenshot("ERROR_Nav_HappyBirthday")

    def scroll_to_start_button_and_click(self):
        """Scrolls to 'Start Writing Your Message' button and clicks it."""
        try:
            start_btn = self.wait.until(EC.presence_of_element_located((
                By.XPATH, "/html/body/section/div[4]/div"
            )))

            # Smooth scroll effect
            total_height = self.driver.execute_script("return document.body.scrollHeight")
            for y in range(0, total_height, 300):
                self.driver.execute_script(f"window.scrollTo(0, {y});")
                sleep(0.3)

            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'});", start_btn)
            sleep(5)
            self.take_screenshot("BEFORE_Click_StartWriting")
            self.driver.execute_script("arguments[0].click();", start_btn)
            sleep(2)
            self.take_screenshot("AFTER_Click_StartWriting")

        except Exception as e:
            print(f"❌ Start Writing button click failed: {e}")

    def enter_message(self):
        """Enters a predefined message into the input textarea."""
        try:
            textarea_xpath = "/html/body/section/div[2]/div[1]/div/div/div[1]/textarea"
            input_box = self.wait.until(EC.presence_of_element_located((By.XPATH, textarea_xpath)))

            self.driver.execute_script("arguments[0].scrollIntoView(true);", input_box)
            sleep(3)
            input_box.click()

            self.take_screenshot("BEFORE_Enter_Text")

            message = "Happy Birthday to the most amazing person in the world!"
            input_box.clear()
            input_box.send_keys(message)

            sleep(3)
            self.take_screenshot("AFTER_Enter_Text")

        except Exception as e:
            print(f"❌ Input failed: {e}")

    def click_all_preview(self):
        """Clicks the All Preview button and closes the resulting modal."""
        try:
            btn = self.wait.until(EC.presence_of_element_located((
                By.XPATH, "/html/body/section/div[2]/div[3]/div[1]/button"
            )))
            sleep(1)
            self.take_screenshot("BEFORE_All_Preview")
            self.driver.execute_script("arguments[0].click();", btn)
            sleep(3)
            self.take_screenshot("AFTER_All_Preview")

            # Close modal
            close_btn = self.wait.until(EC.presence_of_element_located((
                By.XPATH, "/html/body/div[6]/div[3]/div/div[1]/div/div[2]/img"
            )))
            sleep(1)
            self.take_screenshot("BEFORE_Close_All_Preview")
            self.driver.execute_script("arguments[0].click();", close_btn)
            sleep(2)
            self.take_screenshot("AFTER_Close_All_Preview")

        except Exception as e:
            print(f"❌ All Preview modal interaction failed: {e}")

    def copy_all_fonts(self):
        """
        Iterates through the available font styles and clicks copy on each.
        Returns a sample copied message string.
        """
        try:
            copied_text = ""
            copy_buttons = self.driver.find_elements(By.XPATH,
                "/html/body/section/div[2]/div[3]/div[2]/div[23]/div[1]/div[2]/button")

            for i, btn in enumerate(copy_buttons[:20]):
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                    sleep(1.5)
                    self.take_screenshot(f"BEFORE_Copy_Font_{i + 1}")
                    self.driver.execute_script("arguments[0].click();", btn)
                    sleep(2)
                    self.take_screenshot(f"AFTER_Copy_Font_{i + 1}")

                    if i == 0:
                        copied_text = "Sample Copied Birthday Text"
                except Exception as e:
                    print(f"❌ Failed to copy font {i + 1}: {e}")
            return copied_text

        except Exception as e:
            print(f"❌ Copy buttons not found: {e}")
            return ""

    def clear_input(self):
        """
        Clears the text in the input box using the clear/delete button.
        Assumes the button is already in view or fixed on the screen.
        """
        try:
            clear_btn = self.driver.find_element(
                By.XPATH, "/html/body/section/div[2]/div[1]/div/div/div[1]/div/button"
            )

            sleep(2)  # Optional pause to ensure page is stable
            self.take_screenshot("BEFORE_Clear")

            self.driver.execute_script("arguments[0].click();", clear_btn)

            sleep(5)  # Wait after clearing to observe any UI reflow
            self.take_screenshot("AFTER_Clear")

        except Exception as e:
            print(f"❌ Clear input failed: {e}")

    def paste_text_back(self, message):
        """Pastes a message back into the input box after clearing it."""
        try:
            textarea_xpath = "/html/body/section/div[2]/div[1]/div/div/div[1]/textarea"
            input_box = self.wait.until(EC.presence_of_element_located((By.XPATH, textarea_xpath)))

            self.driver.execute_script("arguments[0].scrollIntoView(true);", input_box)
            sleep(3)
            input_box.click()

            self.take_screenshot("BEFORE_Paste_Back")

            message = "Happy Birthday! Wishing you joy, love, and surprises!"
            input_box.clear()
            input_box.send_keys(message)

            sleep(3)
            self.take_screenshot("AFTER_Paste_Back")

        except Exception as e:
            print(f"❌ Paste back failed: {e}")
