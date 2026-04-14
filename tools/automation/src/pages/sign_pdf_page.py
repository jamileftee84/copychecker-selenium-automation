import pyautogui
import math
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from tools.automation.src.pages.common_actions import CommonActions

class SignPDF:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.common = CommonActions(driver, wait, tool_name="Sign_PDF")

    def upload_pdf(self, file_path):
        try:
            file_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
            file_input.send_keys(file_path)
            sleep(3)
            self.common.take_screenshot("01_Uploaded")
        except Exception as e:
            print(f"❌ Upload failed: {e}")
            self.common.log_failure(f"Upload failed: {e}")

    def circle_mouse_and_click(self, center_x=200, center_y=300, radius=30, loops=1):
        """
        Moves the cursor in a small circular motion around (center_x, center_y) and clicks.
        """
        import math

        actions = ActionChains(self.driver)
        steps = 12  # points in circle

        for _ in range(loops):
            for angle in range(0, 360, int(360 / steps)):
                x = center_x + int(radius * math.cos(math.radians(angle)))
                y = center_y + int(radius * math.sin(math.radians(angle)))
                actions.move_by_offset(x - center_x, y - center_y).pause(0.1)
                center_x, center_y = x, y

        actions.click().perform()

    def draw_ellipse_on_canvas(self, canvas_xpath, margin=15, num_points=60):
        try:
            canvas = self.wait.until(EC.presence_of_element_located((By.XPATH, canvas_xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", canvas)
            sleep(1)

            width = canvas.size['width']
            height = canvas.size['height']

            center_x = width / 2
            center_y = height / 2
            radius_x = (width / 2) - margin
            radius_y = (height / 2) - margin

            angle_step = 2 * math.pi / num_points
            actions = ActionChains(self.driver)

            # Move to first point
            start_x = center_x + radius_x * math.cos(0)
            start_y = center_y + radius_y * math.sin(0)
            actions.move_to_element_with_offset(canvas, int(start_x), int(start_y)).click_and_hold()

            for i in range(1, num_points + 1):
                angle = i * angle_step
                x = center_x + radius_x * math.cos(angle)
                y = center_y + radius_y * math.sin(angle)
                safe_x = max(1, min(width - 2, int(x)))
                safe_y = max(1, min(height - 2, int(y)))
                actions.move_to_element_with_offset(canvas, safe_x, safe_y)

            actions.release().perform()
            print("Signature drawn successfully.")
            sleep(2)

        except Exception as e:
            print(f"❌ Failed to draw on canvas: {e}")
            self.common.log_failure(f"Canvas draw failed: {e}")

    def sign_with_type_tab(self):
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[3]/div/div/div/div/div[1]/div/div/div/button[1]'))).click()
            sleep(1)

            name_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[3]/div/div/div/div/div[2]/div/div[2]/input')))
            name_input.clear()
            name_input.send_keys("Test Signature")
            sleep(3)

            # Click each color
            for i in range(2, 9):
                color_btn = f'/html/body/div[4]/div[3]/div/div/div/div/div[2]/div/div[4]/div[{i}]/button'
                self.driver.find_element(By.XPATH, color_btn).click()
                sleep(1.5)


            save_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[3]/div/div/div/div/div[2]/div/div[10]/button')))
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", save_btn)
            save_btn.click()
            sleep(3)


            pdf_container_xpath = '/html/body/section/div[3]/div[2]/div[1]/div/div[2]/div/div[2]/div[2]/div/div/div/canvas'  # or use a div if canvas not used
            pdf_area = self.wait.until(EC.presence_of_element_located((By.XPATH, pdf_container_xpath)))

            # Move to center of element and click using ActionChains
            actions = ActionChains(self.driver)
            actions.move_to_element_with_offset(pdf_area, 50, 50).click().perform()  # Adjust offset as needed



            self.common.take_screenshot("02_Sign_Placed_Type")
        except Exception as e:
            print(f"❌ Type sign failed: {e}")
            self.common.log_failure(f"Type sign failed: {e}")

    def sign_with_draw_tab(self):
        try:
            # Open Sign > New Signature
            self.driver.find_element(By.XPATH, '/html/body/section/div[3]/div[1]/div/div[1]/button[2]').click()
            sleep(5)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/section/div[3]/div[1]/div/div[1]/div/div/ul/div[2]/div/button'))).click()
            sleep(5)

            # Select Draw tab
            self.driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/div/div/div/div/div[1]/div/div/div/button[2]').click()
            sleep(3)

            # Iterate through all 7 color buttons and draw with each
            canvas = self.driver.find_element(By.XPATH,
                                              '/html/body/div[4]/div[3]/div/div/div/div/div[3]/div/div[6]/canvas')
            for i in range(2, 9):
                color_btn = f'/html/body/div[4]/div[3]/div/div/div/div/div[3]/div/div[2]/div[2]/div[{i}]/button'
                self.driver.find_element(By.XPATH, color_btn).click()
                sleep(1)
                ActionChains(self.driver).move_to_element_with_offset(canvas, 10 + (i * 10),
                                                                      10).click_and_hold().move_by_offset(20,
                                                                                                          0).release().perform()
                sleep(1)

            # Locate Save button
            save_btn = self.driver.find_element(By.XPATH,
                                                '/html/body/div[4]/div[3]/div/div/div/div/div[3]/div/div[10]/button')
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", save_btn)
            save_btn.click()
            sleep(2)


            # Place on PDF
            self.circle_mouse_and_click(center_x=200, center_y=300, radius=20, loops=2)
            sleep(2)

            self.common.take_screenshot("03_Sign_Placed_Draw")
        except Exception as e:
            print(f"❌ Draw sign failed: {e}")
            self.common.log_failure(f"Draw sign failed: {e}")

    def sign_with_upload_image(self, image_path):
        try:

            # Open Sign > New Signature
            self.driver.find_element(By.XPATH, '/html/body/section/div[3]/div[1]/div/div[1]/button[2]').click()
            sleep(3)
            self.driver.find_element(By.XPATH, '/html/body/section/div[3]/div[1]/div/div[1]/div/div/ul/div[3]/div/button').click()
            sleep(3)

            # Step 2: Click Upload Image tab (this triggers the native OS file picker)
            self.driver.find_element(By.XPATH,
                                     '/html/body/div[4]/div[3]/div/div/div/div/div[1]/div/div/div/button[3]').click()
            sleep(2)

            # Step 3: Handle macOS native file picker using pyautogui
            pyautogui.write(image_path, interval=0.15)  # full path to image file
            sleep(1)
            pyautogui.press('return')
            sleep(2)
            pyautogui.press('return')
            sleep(5)  # wait for image to load

            # Click image preview multiple times to apply
            image_preview_xpath = '/html/body/div[4]/div[3]/div/div/div/div/div[4]/div/img'
            image_preview = self.wait.until(EC.presence_of_element_located((By.XPATH, image_preview_xpath)))
            for _ in range(3):
                image_preview.click()
                sleep(3)

            # Place on PDF
                # Wait and find the PDF area to click (you can improve this XPath if needed)
                pdf_container_xpath = '/html/body/section/div[3]/div[2]/div[1]/div/div[2]/div/div[2]/div[2]/div/div/div/canvas'  # or use a div if canvas not used
                pdf_area = self.wait.until(EC.presence_of_element_located((By.XPATH, pdf_container_xpath)))

                # Scroll into view and click center of it
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                           pdf_area)
                sleep(1)

                # Move to center of element and click using ActionChains
                actions = ActionChains(self.driver)
                actions.move_to_element_with_offset(pdf_area, 50, 50).click().perform()  # Adjust offset as needed
                sleep(2)

        except Exception as e:
            print(f"❌ Upload image sign failed: {e}")
            self.common.log_failure(f"Upload image sign failed: {e}")

    def finalize_and_download(self):
        try:
            self.driver.find_element(By.XPATH, '/html/body/section/div[2]/div/div/button').click()
            sleep(3)

            # Download
            self.driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/div/div/div[2]/div/div/div[3]/button[1]').click()
            sleep(5)

            # Back to editing
            self.driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/div/div/div[2]/div/div/div[3]/button[2]').click()
            sleep(3)

            self.common.take_screenshot("05_After_Download")
        except Exception as e:
            print(f"❌ Finalize/download failed: {e}")
            self.common.log_failure(f"Finalize/download failed: {e}")

    def click_new_and_reupload(self, file_path):
        try:
            self.driver.find_element(By.XPATH, '/html/body/section/div[3]/div[1]/div/div[1]/button[1]').click()
            sleep(2)

            self.driver.find_element(By.XPATH,'/html/body/div[4]/div[3]/div/button[1]').click()
            sleep(2)

            # Reupload
            self.upload_pdf(file_path)
            sleep(2)

            # Close popup
            cross_btn = self.driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/div/h2/span/svg')
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", cross_btn)
            cross_btn.click()
            sleep(2)
            
        except Exception as e:
            print(f"❌ New+Reupload flow failed: {e}")
            self.common.log_failure(f"New+Reupload flow failed: {e}")
