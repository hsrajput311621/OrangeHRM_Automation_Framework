import pytest
from API.endpoints import GET_EMPLOYEES

def test_get_employees(api_client):
    """
    Why this test:
    - To check if Get Employees API works correctly.
    - Interviewers ALWAYS ask GET request validation.

    What will happen:
    1) Send GET request
    2) Validate status code
    3) Validate data list is not empty
    """

    response = api_client.get(GET_EMPLOYEES)

    # 1. Status code check
    assert response.status_code == 200, "GET employees API failed."

    data = response.json()

    # 2. Response is list or contains data list
    assert isinstance(data, list), "Employees API must return a list."

    # 3. There should be at least 1 employee (demo data)
    assert len(data) > 0, "Employees list is empty."