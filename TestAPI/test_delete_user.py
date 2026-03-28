import pytest
from API.endpoints import DELETE_USER

def test_delete_user(api_client):
    """
    Why this test:
    - DELETE API testing is a MUST for interview.
    - We simulate deleting a user by ID.

    Steps:
    1) Specify user ID
    2) Send DELETE request
    3) Check status code 200/204
    """

    user_id = 12  # example, you change based on your data

    response = api_client.delete(f"{DELETE_USER}{user_id}")

    assert response.status_code in [200, 204], "Delete user API failed."