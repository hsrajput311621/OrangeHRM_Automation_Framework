from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from Core.BasePage import BasePage
from Utils.Logger import logger


class LeaveApplyPage(BasePage):
    """
    LeaveApplyPage:
    This class handles the 'Apply Leave' form inside the Leave module.

    Functions supported:
    - Select leave type (dropdown)
    - Pick From Date & To Date (date picker)
    - Enter comments
    - Submit leave request
    - Validate success message
    """

    # -------------------------------------------------------------
    # LOCATORS (PageFactory Style)
    # -------------------------------------------------------------

    # Leave Type dropdown
    LEAVE_TYPE_DROPDOWN = (By.XPATH,
        "//label[text()='Leave Type']/../following-sibling::div//div[contains(@class,'oxd-select-text-input')]"
    )

    # Options inside dropdown (selected dynamically)
    OPTION = lambda self, text: (By.XPATH, f"//span[normalize-space()='{text}']")

    # From Date field
    FROM_DATE = (By.XPATH,
        "//label[text()='From Date']/../following-sibling::div//input"
    )

    # To Date field
    TO_DATE = (By.XPATH,
        "//label[text()='To Date']/../following-sibling::div//input"
    )

    # Comment box (UI may say 'Comment' or 'Comments')
    COMMENT_BOX = (By.XPATH,
        "//label[contains(normalize-space(),'Comment')]/../following-sibling::div//textarea"
    )

    # Apply button (Vue may omit <form>; prefer leave card, then any Apply submit)
    APPLY_BTN = (
        By.XPATH,
        "("
        "//form[.//label[normalize-space()='Leave Type']]//button[@type='submit'] | "
        "//div[contains(@class,'orangehrm-card-body')][.//label[normalize-space()='Leave Type']]"
        "//button[@type='submit'] | "
        "//button[@type='submit' and contains(normalize-space(.),'Apply')]"
        ")[1]",
    )

    # Success confirmation toast (markup varies by OrangeHRM build)
    SUCCESS_TOAST = (
        By.XPATH,
        "//div[contains(@class,'oxd-toast--success')]"
        "|//div[contains(@class,'oxd-toast') and contains(@class,'success')]"
        "|//div[contains(@class,'oxd-toast-container')]//*["
        "contains(.,'Successfully') or contains(.,'Submitted') or contains(.,'success')]",
    )

    # -------------------------------------------------------------
    # PAGE ACTIONS
    # -------------------------------------------------------------

    def open_apply_leave(self):
        """
        Why:
        - Leave module default is not always the Apply screen (e.g. Leave List).

        What happens:
        - Open .../web/index.php/leave/applyLeave and wait for Leave Type dropdown.
        """
        url = f"{self.config.get_app_base_url()}/leave/applyLeave"
        logger.info("Opening Apply Leave screen: %s", url)
        self.driver.get(url)
        self.wait_for_no_form_loader()
        self.wait.until(EC.visibility_of_element_located(self.LEAVE_TYPE_DROPDOWN))

    def select_leave_type(self, leave_type):
        """
        Why:
        - User must select leave type from a dropdown (Casual, Sick, etc.)

        What happens:
        - Click dropdown
        - Click option based on visible text
        """
        logger.info(f"Selecting Leave Type: {leave_type}")
        self.click(self.LEAVE_TYPE_DROPDOWN)
        self.click(self.OPTION(leave_type))

    def enter_from_date(self, date_text):
        """
        Why:
        - From Date is a date picker.
        - We type date directly in yyyy-mm-dd format.

        What happens:
        - Click field
        - Type date
        """
        logger.info(f"Entering From Date: {date_text}")
        self.type(self.FROM_DATE, date_text)
        self.press_key(self.FROM_DATE, Keys.TAB)

    def enter_to_date(self, date_text):
        logger.info(f"Entering To Date: {date_text}")
        self.type(self.TO_DATE, date_text)
        self.press_key(self.TO_DATE, Keys.TAB)

    def enter_comment(self, text):
        logger.info(f"Entering Comment: {text}")
        self.type(self.COMMENT_BOX, text)

    def click_apply(self):
        logger.info("Clicking Apply button")
        self.click(self.APPLY_BTN)

    # -------------------------------------------------------------
    # HIGH-LEVEL COMPLETE FLOW
    # -------------------------------------------------------------
    def apply_leave(self, leave_type, from_date, to_date, comment):
        """
        Perform the full apply leave action in one call.
        """
        logger.info("Performing full Leave Apply action")

        self.open_apply_leave()
        self.select_leave_type(leave_type)
        self.enter_from_date(from_date)
        self.enter_to_date(to_date)
        self.enter_comment(comment)
        self.click_apply()

    def verify_leave_submitted(self):
        """
        Check success toast message.
        """
        logger.info("Verifying leave has been submitted successfully")
        toast = self.wait.until(EC.presence_of_element_located(self.SUCCESS_TOAST))
        return toast.is_displayed()