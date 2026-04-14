# ai_reverse_image_smoke_email.py
import os
import sys
from time import sleep
import smtplib
import logging
import time
from datetime import datetime
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# =============== CONFIG (edit these) =================

# Option A (recommended): go straight to the tool
TOOL_URL = os.getenv("TOOL_URL", "https://copychecker.com/ai-reverse-image-search")

# Option B: (optional) navigate via homepage + menu click if TOOL_URL is blank
HOMEPAGE_URL = os.getenv("HOMEPAGE_URL", "https://copychecker.com/")
TOOL_NAV_XPATH = os.getenv(
    "TOOL_NAV_XPATH",
    "/html/body/div[1]/div/header/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div[2]/div[2]/ul/a[2]/span"
)

# File paths
IMAGE_PATH = os.getenv("IMAGE_PATH", "data/images/Majnu_bhai_art.png")
SCREENSHOT_DIR = os.getenv("SCREENSHOT_DIR", "screenshots/AI_Reverse_Image_Search")

# Upload <input type="file">
FILE_INPUT_XPATH = os.getenv("FILE_INPUT_XPATH", "//input[@type='file']")

# Consent popup checkboxes + active "Search with AI" button
CONSENT_CHECKBOX1_XPATH = os.getenv(
    "CONSENT_CHECKBOX1_XPATH",
    "/html/body/div[1]/section/div/div/div/div[1]/div[1]/div/div/div/div[2]/div[2]/label[1]/div/input"
)

CONSENT_CHECKBOX2_XPATH = os.getenv(
    "CONSENT_CHECKBOX2_XPATH",
    "/html/body/div[1]/section/div/div/div/div[1]/div[1]/div/div/div/div[2]/div[2]/label[2]/div/input"
)

SEARCH_WITH_AI_BUTTON_XPATH = os.getenv(
    "SEARCH_WITH_AI_BUTTON_XPATH",
    "/html/body/div[1]/section/div/div/div/div[1]/div[1]/div/div/div/div[3]/button"
)

# Result-page “success” marker — e.g. Show more button
SEARCH_NEW_XPATH = os.getenv(
    "SEARCH_NEW_XPATH",
    "/html/body/div[1]/section/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/button"
)

# Timing
EXPLICIT_WAIT_SEC      = int(os.getenv("EXPLICIT_WAIT_SEC", "20"))
POST_CLICK_WAIT_SEC    = int(os.getenv("POST_CLICK_WAIT_SEC", "2"))
SCREENSHOT_DELAY_SEC   = float(os.getenv("SCREENSHOT_DELAY_SEC", "1.5"))

# ⏳ Max time to give Cloudflare/reCAPTCHA + consent popup to appear
# (you can increase this via env, e.g. RECAPTCHA_WAIT_SEC=60)
RECAPTCHA_WAIT_SEC     = float(os.getenv("RECAPTCHA_WAIT_SEC", "45.0"))

# Email creds (use an App Password for Gmail)
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
EMAIL_TO = os.getenv("EMAIL_TO", "")

# Headless
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"

# Retry policy
MAX_RUNS = 2  # run once, and if not found, re-run from start once more

# =====================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S"
)

def ensure_dir(p: str):
    os.makedirs(p, exist_ok=True)

def now_tag() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def take_screenshot(driver, label: str) -> str:
    ensure_dir(SCREENSHOT_DIR)
    path = os.path.join(SCREENSHOT_DIR, f"{now_tag()}_{label}.png")
    driver.save_screenshot(path)
    logging.info("📸 Saved screenshot → %s", path)
    return path

def send_email(subject: str, body: str, attachments=None):
    if not SMTP_USER or not SMTP_PASS:
        logging.warning("SMTP creds missing. Skipping email send.")
        return

    msg = MIMEMultipart()
    msg["From"] = SMTP_USER
    msg["To"] = EMAIL_TO
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    for path in attachments or []:
        try:
            with open(path, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f'attachment; filename="{os.path.basename(path)}"')
            msg.attach(part)
        except Exception as e:
            logging.exception("Failed attaching %s: %s", path, e)

    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, EMAIL_TO.split(","), msg.as_string())
        logging.info("📧 Email sent to %s", EMAIL_TO)
    except Exception as e:
        logging.exception("Email send failed: %s", e)

