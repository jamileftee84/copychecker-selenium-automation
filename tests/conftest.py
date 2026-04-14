import os
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


ROOT_DIR = Path(__file__).resolve().parents[1]


def _env_flag(name: str, default: str = "0") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("BASE_URL", "https://copychecker.com/")


@pytest.fixture(scope="session")
def test_data_dir() -> Path:
    return ROOT_DIR / "tools" / "automation" / "data"


@pytest.fixture(scope="session")
def image_dir(test_data_dir: Path) -> Path:
    return test_data_dir / "images"


@pytest.fixture(scope="session")
def pdf_dir(test_data_dir: Path) -> Path:
    return test_data_dir / "pdfs"


@pytest.fixture(scope="session")
def driver():
    if not _env_flag("RUN_UI_TESTS"):
        pytest.skip("Set RUN_UI_TESTS=1 to run browser-based tests.")

    options = Options()
    if _env_flag("HEADLESS", "1"):
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1080")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    browser = webdriver.Chrome(options=options)
    browser.maximize_window()
    yield browser
    browser.quit()


@pytest.fixture(scope="function")
def wait(driver):
    return WebDriverWait(driver, int(os.getenv("SELENIUM_WAIT_SECONDS", "15")))
