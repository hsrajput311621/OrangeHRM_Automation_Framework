from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

from Core.BasePage import BasePage
from Utils.Logger import logger


class SearchEmployeePage(BasePage):
    """
    SearchEmployeePage:
    This page is used to search for employees in the PIM module.

    It supports:
    - Search by employee name
    - Search by employee ID
    - Select job title or status from dropdown
    - Validate search result in table
    """

    # -------------------------------------------------------------
    # LOCATORS (PageFactory Style)
    # -------------------------------------------------------------

    # Search fields
    EMP_NAME_INPUT = (By.XPATH, "//label[text()='Employee Name']/../following-sibling::div//input")
    EMP_ID_INPUT = (By.XPATH, "//label[text()='Employee Id']/../following-sibling::div//input")

    # Dropdowns (example: Employment Status)
    EMP_STATUS_DROPDOWN = (By.XPATH, "//label[text()='Employment Status']/../following-sibling::div//div[@class='oxd-select-text--after']")

    # Dropdown options (will select dynamically by visible text)
    DROPDOWN_OPTION = lambda self, text: (By.XPATH, f"//div[@role='option']//span[text()='{text}']")

    # Buttons
    SEARCH_BTN = (By.XPATH, "//button[@type='submit']")
    RESET_BTN = (By.XPATH, "//button[text()=' Reset ']")

    # Table rows
    TABLE_ROWS = (By.XPATH, "//div[contains(@class,'oxd-table-body')]//div[@role='row']")

    # Employee Name inside row
    TABLE_EMP_NAME = (By.XPATH, ".//div[@role='cell'][3]//div")

    # Employee ID inside row
    TABLE_EMP_ID = (By.XPATH, ".//div[@role='cell'][2]")

    # -------------------------------------------------------------
    # PAGE ACTIONS
    # -------------------------------------------------------------

    def enter_employee_name(self, name):
        logger.info(f"Entering employee name: {name}")
        self.type(self.EMP_NAME_INPUT, name)
        try:
            self.wait.until(
                EC.visibility_of_element_located((By.XPATH, "//div[@role='listbox']"))
            )
            first = (By.XPATH, "//div[@role='listbox']//div[@role='option'][1]")
            self.click(first)
        except TimeoutException:
            self.press_key(self.EMP_NAME_INPUT, Keys.ARROW_DOWN)
            self.press_key(self.EMP_NAME_INPUT, Keys.ENTER)

    def enter_employee_id(self, emp_id):
        logger.info(f"Entering employee ID: {emp_id}")
        self.type(self.EMP_ID_INPUT, emp_id)

    def select_employment_status(self, status_text):
        """
        Why:
        - Some companies use this filter to search only active employees.

        What happens:
        - Click dropdown.
        - Select given visible option.
        """
        logger.info(f"Selecting Employment Status: {status_text}")
        self.click(self.EMP_STATUS_DROPDOWN)
        self.click(self.DROPDOWN_OPTION(status_text))

    def click_search(self):
        logger.info("Clicking Search button")
        self.click(self.SEARCH_BTN)

    def click_reset(self):
        logger.info("Resetting search filters")
        self.click(self.RESET_BTN)

    # -------------------------------------------------------------
    # METHODS TO VALIDATE TABLE RESULTS
    # -------------------------------------------------------------

    def get_all_rows(self):
        """
        Why:
        - To get the list of all search results.

        What happens:
        - Return all visible rows.
        """
        return self.driver.find_elements(*self.TABLE_ROWS)

    def validate_employee_present(self, expected_name):
        """
        Why:
        - To confirm that the searched employee appears in results.

        What happens:
        - Re-query cells after Search (table refresh makes row WebElements stale).
        """
        logger.info(f"Validating employee name in search results: {expected_name}")
        exp = expected_name.strip().lower()
        if not exp:
            return False

        trans = "translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')"
        if "'" not in exp:
            xpath = (
                "//div[contains(@class,'oxd-table-body')]//div[@role='cell']"
                f"[contains({trans}, '{exp}')]"
            )
            try:
                self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                return True
            except TimeoutException:
                pass

        cells = self.driver.find_elements(
            By.XPATH, "//div[contains(@class,'oxd-table-body')]//div[@role='cell']"
        )
        for cell in cells:
            try:
                if exp in cell.text.strip().lower():
                    return True
            except StaleElementReferenceException:
                return self.validate_employee_present(expected_name)
        return False

    def validate_employee_id_present(self, expected_id):
        """
        Why:
        - To confirm employee ID appears in table.

        What happens:
        - Match exact ID text in any cell without holding stale row references.
        """
        logger.info(f"Validating employee ID in search results: {expected_id}")
        eid = str(expected_id).strip()
        xpath = (
            "//div[contains(@class,'oxd-table-body')]//div[@role='cell']"
            f"[normalize-space()='{eid}']"
        )
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            return True
        except TimeoutException:
            return False

    # -------------------------------------------------------------
    # HIGH-LEVEL METHOD: Search by name or ID
    # -------------------------------------------------------------
    def search_employee(self, name=None, emp_id=None):
        """
        Why:
        - To perform search in one single step for test simplicity.

        What happens:
        - Fill whichever field is provided.
        - Click Search button.
        """
        logger.info("Running high-level employee search")

        if name:
            self.enter_employee_name(name)

        if emp_id:
            self.enter_employee_id(emp_id)

        self.click_search()
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'oxd-table-body')]")
            )
        )