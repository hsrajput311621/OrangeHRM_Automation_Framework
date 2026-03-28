import pytest

from Utils.DataReader import DataReader
from Pages.LoginPage import LoginPage
from Pages.DashboardPage import DashboardPage
from Pages.Admin.AdminAddUserPage import AdminAddUserPage


all_test_data = DataReader.merge_data_files(
    "TestData/add_user.json",
    "TestData/add_user.csv",
    "TestData/add_user.xlsx",
)


@pytest.mark.parametrize("row", all_test_data)
def test_add_user(row, driver, config):
    """
    Why this test:
    - To verify that admin can add a new user from Admin → User Management → Add User.
    - This flow uses dropdowns, auto-suggest, keyboard actions, inputs, and validation.
    - Interviewers frequently ask about this scenario.

    What happens:
    1) Login as Admin
    2) Navigate to Admin module
    3) Open Add User form
    4) Fill the user creation form
    5) Save user
    6) Validate success message
    """

    # -----------------------------------------
    # 1. OPEN LOGIN PAGE
    # -----------------------------------------
    driver.get(config.get("base_url"))

    login = LoginPage(driver, config)
    dashboard = DashboardPage(driver, config)
    admin_page = AdminAddUserPage(driver, config)

    # -----------------------------------------
    # 2. LOGIN USING VALID USERNAME & PASSWORD
    # -----------------------------------------
    login.login(config.username, config.password)
    assert dashboard.verify_login_success(), "Login failed. Cannot add user."

    # -----------------------------------------
    # 3. NAVIGATE TO ADMIN MODULE
    # -----------------------------------------
    dashboard.go_to_admin()

    # -----------------------------------------
    # 4. READ TEST DATA
    # -----------------------------------------
    user_role = row["user_role"]         # e.g., "Admin" or "ESS"
    employee_name = row["employee_name"] # auto-suggest name e.g., "Paul"
    status = row["status"]               # Enabled / Disabled
    username = row["username"]           # newly created user
    password = row["password"]           # new user password

    # -----------------------------------------
    # 5. PERFORM ADD USER ACTION
    # -----------------------------------------
    admin_page.add_user(
        role=user_role,
        employee_name=employee_name,
        status=status,
        username=username,
        password=password
    )

    # -----------------------------------------
    # 6. VALIDATE USER SUCCESSFULLY SAVED
    # -----------------------------------------
    assert admin_page.verify_user_saved(), "User was not saved successfully."