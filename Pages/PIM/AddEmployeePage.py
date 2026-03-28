from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from Core.BasePage import BasePage
from Utils.Logger import logger


class AddEmployeePage(BasePage):
    """
    AddEmployeePage:
    This class handles the 'Add Employee' screen inside the PIM module.

    PIM → Add Employee includes:
    - First name
    - Middle name
    - Last name
    - Employee ID
    - Upload photo
    - Create Login Details (optional)
    - Save button
    """

    # -------------------------------------------------------------
    # LOCATORS (PageFactory Style)
    # -------------------------------------------------------------

    # Name fields
    FIRST_NAME = (By.NAME, "firstName")
    MIDDLE_NAME = (By.NAME, "middleName")
    LAST_NAME = (By.NAME, "lastName")

    # Employee ID field
    EMP_ID = (By.XPATH, "//label[text()='Employee Id']/../following-sibling::div//input")

    # Photo upload
    PHOTO_UPLOAD = (By.CSS_SELECTOR, "input[type='file']")

    # Toggle for creating login details
    CREATE_LOGIN_TOGGLE = (By.XPATH, "//span[@class='oxd-switch-input oxd-switch-input--active --label-left']")

    # Login detail fields (visible only when toggle is ON)
    LOGIN_USERNAME = (By.XPATH, "//label[text()='Username']/../following-sibling::div//input")
    LOGIN_PASSWORD = (By.XPATH, "//input[@type='password'][1]")
    LOGIN_CONFIRM_PASSWORD = (By.XPATH, "//input[@type='password'][2]")

    # Date of birth (example date picker)
    DOB_FIELD = (By.XPATH, "//label[text()='Date of Birth']/../following-sibling::div//input")

    # Save button
    SAVE_BTN = (By.XPATH, "//button[@type='submit']")

    # After saving, employee profile heading appears
    PERSONAL_DETAILS_HEADER = (By.XPATH, "//h6[text()='Personal Details']")

    # -------------------------------------------------------------
    # PAGE ACTIONS
    # -------------------------------------------------------------

    def open_add_employee(self):
        """
        Why:
        - PIM opens on Employee List; firstName fields exist only on Add Employee.

        What happens:
        - Navigate to .../web/index.php/pim/addEmployee and wait for the form.
        """
        url = f"{self.config.get_app_base_url()}/pim/addEmployee"
        logger.info("Opening Add Employee screen: %s", url)
        self.driver.get(url)
        self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME))

    def enter_first_name(self, name):
        logger.info(f"Entering first name: {name}")
        self.type(self.FIRST_NAME, name)

    def enter_middle_name(self, name):
        logger.info(f"Entering middle name: {name}")
        self.type(self.MIDDLE_NAME, name)

    def enter_last_name(self, name):
        logger.info(f"Entering last name: {name}")
        self.type(self.LAST_NAME, name)

    def enter_employee_id(self, emp_id):
        logger.info(f"Entering employee ID: {emp_id}")
        self.type(self.EMP_ID, emp_id)

    def upload_photo(self, file_path):
        logger.info(f"Uploading photo from: {file_path}")
        self.upload_file(self.PHOTO_UPLOAD, file_path)

    def enable_login_details(self):
        """
        Why:
        - Some companies create login credentials for the new employee.

        What happens:
        - Click toggle → login fields appear.
        """
        logger.info("Enabling 'Create Login Details'")
        self.click(self.CREATE_LOGIN_TOGGLE)

    def enter_login_username(self, text):
        logger.info(f"Entering login username: {text}")
        self.type(self.LOGIN_USERNAME, text)

    def enter_login_password(self, text):
        logger.info("Entering login password")
        self.type(self.LOGIN_PASSWORD, text)

    def enter_confirm_password(self, text):
        logger.info("Entering confirm password")
        self.type(self.LOGIN_CONFIRM_PASSWORD, text)

    def enter_dob(self, dob_text):
        """
        DOB must be in yyyy-mm-dd format (OrangeHRM uses date picker).
        """
        logger.info(f"Entering date of birth: {dob_text}")
        self.type(self.DOB_FIELD, dob_text)

    def click_save(self):
        logger.info("Clicking Save button")
        self.click(self.SAVE_BTN)

    # -------------------------------------------------------------
    # HIGH-LEVEL ACTION (FULL ADD EMPLOYEE FLOW)
    # -------------------------------------------------------------
    def add_employee_basic(self, first, middle, last, emp_id, photo=None):
        """
        This is a full basic flow for Add Employee (without login details)
        """
        logger.info("Running high-level add_employee_basic flow")

        self.enter_first_name(first)
        self.enter_middle_name(middle)
        self.enter_last_name(last)
        self.enter_employee_id(emp_id)

        if photo:
            self.upload_photo(photo)

        self.click_save()

    def verify_employee_profile_loaded(self):
        """
        Why:
        - After clicking Save, employee profile page appears.

        What happens:
        - Check for Personal Details header.
        """
        logger.info("Verifying employee profile page loaded")
        header = self.find(self.PERSONAL_DETAILS_HEADER)
        return header.is_displayed()