import pytest

from API.endpoints import GET_EMPLOYEES


def test_get_employees(api_client):
    """
    Why this test:
    - Proves you can call a secured GET endpoint and parse JSON (common interview topic).

    Step-by-step:
    1) api_client builds URL: BASE_API + GET_EMPLOYEES (see API/endpoints.py).
    2) requests sends GET with Bearer token from ORANGEHRM_API_TOKEN (see conftest).
    3) We assert HTTP 200 and that the payload contains a list of employees
       (OrangeHRM often wraps the array in a `data` key).

    Note:
    - Without a token this file is never executed — TestAPI/conftest.py skips these tests.
    """
    response = api_client.get(GET_EMPLOYEES)

    assert response.status_code == 200, f"Unexpected status: {response.status_code}\n{response.text[:500]}"

    payload = response.json()
    # v2 APIs frequently return {"data": [...], "meta": ...} instead of a bare list.
    records = payload if isinstance(payload, list) else payload.get("data")
    assert records is not None, f"Unexpected JSON shape: {payload!r}"
    assert isinstance(records, list), "Expected a list (or .data list) of employees."
    assert len(records) > 0, "Demo tenant usually has employees; empty list may mean wrong token or URL."
