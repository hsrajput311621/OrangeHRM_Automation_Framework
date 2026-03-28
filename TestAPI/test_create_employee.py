import pytest
from API.endpoints import CREATE_EMPLOYEE

testdata = {
    "firstName": "John",
    "lastName": "Doe",
    "email": "john.doe@example.com"
}

def test_create_employee(api_client):
    """
    Why this test:
    - This simulates creating a new employee using API.
    - POST API test is MUST for interviews.

    Steps:
    1) Send POST request with JSON body
    2) Validate 201 status code
    3) Validate new employee ID is returned
    """

    response = api_client.post(CREATE_EMPLOYEE, json=testdata)

    assert response.status_code in [200, 201], "Employee creation failed."

    data = response.json()

    assert "id" in data, "API did not return employee ID."
    assert data["firstName"] == testdata["firstName"]