from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

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
    # PAGE ELEMENT LOCATORS (PageFactory style)
    # -------------------------------------------------------------

    # Dashboard main heading (used to confirm login success)
    DASHBOARD_HEADER = (By.XPATH, "//h6[text()='Dashboard']")

    # User dropdown (top right corner)
    USER_DROPDOWN = (By.CSS_SELECTOR, "span.oxd-userdropdown-tab")

    # Logout link inside dropdown
    LOGOUT_BUTTON = (By.XPATH, "//a[text()='Logout']")

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
    # SIDEBAR NAVIGATION (OrangeHRM 5.x)
    # -------------------------------------------------------------
    def _click_left_menu(self, label: str):
        """
        Why not //span[text()='PIM'] alone:
        - OrangeHRM wraps each module in <a class="oxd-main-menu-item">.
        - Spans can have whitespace; normalize-space() avoids flaky exact matches.
        - In headless/small windows the link can be off-screen; we scroll it into view first.

        What happens:
        1) Find the sidebar <a> whose descendant span text matches `label`.
        2) Scroll it to the center of the viewport.
        3) Wait until clickable, then click.
        """
        xpath = (
            "//a[contains(@class,'oxd-main-menu-item')]"
            f"[.//span[normalize-space()='{label}']]"
        )
        locator = (By.XPATH, xpath)
        logger.info(f"Opening left menu: {label}")
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center', inline:'nearest'});",
            element,
        )
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.highlight(element)
        element.click()

    def go_to_admin(self):
        self._click_left_menu("Admin")

    def go_to_pim(self):
        self._click_left_menu("PIM")

    def go_to_leave(self):
        self._click_left_menu("Leave")

    def go_to_time(self):
        self._click_left_menu("Time")

    def go_to_recruitment(self):
        self._click_left_menu("Recruitment")

    def go_to_buzz(self):
        self._click_left_menu("Buzz")

    def go_to_my_info(self):
        self._click_left_menu("My Info")
