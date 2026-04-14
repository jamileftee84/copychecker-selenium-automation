import pyautogui
from time import sleep
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from tools.automation.src.pages.common_actions import CommonActions


class PDFEditorPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.common = CommonActions(driver, wait, tool_name="PDF_Editor")

    def upload_pdf(self, file_path):
        try:
            file_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
            file_input.send_keys(file_path)
            sleep(4)
            self.common.take_screenshot("03_PDF_Uploaded")
        except Exception as e:
            print(f"Upload failed: {e}")
            self.common.log_failure(f"Upload failed: {e}")

    def add_text_to_pdf(self):
        try:
            # Click Text tool
            text_button = '/html/body/section/div[3]/div[1]/div[1]/div/button[2]'
            self.wait.until(EC.element_to_be_clickable((By.XPATH, text_button))).click()
            sleep(2)

            # Click on canvas
            ActionChains(self.driver).move_by_offset(200, 300).click().perform()
            sleep(2)

            # Type some text
            ActionChains(self.driver).send_keys("Hello from automation!").perform()
            sleep(3)

            # Click Bold and Italic
            bold_xpath = '/html/body/section/div[3]/div[3]/div[1]/div/div[2]/div[2]/div/div[2]/div[1]/div[29]/div[1]/div/button[1]'
            italic_xpath = '/html/body/section/div[3]/div[3]/div[1]/div/div[2]/div[2]/div/div[2]/div[1]/div[29]/div[1]/div/button[2]/svg'
            bold_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, bold_xpath)))
            bold_btn.click()
            sleep(1)

            italic_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, italic_xpath)))
            italic_btn.click()
            sleep(1)

            self.common.take_screenshot("04_Text_Added")
        except Exception as e:
            print(f"Text tool failed: {e}")
            self.common.log_failure(f"Text tool failed: {e}")

    def add_image_to_pdf(self, image_path):
        try:
            # Click Image tab
            image_button = '/html/body/section/div[3]/div[1]/div[1]/div/button[3]'
            self.wait.until(EC.element_to_be_clickable((By.XPATH, image_button))).click()
            sleep(2)

            # Click New Image (dropdown)
            new_image_xpath = '/html/body/section/div[3]/div[1]/div[1]/div/div/div/ul/div/button'
            self.wait.until(EC.element_to_be_clickable((By.XPATH, new_image_xpath))).click()
            sleep(2)

            # Handle macOS native file picker using pyautogui
            pyautogui.write(image_path, interval=0.2)
            pyautogui.press('return')
            sleep(1)
            pyautogui.press('return')
            sleep(2)

            # Click on the PDF to place image
            pdf_container_xpath = '/html/body/section/div[3]/div[3]/div[1]/div/div[2]/div[2]/div/div[2]/div[1]/div[1]'  # or use a div if canvas not used
            pdf_area = self.wait.until(EC.presence_of_element_located((By.XPATH, pdf_container_xpath)))

            # Move to center of element and click using ActionChains
            actions = ActionChains(self.driver)
            actions.move_to_element_with_offset(pdf_area, 20, 50).click().perform()

            actions = ActionChains(self.driver)
            actions.move_to_element_with_offset(pdf_area, 20, 50).click().perform()

            self.common.take_screenshot("05_Image_Added")
        except Exception as e:
            print(f"Image upload failed: {e}")
            self.common.log_failure(f"Image upload failed: {e}")

    def add_signature_to_pdf(self, image_path=None):
        try:
            # Click Sign tab
            sign_button = '/html/body/section/div[3]/div[1]/div[1]/div/button[4]'
            self.driver.find_element(By.XPATH, sign_button).click()
            sleep(2)

            # Click New Signature
            new_sig_xpath = '/html/body/section/div[3]/div[1]/div[1]/div/div/div/ul/div/div/button'
            self.wait.until(EC.element_to_be_clickable((By.XPATH, new_sig_xpath))).click()
            sleep(2)

            # === TYPE TAB ===
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[12]/div[3]/div/div/div/div/div[1]/div/div/div/button[1]'))).click()
            name_input = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[12]/div[3]/div/div/div/div/div[2]/div/div[2]/input')))
            name_input.clear()
            name_input.send_keys("PDF Editor Signature")
            sleep(1)

            # Save
            save_btn = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[12]/div[3]/div/div/div/div/div[2]/div/div[10]/button')))
            save_btn.click()
            sleep(2)

            # Place signature on PDF
            canvas_xpath = '/html/body/section/div[3]/div[3]/div[1]/div/div[2]/div[2]/div/div[2]/div[2]/div/div/div'
            pdf_area = self.wait.until(EC.presence_of_element_located((By.XPATH, canvas_xpath)))
            ActionChains(self.driver).move_to_element_with_offset(pdf_area, 50, 20).click().perform()
            ActionChains(self.driver).move_to_element_with_offset(pdf_area, 50, 20).click().perform()
            sleep(2)

            self.common.take_screenshot("06_Sign_Type")

            # === DRAW TAB ===
            # Open Sign > New Signature
            self.driver.find_element(By.XPATH, '/html/body/section/div[3]/div[1]/div[1]/div/button[4]').click()
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/section/div[3]/div[1]/div[1]/div/div/div/ul/div[2]/div/button'))).click()
            sleep(2)

            # Click Draw tab
            self.driver.find_element(By.XPATH,
                                     '/html/body/div[12]/div[3]/div/div/div/div/div[1]/div/div/div/button[2]').click()
            sleep(1)

            # Draw simple line
            canvas = self.driver.find_element(By.XPATH,
                                              '/html/body/div[12]/div[3]/div/div/div/div/div[3]/div/div[6]/canvas')
            actions = ActionChains(self.driver)
            actions.move_to_element_with_offset(canvas, 10, 10)
            actions.click_and_hold()
            actions.pause(0.3)  # Wait before moving
            actions.move_by_offset(40, 0)  # Simulate drag right
            actions.pause(0.2)
            actions.move_by_offset(0, 20)  # Then drag down
            actions.release()
            actions.perform()
            sleep(1)

            # Save draw
            save_draw_btn = self.driver.find_element(By.XPATH,
                                                     '/html/body/div[12]/div[3]/div/div/div/div/div[3]/div/div[10]/button')
            save_draw_btn.click()
            sleep(2)

            # Place draw on PDF
            ActionChains(self.driver).move_to_element_with_offset(pdf_area, 10, 10).click().perform()
            ActionChains(self.driver).move_to_element_with_offset(pdf_area, 10, 10).click().perform()
            self.common.take_screenshot("07_Sign_Draw")
            sleep(2)

            # === UPLOAD IMAGE TAB ===
            if image_path:
                # Open Sign > New Signature again
                self.driver.find_element(By.XPATH, '/html/body/section/div[3]/div[1]/div[1]/div/button[4]').click()
                self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '/html/body/section/div[3]/div[1]/div[1]/div/div/div/ul/div[3]/div/button'))).click()
                sleep(2)

                # Click Upload Image tab
                self.driver.find_element(By.XPATH,
                                         '/html/body/div[12]/div[3]/div/div/div/div/div[1]/div/div/div/button[3]').click()
                sleep(2)

                # Upload via pyautogui
                pyautogui.write(image_path, interval=0.1)
                pyautogui.press('return')
                sleep(1)
                pyautogui.press('return')
                sleep(4)

                # Click preview
                preview_xpath = '/html/body/div[12]/div[3]/div/div/div/div/div[4]/div/img'
                preview = self.wait.until(EC.element_to_be_clickable((By.XPATH, preview_xpath)))
                preview.click()
                sleep(2)

                # Place image on PDF
                ActionChains(self.driver).move_to_element_with_offset(pdf_area, 30, 30).click().perform()
                ActionChains(self.driver).move_to_element_with_offset(pdf_area, 30, 30).click().perform()
                self.common.take_screenshot("08_Sign_Image")

        except Exception as e:
            print(f"Signature in PDF Editor failed: {e}")
            self.common.log_failure(f"Signature in PDF Editor failed: {e}")

    def finalize_and_download(self):
        try:
            # Apply Changes
            self.driver.find_element(By.XPATH, '/html/body/section/div[2]/div/div/button').click()
            sleep(3)

            # Download
            self.driver.find_element(By.XPATH,
                                     '/html/body/div[12]/div[3]/div/div/div[2]/div/div/div[3]/button[1]').click()
            sleep(5)

            # Back to editing
            self.driver.find_element(By.XPATH,
                                     '/html/body/div[12]/div[3]/div/div/div[2]/div/div/div[3]/button[2]').click()
            sleep(2)

            self.common.take_screenshot("06_Download_Complete")
        except Exception as e:
            print(f"Finalize/download failed: {e}")
            self.common.log_failure(f"Finalize/download failed: {e}")

    def search_and_open_pdf_editor(self):
        try:
            # Step 1: Click the search icon
            search_icon_xpath = '/html/body/header/div/div/div[2]/div[1]/span[1]/div/div[1]/img'
            search_icon = self.wait.until(EC.element_to_be_clickable((By.XPATH, search_icon_xpath)))
            self.common.take_screenshot("Search_Icon_Before_Click")
            search_icon.click()
            sleep(1)

            # Step 2: Type into the search input
            search_input_xpath = '/html/body/div[12]/div/div[1]/input'
            search_box = self.wait.until(EC.presence_of_element_located((By.XPATH, search_input_xpath)))
            self.common.take_screenshot("Search_Input_Before_Typing")
            search_box.send_keys("pdf editor")
            sleep(2)  # wait for dropdown results

            # Step 3: Press Enter to go to PDF Editor page
            search_box.send_keys(Keys.ENTER)
            self.common.take_screenshot("Search_After_Enter")
            sleep(3)

            print("Navigated to PDF Editor via search")

        except Exception as e:
            print(f"PDF Editor search failed: {e}")
            self.common.log_failure(f"Search PDF Editor failed: {e}")
