from selenium.webdriver.common.by import By
from Core.BasePage import BasePage
from Utils.Logger import logger


class MyInfoPersonalDetailsPage(BasePage):
    """
    This class handles the 'My Info → Personal Details' page.
    It supports:
    ✅ Updating full name
    ✅ Updating nickname
    ✅ Selecting nationality (dropdown)
    ✅ Selecting marital status (dropdown)
    ✅ Selecting gender (radio buttons)
    ✅ Updating date of birth
    ✅ Saving form
    ✅ Validating success message
    """

    # -------------------------------------------------------------
    # LOCATORS (PageFactory style)
    # -------------------------------------------------------------

    # Name fields
    FIRST_NAME = (By.NAME, "firstName")
    MIDDLE_NAME = (By.NAME, "middleName")
    LAST_NAME = (By.NAME, "lastName")

    # Personal Details are read-only until Edit is clicked.
    # Header may use icon-only Edit; target the card that contains the Personal Details heading
    PERSONAL_DETAILS_EDIT = (
        By.XPATH,
        "//div[contains(@class,'orangehrm-card-header')]"
        "[.//h6[contains(normalize-space(),'Personal Details')]]"
        "//button[contains(@class,'oxd-button') or contains(@class,'oxd-icon-button')][1]",
    )

    # Nickname (label text can vary slightly by build)
    NICKNAME = (
        By.XPATH,
        "//label[contains(normalize-space(),'Nick')]/../following-sibling::div//input",
    )

    # Employee ID
    EMPLOYEE_ID = (By.XPATH, "//label[text()='Employee Id']/../following-sibling::div//input")

    # Nationality dropdown
    NATIONALITY_DROPDOWN = (By.XPATH,
        "//label[text()='Nationality']/../following-sibling::div//div[contains(@class,'oxd-select-text--after')]"
    )
    OPTION = lambda self, text: (By.XPATH, f"//span[normalize-space()='{text}']")

    # Marital Status dropdown
    MARITAL_STATUS_DROPDOWN = (By.XPATH,
        "//label[text()='Marital Status']/../following-sibling::div//div[contains(@class,'oxd-select-text--after')]"
    )

    # Gender radio buttons
    GENDER_MALE = (By.XPATH, "//label[text()='Gender']/../following-sibling::div//label[text()='Male']/../input")
    GENDER_FEMALE = (By.XPATH, "//label[text()='Gender']/../following-sibling::div//label[text()='Female']/../input")

    # Date of birth
    DOB = (By.XPATH, "//label[text()='Date of Birth']/../following-sibling::div//input")

    # Save button
    SAVE_BUTTON = (By.XPATH, "//button[@type='submit']")

    # Success message
    SUCCESS_TOAST = (By.XPATH, "//p[contains(text(),'Successfully Updated')]")

    # -------------------------------------------------------------
    # PAGE ACTIONS
    # -------------------------------------------------------------

    def click_edit_personal_details(self):
        logger.info("Clicking Edit on Personal Details section")
        self.click(self.PERSONAL_DETAILS_EDIT)

    def enter_first_name(self, text):
        logger.info(f"Entering first name: {text}")
        self.type(self.FIRST_NAME, text)

    def enter_middle_name(self, text):
        logger.info(f"Entering middle name: {text}")
        self.type(self.MIDDLE_NAME, text)

    def enter_last_name(self, text):
        logger.info(f"Entering last name: {text}")
        self.type(self.LAST_NAME, text)

    def enter_nickname(self, text):
        logger.info(f"Entering nickname: {text}")
        self.type(self.NICKNAME, text)

    def enter_employee_id(self, emp_id):
        logger.info(f"Entering employee ID: {emp_id}")
        self.type(self.EMPLOYEE_ID, emp_id)

    def select_nationality(self, text):
        logger.info(f"Selecting nationality: {text}")
        self.click(self.NATIONALITY_DROPDOWN)
        self.click(self.OPTION(text))

    def select_marital_status(self, text):
        logger.info(f"Selecting marital status: {text}")
        self.click(self.MARITAL_STATUS_DROPDOWN)
        self.click(self.OPTION(text))

    def select_gender(self, gender):
        logger.info(f"Selecting gender: {gender}")

        if gender.lower() == "male":
            self.click(self.GENDER_MALE)
        elif gender.lower() == "female":
            self.click(self.GENDER_FEMALE)
        else:
            raise ValueError("Gender must be 'Male' or 'Female'")

    def enter_dob(self, date_text):
        logger.info(f"Entering date of birth: {date_text}")
        self.type(self.DOB, date_text)

    def click_save(self):
        logger.info("Clicking Save button")
        self.click(self.SAVE_BUTTON)

    # -------------------------------------------------------------
    # HIGH-LEVEL ACTION
    # -------------------------------------------------------------

    def update_personal_details(
        self,
        first,
        middle,
        last,
        nickname,
        emp_id,
        nationality,
        marital_status,
        gender,
        dob
    ):
        logger.info("Running full 'Update Personal Details' workflow")

        self.click_edit_personal_details()
        self.enter_first_name(first)
        self.enter_middle_name(middle)
        self.enter_last_name(last)
        self.enter_nickname(nickname)
        self.enter_employee_id(emp_id)
        self.select_nationality(nationality)
        self.select_marital_status(marital_status)
        self.select_gender(gender)
        self.enter_dob(dob)
        self.click_save()

    def verify_update_success(self):
        logger.info("Verifying Personal Details updated successfully")
        toast = self.find(self.SUCCESS_TOAST)
        return toast.is_displayed()