def build_driver():
    chrome_opts = Options()
    if HEADLESS:
        chrome_opts.add_argument("--headless=new")
    chrome_opts.add_argument("--window-size=1366,900")
    chrome_opts.add_argument("--disable-gpu")
    chrome_opts.add_argument("--no-sandbox")
    chrome_opts.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_opts)
    driver.maximize_window()
    return driver

def go_to_tool(driver, wait):
    if TOOL_URL.strip():
        logging.info("🌐 Navigating to tool → %s", TOOL_URL)
        driver.get(TOOL_URL)
        return
    if not HOMEPAGE_URL or not TOOL_NAV_XPATH:
        raise RuntimeError("Provide TOOL_URL or HOMEPAGE_URL + TOOL_NAV_XPATH.")
    logging.info("🌐 Navigating via homepage → %s", HOMEPAGE_URL)
    driver.get(HOMEPAGE_URL)
    el = wait.until(EC.presence_of_element_located((By.XPATH, TOOL_NAV_XPATH)))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
    time.sleep(0.8)
    driver.execute_script("arguments[0].click();", el)

def upload_image(driver, wait, image_path: str):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    file_input = wait.until(EC.presence_of_element_located((By.XPATH, FILE_INPUT_XPATH)))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", file_input)
    time.sleep(0.5)
    file_input.send_keys(os.path.abspath(image_path))
    logging.info("📤 Uploaded image: %s", image_path)

def wait_for_consent_checkboxes(driver):
    """
    Polls for the consent checkboxes to appear for up to RECAPTCHA_WAIT_SEC.
    This gives Cloudflare/reCAPTCHA time to auto-validate the request.
    Returns (checkbox1_element, checkbox2_element) or raises TimeoutException.
    """
    logging.info("⏳ Waiting up to %.1f seconds for Cloudflare/reCAPTCHA + consent popup...", RECAPTCHA_WAIT_SEC)
    end = time.time() + RECAPTCHA_WAIT_SEC
    cb1 = cb2 = None

    while time.time() < end:
        try:
            cb1 = driver.find_element(By.XPATH, CONSENT_CHECKBOX1_XPATH)
            cb2 = driver.find_element(By.XPATH, CONSENT_CHECKBOX2_XPATH)
            if cb1.is_displayed() and cb2.is_displayed():
                logging.info("✅ Consent checkboxes appeared.")
                return cb1, cb2
        except Exception:
            # still waiting – captcha may still be solving
            pass

        time.sleep(1.5)

    raise TimeoutException(
        f"Consent checkboxes did not appear within {RECAPTCHA_WAIT_SEC} seconds. "
        "Cloudflare/reCAPTCHA may still be blocking automated traffic."
    )

