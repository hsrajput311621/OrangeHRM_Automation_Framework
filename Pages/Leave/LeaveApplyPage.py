from selenium.webdriver.common.by import By
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

    # Comment box
    COMMENT_BOX = (By.XPATH,
        "//label[text()='Comments']/../following-sibling::div//textarea"
    )

    # Apply button
    APPLY_BTN = (By.XPATH, "//button[@type='submit']")

    # Success confirmation toast
    SUCCESS_TOAST = (By.XPATH, "//p[contains(text(),'Successfully Submitted')]")

    # -------------------------------------------------------------
    # PAGE ACTIONS
    # -------------------------------------------------------------

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

    def enter_to_date(self, date_text):
        logger.info(f"Entering To Date: {date_text}")
        self.type(self.TO_DATE, date_text)

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
        toast = self.find(self.SUCCESS_TOAST)
        return toast.is_displayed()