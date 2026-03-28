import pytest

from Utils.DataReader import DataReader
from Pages.LoginPage import LoginPage
from Pages.DashboardPage import DashboardPage
from Pages.Time.TimePunchPage import TimePunchPage


# ---------------------------------------------------------
# LOAD TEST DATA (JSON + CSV + Excel)
# ---------------------------------------------------------

testdata_json = DataReader("TestData/punch_time.json").get_data()
testdata_csv = DataReader("TestData/punch_time.csv").get_data()
testdata_excel = DataReader("TestData/punch_time.xlsx").get_data()

# Combine all → full data-driven testing
all_test_data = testdata_json + testdata_csv + testdata_excel


@pytest.mark.parametrize("row", all_test_data)
def test_punch_time(row, driver, config):
    """
    Why this test:
    - To verify Punch In and Punch Out functionality inside the Time module.
    - This is a very important HR workflow.
    - This test covers:
        ✅ Punch In
        ✅ Punch Out
        ✅ Typing comment
        ✅ Reading punch time
        ✅ Validating success toast

    What happens:
    1) Login to OrangeHRM
    2) Navigate to Time → Punch In/Out
    3) Enter comment
    4) Punch In
    5) Verify success + read punch time
    6) Punch Out
    7) Verify success + read punch time
    """

    # ------------------------------------------------
    # 1. OPEN LOGIN PAGE
    # ------------------------------------------------
    driver.get(config.get("base_url"))

    login = LoginPage(driver, config)
    dashboard = DashboardPage(driver, config)
    punch_page = TimePunchPage(driver, config)

    # ------------------------------------------------
    # 2. LOGIN
    # ------------------------------------------------
    login.login(config.username, config.password)
    assert dashboard.verify_login_success(), "Login failed. Cannot punch time."

    # ------------------------------------------------
    # 3. NAVIGATE TO TIME MODULE
    # ------------------------------------------------
    dashboard.go_to_time()

    # ------------------------------------------------
    # 4. GET DATA
    # ------------------------------------------------
    punch_in_comment = row["punch_in_comment"]
    punch_out_comment = row["punch_out_comment"]

    # ------------------------------------------------
    # 5. PUNCH IN
    # ------------------------------------------------
    punch_page.punch_in(comment=punch_in_comment)

    assert punch_page.verify_punch_success(), \
        "Punch In was NOT successful."

    punch_in_time = punch_page.get_punch_time()
    print(f"Punched In at: {punch_in_time}")

    # ------------------------------------------------
    # 6. PUNCH OUT
    # ------------------------------------------------
    punch_page.punch_out(comment=punch_out_comment)

    assert punch_page.verify_punch_success(), \
        "Punch Out was NOT successful."

    punch_out_time = punch_page.get_punch_time()
    print(f"Punched Out at: {punch_out_time}")