def handle_consent_and_start_search(driver, wait):
    """
    Flow:
    - Wait up to RECAPTCHA_WAIT_SEC for consent checkboxes to show
    - Tick both checkboxes
    - Click 'Search with AI' button
    """
    try:
        cb1, cb2 = wait_for_consent_checkboxes(driver)

        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", cb1)
        time.sleep(0.5)

        # Click checkbox 1
        try:
            cb1.click()
        except Exception:
            driver.execute_script("arguments[0].click();", cb1)
        logging.info("☑️ First consent checkbox clicked")

        time.sleep(0.5)

        # Click checkbox 2
        try:
            cb2.click()
        except Exception:
            driver.execute_script("arguments[0].click();", cb2)
        logging.info("☑️ Second consent checkbox clicked")

        # Hide possible ad overlays before clicking
        try:
            driver.execute_script(
                "document.querySelectorAll('ins.adsbygoogle, .adsbygoogle, .ad, [id*=ad]').forEach(e=>e.style.display='none');"
            )
        except Exception:
            pass

        # Wait for "Search with AI" to be clickable
        search_ai_btn = WebDriverWait(driver, EXPLICIT_WAIT_SEC).until(
            EC.element_to_be_clickable((By.XPATH, SEARCH_WITH_AI_BUTTON_XPATH))
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", search_ai_btn)
        time.sleep(0.5)

        try:
            search_ai_btn.click()
        except Exception:
            driver.execute_script("arguments[0].click();", search_ai_btn)
        logging.info("🔎 Clicked 'Search with AI' button")

    except TimeoutException as e:
        logging.error("Consent popup / checkboxes not found in time: %s", e)
        raise
    except Exception as e:
        logging.error("Error while handling consent popup: %s", e)
        raise

def wait_for_results(driver, wait) -> bool:
    """
    Returns True if the specific result marker (SEARCH_NEW_XPATH) appears, else False.
    Typically this is the 'Show more' button on the results page.
    """
    if not SEARCH_NEW_XPATH:
        raise RuntimeError("SEARCH_NEW_XPATH must be provided.")

    end = time.time() + EXPLICIT_WAIT_SEC
    while time.time() < end:
        try:
            el = driver.find_element(By.XPATH, SEARCH_NEW_XPATH)
            if el and el.is_displayed():
                logging.info("✅ Result marker found: %s", SEARCH_NEW_XPATH)
                return True
        except Exception:
            pass
        time.sleep(0.75)

    logging.error("⏰ Timed out waiting for result marker: %s", SEARCH_NEW_XPATH)
    return False

def run_once(run_index: int) -> tuple[bool, str | None, str | None]:
    """
    Executes a full smoke run.
    Returns (ok, screenshot_path, error_text).
    """
    driver = None
    screenshot_path = None
    try:
        driver = build_driver()
        wait = WebDriverWait(driver, EXPLICIT_WAIT_SEC)

        # 1) Go to tool
        go_to_tool(driver, wait)

        # 2) Upload image
        upload_image(driver, wait, IMAGE_PATH)
        time.sleep(POST_CLICK_WAIT_SEC)

        # 3) Wait for Cloudflare/reCAPTCHA + consent popup, then click "Search with AI"
        handle_consent_and_start_search(driver, wait)

        # 4) Wait for specific result marker (e.g., Show more via SEARCH_NEW_XPATH)
        ok = wait_for_results(driver, wait)

        # 5) Screenshot (label includes run index and status)
        time.sleep(SCREENSHOT_DELAY_SEC + 15)  # allow UI to settle, results load
        label = f"RUN{run_index}_{'OK' if ok else 'FAIL'}"
        screenshot_path = take_screenshot(driver, label)

        return ok, screenshot_path, None
    except Exception as e:
        logging.exception("Run %d crashed: %s", run_index, e)
        try:
            if driver:
                screenshot_path = take_screenshot(driver, f"RUN{run_index}_CRASH")
        except Exception:
            pass
        return False, screenshot_path, str(e)
    finally:
        if driver:
            driver.quit()

def main():
    attachments = []
    overall_ok = False
    errors = []

    # First run
    ok1, shot1, err1 = run_once(run_index=1)
    if shot1:
        attachments.append(shot1)
    if err1:
        errors.append(f"[Run 1] {err1}")

    # Retry once from the VERY START if not ok
    if not ok1 and MAX_RUNS > 1:
        logging.info("🔁 Result marker not found. Retrying full flow (1 retry)...")
        time.sleep(2.0)
        ok2, shot2, err2 = run_once(run_index=2)
        if shot2:
            attachments.append(shot2)
        if err2:
            errors.append(f"[Run 2] {err2}")
        overall_ok = ok2
    else:
        overall_ok = ok1

    # Email
    url_line = f"URL: {TOOL_URL or HOMEPAGE_URL}\n"
    if overall_ok:
        subject = "✅ Your site is working — AI Reverse Image Search"
        body = (
            "Hi Team,\n\n"
            "Smoke test succeeded. The AI Reverse Image Search result page appeared "
            f"(found the button at {SEARCH_NEW_XPATH}).\n\n"
            f"{url_line}"
            "Regards,\nSmokeBot"
        )
    else:
        subject = "⛔ Alert: AI Reverse Image Search may be down"
        body = (
            "Hi Team,\n\n"
            "Smoke test failed to detect the expected result button after two full runs.\n"
            f"Checked XPATH:\n{SEARCH_NEW_XPATH}\n\n"
            f"{url_line}"
            "Please investigate. Screenshots attached.\n\n"
            "Errors (if any):\n" + ("\n".join(errors) if errors else "None") +
            "\n\nRegards,\nSmokeBot"
        )

    send_email(subject, body, attachments=attachments)

if __name__ == "__main__":
    main()
