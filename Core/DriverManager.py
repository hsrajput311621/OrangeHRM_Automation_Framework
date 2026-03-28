"""
DriverManager — builds the Selenium Chrome WebDriver used by every UI test.

Step-by-step (what happens when tests run):
1) Pytest starts and loads `conftest.py`.
2) The `driver` fixture creates a `DriverManager` and calls `get_driver()`.
3) This file reads flags from `config.json` (headless, incognito, etc.).
4) Selenium 4.6+ includes **Selenium Manager**, which picks or fetches a matching
   ChromeDriver for the installed Chrome (more reliable than older tools on Win64).
5) Chrome starts with those options and returns the `driver` object.
6) After the test, `quit_driver()` closes the browser to free memory.
"""
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from Core.ConfigLoader import ConfigLoader
from Utils.Logger import logger


class DriverManager:
    """
    Creates and tears down one Chrome browser instance per test (via pytest fixture).
    """

    def __init__(self, config: ConfigLoader):
        # Keep a reference to config so we can read timeouts and browser flags.
        self.config = config
        self.driver = None

    def get_driver(self):
        """
        Why use this:
        - UI tests need a real browser controlled by Selenium.

        What happens:
        1) Build ChromeOptions (window size, headless, stability flags for CI).
        2) Start Chrome (Selenium Manager resolves ChromeDriver automatically).
        3) Set implicit wait and page-load timeout from config.json.
        4) Return the WebDriver so tests can call driver.get(), find_element(), etc.
        """
        logger.info("Starting Chrome browser...")

        chrome_options = Options()

        # --- Browser behaviour from config.json + CI ---
        # Headless: no GUI. We turn it on when config says so, or on CI (GitHub Actions /
        # many Jenkins Linux agents) where there is no physical display for Chrome.
        use_headless = bool(self.config.get("headless"))
        if os.getenv("CI") == "true" or os.getenv("GITHUB_ACTIONS") == "true":
            use_headless = True
        if use_headless:
            chrome_options.add_argument("--headless=new")

        # Private mode: clean session, fewer extensions interfering with tests.
        if self.config.get("incognito"):
            chrome_options.add_argument("--incognito")

        if self.config.get("disable_notifications"):
            chrome_options.add_argument("--disable-notifications")

        if self.config.get("start_maximized"):
            chrome_options.add_argument("--start-maximized")

        # Jenkins / Docker / many Linux agents: Chrome needs these or it crashes
        # (sandbox and /dev/shm issues). Safe to keep on Windows too.
        if os.getenv("CI") == "true" or os.getenv("JENKINS_URL"):
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")

        # Makes automation slightly less obvious to some sites (not security-relevant).
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)

        # --- Start Chrome (no explicit Service path) ---
        # Selenium Manager (built into Selenium 4.6+) matches ChromeDriver to your Chrome.
        # We avoid webdriver-manager here: on 64-bit Windows it can fetch a win32 driver
        # zip and trigger WinError 193 ("not a valid Win32 application").
        self.driver = webdriver.Chrome(options=chrome_options)

        logger.info("Chrome browser started successfully.")

        # Implicit wait: how long Selenium polls when you use find_element before failing.
        # 0 is common with explicit WebDriverWait (see BasePage).
        self.driver.implicitly_wait(self.config.get_timeout("implicit_wait"))

        # Page load: max seconds to wait for document.ready after driver.get(url).
        page_load = self.config.get_timeout("page_load_timeout")
        if page_load is not None:
            self.driver.set_page_load_timeout(float(page_load))

        return self.driver

    def quit_driver(self):
        """
        Why: Browsers consume RAM; quitting avoids leaks when many tests run in Jenkins.

        What happens: closes all windows and ends the WebDriver session.
        """
        if self.driver:
            logger.info("Closing Chrome browser...")
            self.driver.quit()
            self.driver = None
