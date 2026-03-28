import pytest

from Pages.LoginPage import LoginPage
from Pages.DashboardPage import DashboardPage
from Pages.Recruitment.RecruitmentCandidatesListPage import RecruitmentCandidatesListPage


def test_delete_candidate(driver, config):
    """
    This test deletes a candidate from Recruitment → Candidates list.

    Steps:
    1. Login
    2. Go to Recruitment module
    3. Search the candidate
    4. Select checkbox
    5. Click delete
    6. Confirm deletion
    7. Validate success toast
    """

    # 1. Open login page
    driver.get(config.get("base_url"))

    login = LoginPage(driver, config)
    dashboard = DashboardPage(driver, config)
    candidates_page = RecruitmentCandidatesListPage(driver, config)

    # 2. Login
    login.login(config.username, config.password)
    assert dashboard.verify_login_success(), "Login failed"

    # 3. Go to Recruitment module
    dashboard.go_to_recruitment()

    # Candidate name to delete
    candidate_name = "John Smith"   # You can make it data-driven later

    # 4. Search candidate
    candidates_page.search_candidate(candidate_name)

    # 5. Select candidate checkbox
    assert candidates_page.select_candidate_checkbox(), \
        "Candidate not found in the list"

    # 6. Delete candidate
    candidates_page.delete_candidate()

    # 7. Validate
    assert candidates_page.verify_success(), "Candidate NOT deleted!"