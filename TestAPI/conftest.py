"""
TestAPI-local pytest hooks.

Why:
- OrangeHRM API v2 returns 401 without a valid Bearer token.
- Failing API tests on every Jenkins run confuses beginners; we skip the API suite
  until ORANGEHRM_API_TOKEN is configured.

What happens:
- During collection, if the token env var is missing, every test in TestAPI/ gets
  a skip marker with a short explanation.
"""
import os

import pytest


def pytest_collection_modifyitems(config, items):
    if os.getenv("ORANGEHRM_API_TOKEN"):
        return
    skip_api = pytest.mark.skip(
        reason=(
            "Set ORANGEHRM_API_TOKEN in Env/.env to run API tests "
            "(OrangeHRM v2 requires Bearer authentication)."
        )
    )
    for item in items:
        if "TestAPI" in getattr(item.path, "parts", ()):
            item.add_marker(skip_api)
