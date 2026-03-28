import pytest

from API.endpoints import CREATE_EMPLOYEE, DELETE_EMPLOYEE
from Pages.LoginPage import LoginPage
from Pages.DashboardPage import DashboardPage
from Pages.PIM.SearchEmployeePage import SearchEmployeePage


def test_api_ui_employee_flow(api_client, driver, config):
    """
    COMPLETE HYBRID TEST (API + UI)

    Steps:
    1) Create Employee using API
    2) Login using UI
    3) Search employee in PIM → must exist
    4) Delete employee using API
    5) Search employee again → must NOT exist
    """

    # -------------------------------------
    # 1. CREATE EMPLOYEE USING API
    # -------------------------------------
    create_body = {
        "firstName": "APIUser",
        "middleName": "Test",
        "lastName": "Automation"
    }

    response = api_client.post(CREATE_EMPLOYEE, json=create_body)
    assert response.status_code in [200, 201]

    employee_id = response.json().get("id")
    assert employee_id, "API did not return Employee ID"

    # -------------------------------------
    # 2. LOGIN USING UI
    # -------------------------------------
    driver.get(config.get("base_url"))
    login = LoginPage(driver, config)
    dashboard = DashboardPage(driver, config)
    search_page = SearchEmployeePage(driver, config)

    login.login(config.username, config.password)
    assert dashboard.verify_login_success()

    # -------------------------------------
    # 3. SEARCH EMPLOYEE IN UI (SHOULD EXIST)
    # -------------------------------------
    dashboard.go_to_pim()
    search_page.search_employee(emp_id=str(employee_id))

    assert search_page.validate_employee_id_present(str(employee_id)), \
        "Employee DOES NOT exist in UI after API creation"

    # -------------------------------------
    # 4. DELETE EMPLOYEE USING API
    # -------------------------------------
    delete_response = api_client.delete(DELETE_EMPLOYEE + str(employee_id))
    assert delete_response.status_code in [200, 204]

    # -------------------------------------
    # 5. SEARCH AGAIN IN UI (SHOULD NOT EXIST)
    # -------------------------------------
    search_page.search_employee(emp_id=str(employee_id))
    assert not search_page.validate_employee_id_present(str(employee_id)), \
        "Employee still exists in UI after API deletion"