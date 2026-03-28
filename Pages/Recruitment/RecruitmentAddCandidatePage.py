from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from Core.BasePage import BasePage
from Utils.Logger import logger


class RecruitmentAddCandidatePage(BasePage):
    """
    RecruitmentAddCandidatePage:
    This page handles the 'Add Candidate' form inside the Recruitment module.

    Supports:
    - Enter first/middle/last name
    - Enter email and contact number
    - Select job vacancy (dropdown)
    - Upload resume
    - Enter keywords
    - Enter notes
    - Set date of application
    - Save candidate
    - Validate success toast
    """

    # -------------------------------------------------------------
    # LOCATORS (PageFactory Style)
    # -------------------------------------------------------------

    # Name fields
    FIRST_NAME = (By.NAME, "firstName")
    MIDDLE_NAME = (By.NAME, "middleName")
    LAST_NAME = (By.NAME, "lastName")

    # Email and contact number
    EMAIL = (By.XPATH, "//label[text()='Email']/../following-sibling::div//input")
    CONTACT_NUMBER = (By.XPATH, "//label[text()='Contact Number']/../following-sibling::div//input")

    # Vacancy dropdown
    VACANCY_DROPDOWN = (By.XPATH,
        "//label[text()='Vacancy']/../following-sibling::div//div[contains(@class,'oxd-select-text-input')]"
    )
    OPTION = lambda self, text: (By.XPATH, f"//span[normalize-space()='{text}']")

    # Resume upload
    RESUME_UPLOAD = (
        By.XPATH,
        "//div[contains(@class,'oxd-input-group')]"
        "[.//label[contains(translate(normalize-space(.), 'RESUME', 'resume'), 'resume')]]"
        "//input[@type='file']",
    )

    # Keywords
    KEYWORDS = (By.XPATH, "//label[text()='Keywords']/../following-sibling::div//input")

    # Notes
    NOTES = (By.XPATH, "//label[text()='Notes']/../following-sibling::div//textarea")

    # Date of Application
    DATE_OF_APPLICATION = (By.XPATH,
        "//label[text()='Date of Application']/../following-sibling::div//input"
    )

    # Save button
    SAVE_BUTTON = (By.XPATH, "//button[@type='submit']")

    # Success toast
    SUCCESS_TOAST = (By.XPATH, "//p[contains(text(),'Successfully Saved')]")

    # -------------------------------------------------------------
    # PAGE ACTIONS
    # -------------------------------------------------------------

    def open_add_candidate(self):
        """
        Why:
        - Clicking only 'Recruitment' opens the module default (often dashboard), not the form.
        - Direct route is stable in CI/Jenkins and matches OrangeHRM routing.

        What happens:
        - Browser goes to .../web/index.php/recruitment/addCandidate and waits for the form.
        """
        url = f"{self.config.get_app_base_url()}/recruitment/addCandidate"
        logger.info("Opening Add Candidate screen: %s", url)
        self.driver.get(url)
        self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME))

    def enter_first_name(self, text):
        logger.info(f"Entering first name: {text}")
        self.type(self.FIRST_NAME, text)

    def enter_middle_name(self, text):
        logger.info(f"Entering middle name: {text}")
        self.type(self.MIDDLE_NAME, text)

    def enter_last_name(self, text):
        logger.info(f"Entering last name: {text}")
        self.type(self.LAST_NAME, text)

    def enter_email(self, text):
        logger.info(f"Entering email: {text}")
        self.type(self.EMAIL, text)

    def enter_contact_number(self, text):
        logger.info(f"Entering contact number: {text}")
        self.type(self.CONTACT_NUMBER, text)

    def select_vacancy(self, vacancy_text):
        logger.info(f"Selecting vacancy: {vacancy_text}")
        self.click(self.VACANCY_DROPDOWN)
        self.click(self.OPTION(vacancy_text))

    def upload_resume(self, file_path):
        logger.info(f"Uploading resume from: {file_path}")
        self.upload_file(self.RESUME_UPLOAD, file_path)

    def enter_keywords(self, text):
        logger.info(f"Entering keywords: {text}")
        self.type(self.KEYWORDS, text)

    def enter_notes(self, text):
        logger.info("Entering notes")
        self.type(self.NOTES, text)

    def enter_date_of_application(self, date_text):
        logger.info(f"Entering date of application: {date_text}")
        self.type(self.DATE_OF_APPLICATION, date_text)

    def click_save(self):
        logger.info("Clicking Save button")
        self.click(self.SAVE_BUTTON)

    # -------------------------------------------------------------
    # HIGH-LEVEL COMPLETE FLOW
    # -------------------------------------------------------------
    def add_candidate(
        self, first, middle, last, email, phone,
        vacancy, resume, keywords, notes, date
    ):
        logger.info("Performing full Add Candidate workflow")

        self.enter_first_name(first)
        self.enter_middle_name(middle)
        self.enter_last_name(last)
        self.enter_email(email)
        self.enter_contact_number(phone)
        self.select_vacancy(vacancy)

        if resume:
            self.upload_resume(resume)

        self.enter_keywords(keywords)
        self.enter_notes(notes)
        self.enter_date_of_application(date)

        self.click_save()

    def verify_candidate_saved(self):
        logger.info("Checking candidate saved success toast")
        toast = self.find(self.SUCCESS_TOAST)
        return toast.is_displayed()