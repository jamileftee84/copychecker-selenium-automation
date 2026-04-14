from pathlib import Path

from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def find_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def scroll_into_view(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
            element,
        )

    @staticmethod
    def ensure_path(path_like) -> str:
        return str(Path(path_like).expanduser().resolve())
