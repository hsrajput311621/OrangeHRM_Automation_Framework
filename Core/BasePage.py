import os
import shutil
import tempfile

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException

from Utils.Logger import logger


class BasePage:
    """
    BasePage:
    This class contains all common functions that every page will use.
    Example: click, type text, wait, scroll, highlight element etc.

    Every page (LoginPage, DashboardPage…) will inherit from BasePage.
    """

    def __init__(self, driver, config):
        self.driver = driver
        self.config = config
        self.wait = WebDriverWait(
            driver,
            config.get_timeout("explicit_wait")
        )

    # OrangeHRM shows a full-screen-ish overlay while forms load/save.
    FORM_LOADER = (By.CSS_SELECTOR, "div.oxd-form-loader")

    def wait_for_no_form_loader(self):
        """
        Wait until the OXD form loader is gone so clicks are not intercepted.
        If no loader is present, returns immediately.
        """
        try:
            self.wait.until(EC.invisibility_of_element_located(self.FORM_LOADER))
        except TimeoutException:
            logger.warning("oxd-form-loader still visible after explicit wait")

    # ----------------------------------------------------------------
    # HIGHLIGHT ELEMENT (YELLOW)
    # ----------------------------------------------------------------
    def highlight(self, element):
        """
        Why this step:
        - Helps you SEE which element Selenium is interacting with.
        - Very useful for learning + debugging.

        What will happen:
        - A yellow border appears around the element for a moment.
        """
        try:
            self.driver.execute_script(
                "arguments[0].style.border='3px solid yellow'", element
            )
        except Exception as exc:
            logger.warning(f"Could not highlight element: {exc}")

    # ----------------------------------------------------------------
    # FIND ELEMENT
    # ----------------------------------------------------------------
    def find(self, locator: tuple):
        """
        Why this step:
        - This method finds an element on the page safely.

        What will happen:
        - Wait for element to be visible.
        - Highlight it.
        - Return the element.
        """
        element = self.wait.until(
            EC.visibility_of_element_located(locator)
        )
        self.highlight(element)
        return element

    # ----------------------------------------------------------------
    # CLICK ELEMENT
    # ----------------------------------------------------------------
    def click(self, locator: tuple):
        """
        Why this step:
        - Clicks an element using explicit wait.

        What will happen:
        - Wait for form loader overlay to disappear (OrangeHRM).
        - Wait until element is clickable, highlight, click.
        - If click is intercepted by a loader, wait again and retry; then JS click.
        """
        logger.info(f"Clicking element: {locator}")
        self.wait_for_no_form_loader()
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.highlight(element)
        try:
            element.click()
        except ElementClickInterceptedException:
            logger.info("Click intercepted; waiting for loader and retrying")
            self.wait_for_no_form_loader()
            element = self.wait.until(EC.element_to_be_clickable(locator))
            self.highlight(element)
            try:
                element.click()
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", element)

    # ----------------------------------------------------------------
    # TYPE TEXT
    # ----------------------------------------------------------------
    def type(self, locator: tuple, text: str):
        """
        Why this step:
        - To type text into an input field.

        What will happen:
        - Find element
        - Highlight it
        - Clear old text
        - Type new text
        """
        logger.info(f"Typing text into element: {locator}")
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    # ----------------------------------------------------------------
    # GET TEXT
    # ----------------------------------------------------------------
    def get_text(self, locator: tuple):
        """
        Why:
        - To extract text from an element.

        What happens:
        - Wait for element → return text.
        """
        element = self.find(locator)
        return element.text.strip()

    # ----------------------------------------------------------------
    # SCROLL INTO VIEW
    # ----------------------------------------------------------------
    def scroll_to(self, locator: tuple):
        """
        Why:
        - Scroll page so element becomes visible.

        What happens:
        - Execute JS scroll.
        """
        element = self.find(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    # ----------------------------------------------------------------
    # SELECT FROM DROPDOWN (BY VISIBLE TEXT)
    # ----------------------------------------------------------------
    def select_by_text(self, locator: tuple, text: str):
        """
        Why:
        - Many pages have dropdowns.
        - Easy helper to choose any dropdown option.

        What happens:
        - Find dropdown
        - Select visible text
        """

        from selenium.webdriver.support.ui import Select

        element = self.find(locator)
        self.highlight(element)
        Select(element).select_by_visible_text(text)

    # ----------------------------------------------------------------
    # HOVER MOUSE
    # ----------------------------------------------------------------
    def hover(self, locator: tuple):
        """
        Why:
        - Some menus open on mouse hover.

        What happens:
        - Move mouse to the element.
        """
        element = self.find(locator)
        ActionChains(self.driver).move_to_element(element).perform()

    # ----------------------------------------------------------------
    # KEYBOARD ACTIONS
    # ----------------------------------------------------------------
    def press_key(self, locator: tuple, key=Keys.ENTER):
        """
        Why:
        - Useful for auto-suggest dropdowns, search fields etc.

        What happens:
        - Find element
        - Press a key like ENTER, TAB, ESCAPE
        """
        element = self.find(locator)
        element.send_keys(key)

    # ----------------------------------------------------------------
    # FILE UPLOAD
    # ----------------------------------------------------------------
    def upload_file(self, locator: tuple, file_path: str):
        """
        Why:
        - Many forms need file upload (image, resume, etc.)

        What happens:
        - Type file path into input[type='file']
        - OrangeHRM hides file inputs (opacity 0); visibility wait never succeeds, so use presence.
        - On Windows, ChromeDriver often fails when the path contains spaces; copy to TEMP first.
        """
        self.wait_for_no_form_loader()

        path = os.path.abspath(os.path.normpath(file_path))
        if not os.path.isfile(path):
            raise FileNotFoundError(
                f"Upload file missing: {path}. "
                "Commit TestData assets or run tests from a repo where pytest_sessionstart can create them."
            )

        upload_path = path
        tmp_copy = None
        if os.name == "nt" and " " in path:
            suffix = os.path.splitext(path)[1] or ".bin"
            fd, tmp_copy = tempfile.mkstemp(prefix="ohrm_upload_", suffix=suffix)
            os.close(fd)
            shutil.copy2(path, tmp_copy)
            upload_path = tmp_copy

        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            self.highlight(element)
            element.send_keys(upload_path)
        finally:
            if tmp_copy and os.path.isfile(tmp_copy):
                try:
                    os.remove(tmp_copy)
                except OSError:
                    pass

    # ----------------------------------------------------------------
    # SWITCH TO FRAME
    # ----------------------------------------------------------------
    def switch_to_frame(self, locator: tuple):
        """
        Why:
        - Some pages or forms are inside an iframe.

        What happens:
        - Switch driver to iframe.
        """
        frame = self.find(locator)
        self.driver.switch_to.frame(frame)

    # ----------------------------------------------------------------
    # SWITCH OUT OF FRAME
    # ----------------------------------------------------------------
    def switch_to_default(self):
        """
        Why:
        - After working inside iframe, return to the main page.
        """
        self.driver.switch_to.default_content()

    # ----------------------------------------------------------------
    # SWITCH TO NEW WINDOW
    # ----------------------------------------------------------------
    def switch_to_new_window(self):
        """
        Why:
        - Some links open in a new window/tab.

        What happens:
        - Switch driver to the latest window.
        """
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])

    # ----------------------------------------------------------------
    # EXECUTE JAVASCRIPT
    # ----------------------------------------------------------------
    def js(self, script: str, element=None):
        """
        Why:
        - Sometimes you need JS: scroll, click, set attribute.

        What happens:
        - Run JS script.
        """
        return self.driver.execute_script(script, element)