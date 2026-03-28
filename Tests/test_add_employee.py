import pytest
from Utils.DataReader import DataReader
from Pages.LoginPage import LoginPage
from Pages.DashboardPage import DashboardPage
from Pages.PIM.AddEmployeePage import AddEmployeePage

# JSON + CSV always present; .xlsx optional (see DataReader.merge_data_files).
all_test_data = DataReader.merge_data_files(
    "TestData/add_employee.json",
    "TestData/add_employee.csv",
    "TestData/add_employee.xlsx",
)


@pytest.mark.parametrize("row", all_test_data)
def test_add_employee(row, driver, config):
    """
    Why this test:
    - To verify that a new employee can be added from PIM → Add Employee.
    - This is a very common real-time scenario in HR applications.
    - Interviewers often ask for dropdown, date picker, file upload, etc.

    What happens:
    1) Login using ADMIN
    2) Go to PIM module
    3) Click Add Employee
    4) Enter employee name + ID
    5) Upload photo (optional)
    6) Enter date of birth
    7) Click Save
    8) Verify employee profile loaded
    """

    # Step 1: Open login page
    driver.get(config.get("base_url"))

    login = LoginPage(driver, config)
    dashboard = DashboardPage(driver, config)
    add_emp = AddEmployeePage(driver, config)

    # Step 2: Login using admin credentials
    login.login(config.username, config.password)
    assert dashboard.verify_login_success(), "Login failed. Cannot add employee."

    # Step 3: Navigate to PIM module
    dashboard.go_to_pim()

    # Step 4: Click Add Employee button (OrangeHRM opens Add Employee by default)
    # If needed, you can add extra click actions here.

    # Step 5: Extract data from row
    first = row["first_name"]
    middle = row["middle_name"]
    last = row["last_name"]
    emp_id = str(row["employee_id"])
    dob = row["dob"]  # yyyy-mm-dd
    photo = row.get("photo_path")  # optional field

    # Step 6: Fill form
    add_emp.enter_first_name(first)
    add_emp.enter_middle_name(middle)
    add_emp.enter_last_name(last)
    add_emp.enter_employee_id(emp_id)

    if photo:
        add_emp.upload_photo(photo)

    add_emp.enter_dob(dob)

    # Step 7: Save
    add_emp.click_save()

    # Step 8: Validation
    assert add_emp.verify_employee_profile_loaded(), \
        "Employee profile not loaded. Add Employee failed."