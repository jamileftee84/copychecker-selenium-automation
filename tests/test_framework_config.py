from pathlib import Path

import pytest

from tools.automation.main import TEST_REGISTRY
from tools.automation.src.config.settings import AUTOMATION_ROOT, IMAGE_DIR, PDF_DIR, URL


@pytest.mark.framework
def test_base_url_is_configurable():
    assert URL.startswith("http")


@pytest.mark.framework
def test_data_directories_exist():
    assert Path(AUTOMATION_ROOT).exists()
    assert Path(IMAGE_DIR).exists()
    assert Path(PDF_DIR).exists()


@pytest.mark.framework
def test_launcher_registry_contains_multiple_demo_flows():
    assert len(TEST_REGISTRY) >= 10
    assert "7" in TEST_REGISTRY
    assert TEST_REGISTRY["7"][0] == "PDF to Text"
