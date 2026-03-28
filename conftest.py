"""
conftest.py — pytest’s special file: hooks and fixtures here are auto-discovered.

Flow for each UI test:
1) Session starts → `config` fixture loads Config/config.json + Env/.env once.
2) Each test → `driver` fixture opens Chrome, yields `driver`, then quits.
3) After a failed test → `pytest_runtest_makereport` saves a PNG and attaches Allure.

Upload fixtures (resume.pdf, photo.png) are created here if missing so CI does not depend
on a separate module that might be omitted from a push.
"""
import base64
import os
from datetime import datetime
from pathlib import Path

import allure
import pytest

from Core.ConfigLoader import ConfigLoader
from Core.DriverManager import DriverManager
from Utils.Logger import logger

_MINIMAL_PDF = b"""%PDF-1.1
1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj
2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj
3 0 obj<</Type/Page/MediaBox[0 0 200 200]/Parent 2 0 R>>endobj
xref
0 4
0000000000 65535 f
trailer<</Size 4/Root 1 0 R>>
startxref
130
%%EOF
"""
_MINIMAL_PNG_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
)


def _ensure_test_upload_files(test_data_dir: Path) -> None:
    """Create minimal resume.pdf / photo.png under TestData/ if absent (CI-safe)."""
    test_data_dir = Path(test_data_dir)
    test_data_dir.mkdir(parents=True, exist_ok=True)

    resume = test_data_dir / "resume.pdf"
    if not resume.is_file():
        resume.write_bytes(_MINIMAL_PDF)
        logger.info("Created minimal TestData asset: %s", resume)

    photo = test_data_dir / "photo.png"
    if not photo.is_file():
        photo.write_bytes(base64.b64decode(_MINIMAL_PNG_B64))
        logger.info("Created minimal TestData asset: %s", photo)


def pytest_sessionstart(session):
    """
    Jenkins/Git clones may omit binary fixtures; Chrome also rejects some paths with spaces.
    Ensure minimal resume.pdf / photo.png exist under TestData/ before any test runs.
    """
    root = Path(__file__).resolve().parent
    _ensure_test_upload_files(root / "TestData")


# -------------------------------------------------------
# FIXTURE: LOAD CONFIG ONCE
# -------------------------------------------------------
@pytest.fixture(scope="session")
def config():
    """
    Why:
    - Load config.json and .env only ONCE for entire test session.
    - Faster + simple + clean.

    What happens:
    - Create ConfigLoader instance and share it with all fixtures/tests.
    """
    return ConfigLoader()


# -------------------------------------------------------
# FIXTURE: CREATE DRIVER FOR EACH TEST
# -------------------------------------------------------
@pytest.fixture()
def driver(config):
    """
    Why:
    - Create a fresh browser for each test.
    - Avoids test dependency.

    What happens:
    - Start Chrome using DriverManager.
    - Yield driver to the test.
    - After test finishes → close browser.
    """
    manager = DriverManager(config)
    driver = manager.get_driver()

    yield driver  # provide driver to test

    logger.info("Closing browser after test...")
    manager.quit_driver()


# -------------------------------------------------------
# PYTEST HOOK: CAPTURE SCREENSHOT ON FAILURE
# -------------------------------------------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Why:
    - Detect when a test fails.
    - Capture screenshot.
    - Save screenshot to Screenshots/.
    - Attach screenshot to Allure report.

    What happens:
    - After each test, check its result.
    - If FAILED → capture screenshot.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        config = item.funcargs.get("config")

        if driver is None:
            return  # test had no driver fixture

        # ---------------------------------------------------
        # Prepare screenshot folder
        # ---------------------------------------------------
        screenshot_folder = Path(config.get_path("screenshots"))
        screenshot_folder.mkdir(exist_ok=True)

        # ---------------------------------------------------
        # Prepare screenshot file name (Option A)
        # Example: test_login_2026-03-27_12-30-10.png
        # ---------------------------------------------------
        test_name = item.name
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_name = f"{test_name}_{timestamp}.png"

        screenshot_path = screenshot_folder / screenshot_name

        # ---------------------------------------------------
        # Take screenshot
        # ---------------------------------------------------
        try:
            driver.save_screenshot(str(screenshot_path))
            logger.error(f"Screenshot saved: {screenshot_path}")

            # Attach screenshot to Allure report
            allure.attach.file(
                str(screenshot_path),
                name=screenshot_name,
                attachment_type=allure.attachment_type.PNG
            )

        except Exception as exc:
            logger.error(f"Failed to take screenshot: {exc}")

@pytest.fixture(scope="session")
def api_client():
    """
    Why:
    - API tests share one client with the same base URL and auth headers.

    What happens:
    - If ORANGEHRM_API_TOKEN is set, requests include Authorization: Bearer <token>.
    - TestAPI tests are skipped when the token is missing (see TestAPI/conftest.py).
    """
    from API.client import APIClient
    from API.endpoints import BASE_API

    token = os.getenv("ORANGEHRM_API_TOKEN")
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"} if token else {}
    return APIClient(BASE_API, default_headers=headers)