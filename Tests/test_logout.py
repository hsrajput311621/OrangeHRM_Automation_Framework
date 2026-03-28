import pytest
from Pages.LoginPage import LoginPage
from Pages.DashboardPage import DashboardPage


@pytest.mark.usefixtures("driver", "config")
def test_logout(driver, config):
    """
    Why this test:
    - To verify that a logged-in user can successfully log out.
    - Logout is a very important basic functionality.
    - Interviewers often ask about login + logout flow.

    What happens:
    1) Open login page
    2) Login with valid credentials (from .env)
    3) Verify dashboard is visible
    4) Open user dropdown
    5) Click logout
    6) Verify we return to the login page
    """

    # ----------------------------------------
    # 1. OPEN LOGIN PAGE
    # ----------------------------------------
    driver.get(config.get("base_url"))

    login = LoginPage(driver, config)
    dashboard = DashboardPage(driver, config)

    # ----------------------------------------
    # 2. LOGIN USING VALID USERNAME & PASSWORD
    # (These come from .env file)
    # ----------------------------------------
    login.login(config.username, config.password)

    # ----------------------------------------
    # 3. VERIFY LOGIN SUCCESSFUL
    # ----------------------------------------
    assert dashboard.verify_login_success() is True, \
        "Login failed, cannot perform logout."

    # ----------------------------------------
    # 4. OPEN USER DROPDOWN MENU
    # ----------------------------------------
    dashboard.open_user_dropdown()

    # ----------------------------------------
    # 5. CLICK LOGOUT BUTTON
    # ----------------------------------------
    dashboard.click_logout()

    # ----------------------------------------
    # 6. VERIFY WE RETURNED TO LOGIN PAGE
    # ----------------------------------------
    current_url = driver.current_url
    assert "auth/login" in current_url, \
        "Logout failed. User is not on login page."