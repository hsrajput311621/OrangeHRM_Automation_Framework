import pytest
from Utils.DataReader import DataReader
from Pages.LoginPage import LoginPage
from Pages.DashboardPage import DashboardPage


# ---------------------------------------------------------
# LOAD TEST DATA (JSON + CSV + optional Excel)
# ---------------------------------------------------------
# Step 1: merge_data_files reads each path that exists.
# Step 2: If login.xlsx is not in the repo (common on Jenkins), we skip it with a log
#         warning instead of crashing during pytest collection.
all_test_data = DataReader.merge_data_files(
    "TestData/login.json",
    "TestData/login.csv",
    "TestData/login.xlsx",
)


# ---------------------------------------------------------
# ✅ PARAMETRIZE TEST (runs test for each row of data)
# ---------------------------------------------------------
@pytest.mark.parametrize("row", all_test_data)
def test_login(row, driver, config):
    """
    Why this test:
    - To check login functionality with VALID and INVALID credentials.
    - To verify login success goes to Dashboard.
    - To verify login failure shows the correct error message.

    What will happen:
    - Open browser
    - Load login page
    - Enter username & password (from data)
    - Click login
    - Check expected result (success or failure)
    """

    # ----------------------------------------
    # 1. OPEN THE LOGIN PAGE
    # ----------------------------------------
    driver.get(config.get("base_url"))

    login = LoginPage(driver, config)
    dashboard = DashboardPage(driver, config)

    username = row["username"]
    password = row["password"]
    expected = row["expected"]   # "success" or "failure"

    print(f"Testing login with: {username} / {password}")

    # ----------------------------------------
    # 2. PERFORM LOGIN
    # ----------------------------------------
    login.login(username, password)

    # ----------------------------------------
    # 3. VALIDATION
    # ----------------------------------------

    if expected == "success":
        # Check dashboard loaded
        assert dashboard.verify_login_success() is True, "Login should succeed but failed."

    else:
        # Check error message
        error = login.get_error_message()
        assert error != "", "Expected an error message but none appeared."