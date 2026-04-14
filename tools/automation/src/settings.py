import os
from pathlib import Path

AUTOMATION_ROOT = Path(__file__).resolve().parents[1]
URL = os.getenv("BASE_URL", "https://copychecker.com/")
IMAGE_DIR = str(AUTOMATION_ROOT / "data" / "images")
PDF_DIR = str(AUTOMATION_ROOT / "data" / "pdfs")
