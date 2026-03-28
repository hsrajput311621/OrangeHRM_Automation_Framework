import pytest

from Utils.DataReader import DataReader
from Pages.LoginPage import LoginPage
from Pages.DashboardPage import DashboardPage
from Pages.MyInfo.MyInfoPersonalDetailsPage import MyInfoPersonalDetailsPage

# ---------------------------------------------------------
# LOAD TEST DATA (JSON + CSV + Excel)
# ---------------------------------------------------------

testdata_json = DataReader("TestData/update_personal_details.json").get_data()
testdata_csv = DataReader("TestData/update_personal_details.csv").get_data()
testdata_excel = DataReader("TestData/update_personal_details.xlsx").get_data()

all_test_data = testdata_json + testdata_csv + testdata_excel


@pytest.mark.parametrize("row", all_test_data)
def test_update_personal_details(row, driver, config):
    """
    Why this test:
    - To verify that a logged-in user can update their personal details.
    - This covers many UI concepts:
        ✅ Dropdown (nationality, marital status)
        ✅ Date picker
        ✅ Text input fields
        ✅ Radio buttons (gender)
        ✅ Save button
        ✅ Validation of success toast

    Steps:
    1) Login
    2) Go to My Info → Personal Details
    3) Update all fields using data from test file
    4) Save
    5) Validate success message
    """

    # -----------------------------------------
    # 1. OPEN LOGIN PAGE
    # -----------------------------------------
    driver.get(config.get("base_url"))

    login = LoginPage(driver, config)
    dashboard = DashboardPage(driver, config)
    myinfo = MyInfoPersonalDetailsPage(driver, config)

    # -----------------------------------------
    # 2. LOGIN
    # -----------------------------------------
    login.login(config.username, config.password)
    assert dashboard.verify_login_success(), "Login failed. Cannot update personal details."

    # -----------------------------------------
    # 3. GO TO MY INFO MODULE
    # -----------------------------------------
    dashboard.go_to_my_info()

    # -----------------------------------------
    # 4. EXTRACT DATA FROM TEST ROW
    # -----------------------------------------
    first = row["first_name"]
    middle = row["middle_name"]
    last = row["last_name"]
    nickname = row["nickname"]
    emp_id = str(row["employee_id"])
    nationality = row["nationality"]  # Example: "Indian"
    marital_status = row["marital_status"]  # Example: "Single"
    gender = row["gender"]  # "Male" or "Female"
    dob = row["dob"]  # yyyy-mm-dd

    # -----------------------------------------
    # 5. RUN UPDATE WORKFLOW
    # -----------------------------------------
    myinfo.update_personal_details(
        first=first,
        middle=middle,
        last=last,
        nickname=nickname,
        emp_id=emp_id,
        nationality=nationality,
        marital_status=marital_status,
        gender=gender,
        dob=dob
    )

    # -----------------------------------------
    # 6. VALIDATION
    # -----------------------------------------
    assert myinfo.verify_update_success(), \
        "Personal details were NOT updated successfully."