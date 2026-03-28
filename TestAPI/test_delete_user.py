import os

import pytest

from API.endpoints import DELETE_USER


def test_delete_user(api_client):
    """
    Why:
    - DELETE is part of a typical CRUD demo.

    Important:
    - Deleting real users is destructive. We only run this when you explicitly set
      ORANGEHRM_DELETE_USER_ID in Env/.env so Jenkins does not remove random users.

    Steps:
    1) Read target id from the environment.
    2) DELETE {DELETE_USER}{id}.
    3) Assert a successful status code.
    """
    user_id = os.getenv("ORANGEHRM_DELETE_USER_ID")
    if not user_id:
        pytest.skip("Set ORANGEHRM_DELETE_USER_ID to run this destructive API test.")

    response = api_client.delete(f"{DELETE_USER}{user_id}")

    assert response.status_code in (200, 204), (
        f"Delete failed ({response.status_code}): {response.text[:500]}"
    )
