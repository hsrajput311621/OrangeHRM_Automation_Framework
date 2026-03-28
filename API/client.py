"""
APIClient — thin wrapper around the `requests` library.

Why:
- Keeps base URL and default headers (e.g. Bearer token) in one place.
- Tests stay short: api_client.get(endpoint).

What happens on each call:
- requests merges your per-call headers with default_headers.
- Full URL = base_url + endpoint string.
"""
import requests


class APIClient:
    """Minimal HTTP client for OrangeHRM REST API v2 (Bearer auth)."""

    def __init__(self, base_url: str, default_headers=None):
        # base_url should end without trailing slash; endpoints start with "/".
        self.base_url = base_url.rstrip("/")
        self.default_headers = default_headers or {}

    def _headers(self, headers):
        merged = dict(self.default_headers)
        if headers:
            merged.update(headers)
        return merged

    def get(self, endpoint, headers=None):
        return requests.get(self.base_url + endpoint, headers=self._headers(headers))

    def post(self, endpoint, json=None, headers=None):
        return requests.post(
            self.base_url + endpoint, json=json, headers=self._headers(headers)
        )

    def delete(self, endpoint, headers=None):
        return requests.delete(self.base_url + endpoint, headers=self._headers(headers))
