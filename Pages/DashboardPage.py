from selenium.webdriver.common.by import By
from Core.BasePage import BasePage
from Utils.Logger import logger


class DashboardPage(BasePage):
    """
    DashboardPage:
    This class represents the main page you see after a successful login.
    It contains:
      - top menu buttons
      - user dropdown
      - logout button
      - navigation links

    All tests after login will use this page.
    """

    # -------------------------------------------------------------
    # PAGEELEMENT LOCATORS (PageFactory style)
    # -------------------------------------------------------------

    # Dashboard main heading (used to confirm login success)
    DASHBOARD_HEADER = (By.XPATH, "//h6[text()='Dashboard']")

    # User dropdown (top right corner)
    USER_DROPDOWN = (By.CSS_SELECTOR, "span.oxd-userdropdown-tab")

    # Logout link inside dropdown
    LOGOUT_BUTTON = (By.XPATH, "//a[text()='Logout']")

    # Menu options (Admin, PIM, Leave, etc.)
    MENU_ADMIN = (By.XPATH, "//span[text()='Admin']")
    MENU_PIM = (By.XPATH, "//span[text()='PIM']")
    MENU_LEAVE = (By.XPATH, "//span[text()='Leave']")
    MENU_TIME = (By.XPATH, "//span[text()='Time']")
    MENU_RECRUITMENT = (By.XPATH, "//span[text()='Recruitment']")
    MENU_BUZZ = (By.XPATH, "//span[text()='Buzz']")
    MENU_MYINFO = (By.XPATH, "//span[text()='My Info']")

    # -------------------------------------------------------------
    # METHODS (actions for the Dashboard)
    # -------------------------------------------------------------

    def verify_login_success(self):
        """
        Why:
        - After login, we must confirm user actually reached Dashboard.

        What happens:
        - Wait until Dashboard heading becomes visible.
        - Highlight it.
        - Return True/False based on visibility.
        """
        logger.info("Verifying successful login by checking Dashboard header")
        header = self.find(self.DASHBOARD_HEADER)
        return header.is_displayed()

    def open_user_dropdown(self):
        """
        Why:
        - To access logout button, we must click on user menu.

        What happens:
        - Highlight menu.
        - Click user dropdown.
        """
        logger.info("Opening user dropdown menu")
        self.click(self.USER_DROPDOWN)

    def click_logout(self):
        """
        Why:
        - To log out from the application.

        What happens:
        - Click the 'Logout' link.
        """
        logger.info("Clicking logout button")
        self.click(self.LOGOUT_BUTTON)

    # -------------------------------------------------------------
    # NAVIGATION METHODS (used in other Test Cases)
    # -------------------------------------------------------------

    def go_to_admin(self):
        logger.info("Navigating to Admin module")
        self.click(self.MENU_ADMIN)

    def go_to_pim(self):
        logger.info("Navigating to PIM module")
        self.click(self.MENU_PIM)

    def go_to_leave(self):
        logger.info("Navigating to Leave module")
        self.click(self.MENU_LEAVE)

    def go_to_time(self):
        logger.info("Navigating to Time module")
        self.click(self.MENU_TIME)

    def go_to_recruitment(self):
        logger.info("Navigating to Recruitment module")
        self.click(self.MENU_RECRUITMENT)

    def go_to_buzz(self):
        logger.info("Navigating to Buzz module")
        self.click(self.MENU_BUZZ)

    def go_to_my_info(self):
        logger.info("Navigating to My Info module")
        self.click(self.MENU_MYINFO)