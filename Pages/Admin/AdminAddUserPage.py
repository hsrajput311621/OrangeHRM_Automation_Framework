from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from Core.BasePage import BasePage
from Utils.Logger import logger


class AdminAddUserPage(BasePage):
    """
    AdminAddUserPage:
    This page controls the 'Add User' screen in the Admin module.

    Functions supported:
    - Select user role
    - Enter employee name (auto-suggest dropdown)
    - Select user status
    - Enter username
    - Enter password + confirm password
    - Save user
    """

    # -------------------------------------------------------------
    # LOCATORS (PageFactory Style)
    # -------------------------------------------------------------

    # Buttons
    ADD_BUTTON = (By.XPATH, "//button[normalize-space()='Add']")

    # Dropdowns (click to open)
    USER_ROLE_DROPDOWN = (By.XPATH, "//label[text()='User Role']/../following-sibling::div//div[@class='oxd-select-text-input']")
    STATUS_DROPDOWN = (By.XPATH, "//label[text()='Status']/../following-sibling::div//div[@class='oxd-select-text-input']")

    # Dropdown options (chosen dynamically)
    DROPDOWN_OPTION = lambda self, text: (By.XPATH, f"//span[text()='{text}']")

    # Employee name auto-suggest
    EMPLOYEE_NAME_INPUT = (By.XPATH, "//label[text()='Employee Name']/../following-sibling::div//input")
    EMPLOYEE_SUGGESTION = (By.XPATH, "//div[@role='option']")

    # Username & password fields (oxd layout: label + slot wrapper — avoid brittle ../following)
    USERNAME_INPUT = (By.XPATH,
        "//div[contains(@class,'oxd-input-group')][.//label[normalize-space()='Username']]//input"
    )

    # Save button
    SAVE_BUTTON = (By.XPATH, "//button[@type='submit']")

    # After saving success message appears
    SUCCESS_TOAST = (By.XPATH, "//p[contains(text(),'Successfully Saved')]")

    # -------------------------------------------------------------
    # PAGE ACTIONS
    # -------------------------------------------------------------

    def click_add(self):
        logger.info("Clicking Add User button")
        self.click(self.ADD_BUTTON)

    def select_user_role(self, role_text):
        """
        Why:
        - User Role dropdown has values like Admin, ESS, etc.

        What happens:
        - Click dropdown → choose visible text option.
        """
        logger.info(f"Selecting User Role: {role_text}")
        self.click(self.USER_ROLE_DROPDOWN)
        self.click(self.DROPDOWN_OPTION(role_text))

    def enter_employee_name(self, name):
        """
        Why:
        - Employee Name uses auto-suggest.
        - You type name → suggestions appear → you press ENTER.

        What happens:
        - Type name into input box.
        - Press ENTER to select first suggestion.
        """
        logger.info(f"Entering employee name (auto-suggest): {name}")
        self.type(self.EMPLOYEE_NAME_INPUT, name)
        try:
            self.wait.until(
                EC.visibility_of_element_located((By.XPATH, "//div[@role='listbox']"))
            )
            first = (By.XPATH, "//div[@role='listbox']//div[@role='option'][1]")
            self.click(first)
        except TimeoutException:
            self.press_key(self.EMPLOYEE_NAME_INPUT, Keys.ARROW_DOWN)
            self.press_key(self.EMPLOYEE_NAME_INPUT, Keys.ENTER)

    def select_status(self, status_text):
        logger.info(f"Selecting Status: {status_text}")
        self.click(self.STATUS_DROPDOWN)
        self.click(self.DROPDOWN_OPTION(status_text))

    def enter_username(self, text):
        logger.info(f"Entering username: {text}")
        self.type(self.USERNAME_INPUT, text)

    def _visible_password_inputs(self):
        """Add User DOM varies by build; use visible password fields in order (password, confirm)."""
        xpaths = [
            "//div[contains(@class,'orangehrm-card-body')]//input[@type='password']",
            "//div[contains(@class,'orangehrm-card')]//input[@type='password']",
            "//div[contains(@class,'oxd-form')]//input[@type='password']",
            "//form//input[@type='password' and not(@readonly)]",
        ]
        for xp in xpaths:
            els = self.driver.find_elements(By.XPATH, xp)
            visible = [e for e in els if e.is_displayed()]
            if len(visible) >= 2:
                return visible
        return []

    def enter_password(self, text):
        logger.info("Entering password")

        def two_fields(_driver):
            fields = self._visible_password_inputs()
            return fields if len(fields) >= 2 else False

        fields = self.wait.until(two_fields)
        el = fields[0]
        self.highlight(el)
        el.clear()
        el.send_keys(text)

    def enter_confirm_password(self, text):
        logger.info("Entering confirm password")
        fields = self._visible_password_inputs()
        if len(fields) < 2:
            raise TimeoutException("Expected two visible password fields on Add User form")
        el = fields[1]
        self.highlight(el)
        el.clear()
        el.send_keys(text)

    def click_save(self):
        logger.info("Clicking Save button")
        self.click(self.SAVE_BUTTON)

    # -------------------------------------------------------------
    # HIGH-LEVEL METHOD (Complete User Creation)
    # -------------------------------------------------------------
    def add_user(self, role, employee_name, status, username, password):
        """
        High-level function to add user in a single call.
        """
        logger.info("Running high-level 'Add User' flow")

        self.click_add()
        self.select_user_role(role)
        self.enter_employee_name(employee_name)
        self.select_status(status)
        self.enter_username(username)
        self.enter_password(password)
        self.enter_confirm_password(password)
        self.click_save()

    def verify_user_saved(self):
        """
        Check if success message appears after saving user.
        """
        logger.info("Verifying success message after adding user")
        header = self.find(self.SUCCESS_TOAST)
        return header.is_displayed()