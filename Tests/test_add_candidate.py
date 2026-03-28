import pytest

from Utils.DataReader import DataReader
from Pages.LoginPage import LoginPage
from Pages.DashboardPage import DashboardPage
from Pages.Recruitment.RecruitmentAddCandidatePage import RecruitmentAddCandidatePage


# ----------------------------------------------------------------
# LOAD TEST DATA (JSON + CSV + Excel)
# ----------------------------------------------------------------

testdata_json = DataReader("TestData/add_candidate.json").get_data()
testdata_csv = DataReader("TestData/add_candidate.csv").get_data()
testdata_excel = DataReader("TestData/add_candidate.xlsx").get_data()

# Combine all sources → full data-driven testing
all_test_data = testdata_json + testdata_csv + testdata_excel


@pytest.mark.parametrize("row", all_test_data)
def test_add_candidate(row, driver, config):
    """
    Why this test:
    - To verify that a recruiter/admin can add a new job candidate.
    - This covers:
        ✅ Text inputs
        ✅ Dropdown (Vacancy)
        ✅ File upload (Resume)
        ✅ Date Picker
        ✅ Notes / Keywords
        ✅ Form submission
        ✅ Success toast verification

    Steps:
    1. Login
    2. Go to Recruitment module
    3. Click 'Add Candidate'
    4. Fill full candidate form
    5. Upload resume
    6. Save candidate
    7. Validate success message
    """

    # ---------------------------------------------------------
    # 1. OPEN LOGIN PAGE
    # ---------------------------------------------------------
    driver.get(config.get("base_url"))

    login = LoginPage(driver, config)
    dashboard = DashboardPage(driver, config)
    candidate_page = RecruitmentAddCandidatePage(driver, config)

    # ---------------------------------------------------------
    # 2. LOGIN
    # ---------------------------------------------------------
    login.login(config.username, config.password)
    assert dashboard.verify_login_success(), "Login failed. Cannot add candidate."

    # ---------------------------------------------------------
    # 3. NAVIGATE TO RECRUITMENT → ADD CANDIDATE
    # ---------------------------------------------------------
    dashboard.go_to_recruitment()

    # There is an 'Add' button on Recruitment page
    # We will click it using RecruitmentAddCandidatePage high-level flow

    # ---------------------------------------------------------
    # 4. READ TEST DATA
    # ---------------------------------------------------------
    first = row["first_name"]
    middle = row["middle_name"]
    last = row["last_name"]
    email = row["email"]
    phone = row["contact_number"]
    vacancy = row["vacancy"]
    keywords = row["keywords"]
    notes = row["notes"]
    date = row["date_of_application"]       # yyyy-mm-dd
    resume = row.get("resume_path")         # optional resume path

    # ---------------------------------------------------------
    # 5. FILL ADD CANDIDATE FORM
    # ---------------------------------------------------------
    candidate_page.add_candidate(
        first=first,
        middle=middle,
        last=last,
        email=email,
        phone=phone,
        vacancy=vacancy,
        resume=resume,
        keywords=keywords,
        notes=notes,
        date=date
    )

    # ---------------------------------------------------------
    # 6. VALIDATE SUCCESS MESSAGE
    # ---------------------------------------------------------
    assert candidate_page.verify_candidate_saved(), \
        "Candidate was NOT saved successfully."