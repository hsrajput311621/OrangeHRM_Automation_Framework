from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager .chrome import ChromeDriverManager
from pathlib import Path
from Core.ConfigLoader import ConfigLoader
#from Utils.Logger import logger

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager

from pathlib import Path
from Core.ConfigLoader import ConfigLoader
from Utils.Logger import logger


class DriverManager:
    """
    This class is responsible for creating the Chrome browser.
    It reads all settings from config.json using ConfigLoader.
    """

    def __init__(self, config: ConfigLoader):
        # store config for use
        self.config = config
        self.driver = None

    def get_driver(self):
        """
        Why this step:
        - We need a browser to run our tests.
        - This function will create and return the Chrome browser.

        What will happen:
        - Create Chrome options (headless, incognito)
        - Start Chrome using webdriver_manager
        - Apply timeouts
        - Maximize window
        """

        logger.info("Starting Chrome browser...")

        chrome_options = Options()

        # --------------------------------------------------------
        # Apply browser options from config.json
        # --------------------------------------------------------

        if self.config.get("headless"):
            chrome_options.add_argument("--headless=new")  # modern headless

        if self.config.get("incognito"):
            chrome_options.add_argument("--incognito")

        if self.config.get("disable_notifications"):
            chrome_options.add_argument("--disable-notifications")

        if self.config.get("start_maximized"):
            chrome_options.add_argument("--start-maximized")

        # Remove automation flags
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)

        # --------------------------------------------------------
        # Start Chrome using webdriver_manager (auto-download)
        # --------------------------------------------------------

        try:
            self.driver = webdriver.Chrome(options=chrome_options)
        except Exception as exc:
            raise Exception(f"Error launching Chrome browser: {exc}")

        logger.info("Chrome browser started successfully.")

        # --------------------------------------------------------
        # Apply timeouts
        # --------------------------------------------------------

        # IMPORTANT: You selected implicit_wait = 0 (modern best practice)
        self.driver.implicitly_wait(self.config.get_timeout("implicit_wait"))
        return self.driver

    def quit_driver(self):
        """
        Why this step:
        - To properly close the browser after tests.
        - Prevents memory leaks.

        What will happen:
        - If browser is open → close it.
        """
        if self.driver:
            logger.info("Closing Chrome browser...")
            self.driver.quit()
