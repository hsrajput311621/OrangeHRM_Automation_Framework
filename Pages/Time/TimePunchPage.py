from selenium.webdriver.common.by import By
from Core.BasePage import BasePage
from Utils.Logger import logger


class TimePunchPage(BasePage):
    """
    TimePunchPage:
    This class handles the 'Punch In' and 'Punch Out' functionality
    inside the Time module.

    Supported actions:
    - Punch In
    - Punch Out
    - Enter comment
    - Validate punch success
    - Read punch in/out time
    """

    # -------------------------------------------------------------
    # LOCATORS (PageFactory Style)
    # -------------------------------------------------------------

    # Punch In button
    PUNCH_IN_BUTTON = (By.XPATH, "//button[contains(., 'Punch In')]")

    # Punch Out button
    PUNCH_OUT_BUTTON = (By.XPATH, "//button[contains(., 'Punch Out')]")

    # Comment field
    COMMENT_FIELD = (By.XPATH, "//textarea")

    # Displayed time after punching
    PUNCH_TIME_TEXT = (By.XPATH, "//p[contains(@class,'oxd-text-bold')]")

    # Success toast
    SUCCESS_TOAST = (By.XPATH, "//p[contains(text(),'Success')]")

    # -------------------------------------------------------------
    # PAGE ACTIONS
    # -------------------------------------------------------------

    def enter_comment(self, text):
        """
        Why:
        - Comment is optional but good practice.

        What happens:
        - Type into the textarea.
        """
        logger.info(f"Entering punch comment: {text}")
        self.type(self.COMMENT_FIELD, text)

    def click_punch_in(self):
        """
        Click the Punch In button.
        """
        logger.info("Clicking Punch In button")
        self.click(self.PUNCH_IN_BUTTON)

    def click_punch_out(self):
        """
        Click the Punch Out button.
        """
        logger.info("Clicking Punch Out button")
        self.click(self.PUNCH_OUT_BUTTON)

    def get_punch_time(self):
        """
        Why:
        - After punching, OrangeHRM shows the time.

        Example:
        '13:10 PM'

        What happens:
        - Extract and return the time text.
        """
        logger.info("Reading punch time text")
        return self.get_text(self.PUNCH_TIME_TEXT)

    def verify_punch_success(self):
        """
        Check if success toast appears.
        """
        logger.info("Verifying punch success toast")
        toast = self.find(self.SUCCESS_TOAST)
        return toast.is_displayed()

    # -------------------------------------------------------------
    # HIGH-LEVEL STEPS
    # -------------------------------------------------------------

    def punch_in(self, comment):
        """
        Full punch-in flow.
        """
        logger.info("Performing Punch In workflow")

        self.enter_comment(comment)
        self.click_punch_in()

    def punch_out(self, comment):
        """
        Full punch-out flow.
        """
        logger.info("Performing Punch Out workflow")

        self.enter_comment(comment)
        self.click_punch_out()