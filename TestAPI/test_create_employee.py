import pytest

from API.endpoints import CREATE_EMPLOYEE

# Sample body — OrangeHRM v2 may require extra fields (employeeId, etc.).
# Adjust to match your API contract once you have a valid token.
testdata = {
    "firstName": "John",
    "lastName": "Doe",
}


def test_create_employee(api_client):
    """
    Why:
    - POST + JSON body is a standard pattern to demonstrate in interviews.

    Steps:
    1) POST to CREATE_EMPLOYEE with testdata.
    2) Expect 200/201 when token and payload match the server schema.

    If this fails with 4xx:
    - Open the response body in the failure log and align `testdata` with OrangeHRM docs.
    """
    response = api_client.post(CREATE_EMPLOYEE, json=testdata)

    assert response.status_code in (200, 201), (
        f"Create failed ({response.status_code}): {response.text[:800]}"
    )

    data = response.json()
    # Server may return id, empNumber, or nested data — accept common shapes.
    emp_id = data.get("id") or data.get("empNumber") or (data.get("data") or {}).get("empNumber")
    assert emp_id is not None, f"Could not find new employee id in response: {data!r}"
