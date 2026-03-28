import pytest

from Utils.DataReader import DataReader
from Pages.LoginPage import LoginPage
from Pages.DashboardPage import DashboardPage
from Pages.Leave.LeaveApplyPage import LeaveApplyPage


# ---------------------------------------------------------
# LOAD TEST DATA (JSON + CSV + Excel)
# ---------------------------------------------------------

testdata_json = DataReader("TestData/apply_leave.json").get_data()
testdata_csv = DataReader("TestData/apply_leave.csv").get_data()
testdata_excel = DataReader("TestData/apply_leave.xlsx").get_data()

# Combine everything → full data-driven testing
all_test_data = testdata_json + testdata_csv + testdata_excel


@pytest.mark.parametrize("row", all_test_data)
def test_apply_leave(row, driver, config):
    """
    Why this test:
    - To verify that an employee can successfully apply for leave.
    - This test covers:
        ✅ Dropdown (Leave Type)
        ✅ Date picker (From and To Date)
        ✅ Textarea (Comments)
        ✅ Form submit
        ✅ Success toast validation
    - This is a very important real-world workflow in HR systems.

    What happens:
    1) Login to OrangeHRM
    2) Navigate to Leave → Apply
    3) Select leave type
    4) Enter dates
    5) Enter comment
    6) Click Apply
    7) Validate "Successfully Submitted"
    """

    # ------------------------------------------------
    # 1. OPEN LOGIN PAGE
    # ------------------------------------------------
    driver.get(config.get("base_url"))

    login = LoginPage(driver, config)
    dashboard = DashboardPage(driver, config)
    leave_page = LeaveApplyPage(driver, config)

    # ------------------------------------------------
    # 2. LOGIN
    # ------------------------------------------------
    login.login(config.username, config.password)
    assert dashboard.verify_login_success(), "Login failed. Cannot apply leave."

    # ------------------------------------------------
    # 3. GO TO LEAVE MODULE
    # ------------------------------------------------
    dashboard.go_to_leave()

    # ------------------------------------------------
    # 4. GET DATA FROM CURRENT ROW
    # ------------------------------------------------
    leave_type = row["leave_type"]        # Example: "CAN - Personal"
    from_date = row["from_date"]          # Example: "2026-03-28"
    to_date = row["to_date"]              # Example: "2026-03-28"
    comment = row["comment"]              # Any comment message

    # ------------------------------------------------
    # 5. APPLY LEAVE
    # ------------------------------------------------
    leave_page.apply_leave(
        leave_type=leave_type,
        from_date=from_date,
        to_date=to_date,
        comment=comment
    )

    # ------------------------------------------------
    # 6. VALIDATION
    # ------------------------------------------------
    assert leave_page.verify_leave_submitted(), \
        "Leave was NOT successfully submitted."