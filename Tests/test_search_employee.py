import pytest

from Utils.DataReader import DataReader
from Pages.LoginPage import LoginPage
from Pages.DashboardPage import DashboardPage
from Pages.PIM.SearchEmployeePage import SearchEmployeePage


all_test_data = DataReader.merge_data_files(
    "TestData/search_employee.json",
    "TestData/search_employee.csv",
    "TestData/search_employee.xlsx",
    require_keys=("search_type", "employee_name", "employee_id"),
)


@pytest.mark.parametrize("row", all_test_data)
def test_search_employee(row, driver, config):
    """
    Why this test:
    - To verify employee search works correctly.
    - To check both 'search by name' and 'search by employee ID'.
    - This is a real-time feature in HR systems.
    - Interviewers often test table validation logic.

    What happens:
    1) Login
    2) Go to PIM → Employee List (default)
    3) Fill search fields (name or id)
    4) Click Search
    5) Validate table results
    """

    # -----------------------------------------
    # 1. OPEN LOGIN PAGE
    # -----------------------------------------
    driver.get(config.get("base_url"))

    login = LoginPage(driver, config)
    dashboard = DashboardPage(driver, config)
    search_page = SearchEmployeePage(driver, config)

    # -----------------------------------------
    # 2. LOGIN USING VALID CREDENTIALS
    # -----------------------------------------
    login.login(config.username, config.password)
    assert dashboard.verify_login_success(), "Login failed; cannot search employee."

    # -----------------------------------------
    # 3. NAVIGATE TO PIM → Employee List
    # -----------------------------------------
    dashboard.go_to_pim()

    # -----------------------------------------
    # 4. GET DATA FROM CURRENT ROW
    # -----------------------------------------
    emp_name = row.get("employee_name")
    emp_id = str(row.get("employee_id")) if row.get("employee_id") else None
    search_type = row.get("search_type")   # name / id

    # -----------------------------------------
    # 5. PERFORM SEARCH
    # -----------------------------------------
    if search_type == "name":
        search_page.search_employee(name=emp_name)

        # Validate employee is present in table
        assert search_page.validate_employee_present(emp_name), \
            f"Employee '{emp_name}' not found in results."

    elif search_type == "id":
        search_page.search_employee(emp_id=emp_id)

        # Validate employee ID in table
        assert search_page.validate_employee_id_present(emp_id), \
            f"Employee ID '{emp_id}' not found in results."

    else:
        raise ValueError("Invalid search_type. Must be 'name' or 'id'.")