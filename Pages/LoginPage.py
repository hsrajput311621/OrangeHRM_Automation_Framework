from selenium.webdriver.common.by import By
from Core.BasePage import BasePage
from Utils.Logger import logger


class LoginPage(BasePage):
    """
    LoginPage:
    This class contains all elements and actions related to the Login Page.
    It inherits BasePage, so it can use click(), type(), find(), highlight(), etc.
    """

    # -------------------------------------------------------------
    # ALL LOCATORS (PageFactory style)
    # -------------------------------------------------------------

    # Username input box
    USERNAME = (By.NAME, "username")

    # Password input box
    PASSWORD = (By.NAME, "password")

    # Login button
    LOGIN_BTN = (By.CSS_SELECTOR, "button[type='submit']")

    # Error message (appears on invalid login)
    ERROR_MSG = (By.CSS_SELECTOR, "p.oxd-alert-content-text")

    # -------------------------------------------------------------
    # PAGE ACTIONS
    # -------------------------------------------------------------

    def enter_username(self, username: str):
        """
        Why this step:
        - To type the username into the username input box.

        What will happen:
        - Highlight the field.
        - Clear old value.
        - Type new value.
        """
        logger.info(f"Entering username: {username}")
        self.type(self.USERNAME, username)

    def enter_password(self, password: str):
        """
        Why:
        - To type password into the password field.

        What happens:
        - Highlight field.
        - Clear old value.
        - Type password.
        """
        logger.info(f"Entering password: {password}")
        self.type(self.PASSWORD, password)

    def click_login(self):
        """
        Why:
        - To click on the login button.

        What happens:
        - Wait until button clickable.
        - Highlight.
        - Click.
        """
        logger.info("Clicking login button")
        self.click(self.LOGIN_BTN)

    def get_error_message(self):
        """
        Why:
        - When login fails, we need to fetch the error message text.

        What happens:
        - Find error message.
        - Highlight.
        - Return extracted text.
        """
        logger.info("Fetching login error message")
        return self.get_text(self.ERROR_MSG)

    # -------------------------------------------------------------
    # HIGH-LEVEL METHODS (Complete steps)
    # -------------------------------------------------------------
    def login(self, username: str, password: str):
        """
        Why:
        - To perform full login in ONE step.
        - Helpful for tests where we only want to call login().

        What happens:
        - Enter username.
        - Enter password.
        - Click login button.
        """
        logger.info("Performing full login sequence")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()