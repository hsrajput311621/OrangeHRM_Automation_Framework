import pytest

from Utils.DataReader import DataReader
from Pages.LoginPage import LoginPage
from Pages.DashboardPage import DashboardPage
from Pages.Recruitment.RecruitmentAddCandidatePage import RecruitmentAddCandidatePage


# require_keys drops Excel template rows (Column Name / Example Value) from parametrization.
all_test_data = DataReader.merge_data_files(
    "TestData/add_candidate.json",
    "TestData/add_candidate.csv",
    "TestData/add_candidate.xlsx",
    require_keys=("first_name", "middle_name", "last_name", "email"),
)


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
    # 3. OPEN ADD CANDIDATE (direct route — sidebar default is not this form)
    # ---------------------------------------------------------
    candidate_page.open_add_candidate()

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