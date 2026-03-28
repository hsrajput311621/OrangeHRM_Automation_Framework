from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from Core.BasePage import BasePage
from Utils.Logger import logger


class RecruitmentCandidatesListPage(BasePage):
    """
    This page handles:
    ✅ Searching candidate
    ✅ Selecting candidate checkbox
    ✅ Deleting the candidate
    ✅ Confirming deletion
    """

    # Search field
    SEARCH_NAME = (By.XPATH, "//label[text()='Candidate Name']/../following-sibling::div//input")

    # Search button
    SEARCH_BUTTON = (By.XPATH, "//button[@type='submit']")

    # Table rows
    TABLE_ROWS = (By.XPATH, "//div[@class='oxd-table-body']/div[@role='row']")

    # Checkbox inside first column
    ROW_CHECKBOX = (By.XPATH, ".//div[@role='cell'][1]//input")

    # Delete button (appears after checkbox selected)
    DELETE_BUTTON = (By.XPATH, "//button[contains(@class,'oxd-button--label-danger')]")

    # Confirm delete popup
    CONFIRM_DELETE_BUTTON = (By.XPATH, "//button[normalize-space()='Yes, Delete']")

    # Success toast
    SUCCESS_TOAST = (By.XPATH, "//p[contains(text(),'Successfully Deleted')]")

    # ---------------------------------------------------------
    # Methods
    # ---------------------------------------------------------

    def open_view_candidates(self):
        """
        Why:
        - Recruitment default view may not be the Candidates list (search + grid).

        What happens:
        - Open the standard Candidates list route used by the app.
        """
        url = f"{self.config.get_app_base_url()}/recruitment/viewCandidates"
        logger.info("Opening Candidates list: %s", url)
        self.driver.get(url)
        self.wait.until(EC.visibility_of_element_located(self.SEARCH_NAME))

    def search_candidate(self, name):
        logger.info(f"Searching candidate: {name}")
        self.type(self.SEARCH_NAME, name)
        self.click(self.SEARCH_BUTTON)

    def select_candidate_checkbox(self):
        logger.info("Selecting first candidate checkbox")
        rows = self.driver.find_elements(*self.TABLE_ROWS)

        if not rows:
            return False  # No candidates found

        first_row = rows[0]
        checkbox = first_row.find_element(*self.ROW_CHECKBOX)
        self.highlight(checkbox)
        checkbox.click()
        return True

    def delete_candidate(self):
        logger.info("Clicking Delete button")
        self.click(self.DELETE_BUTTON)

        logger.info("Confirming deletion")
        self.click(self.CONFIRM_DELETE_BUTTON)

    def verify_success(self):
        logger.info("Checking deletion success toast")
        toast = self.find(self.SUCCESS_TOAST)
        return toast.is_displayed()