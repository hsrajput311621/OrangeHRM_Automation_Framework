import requests

class APIClient:
    """
    Simple wrapper for all API calls.
    It makes GET, POST, DELETE easy.
    """

    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint, headers=None):
        return requests.get(self.base_url + endpoint, headers=headers)

    def post(self, endpoint, json=None, headers=None):
        return requests.post(self.base_url + endpoint, json=json, headers=headers)

    def delete(self, endpoint, headers=None):
        return requests.delete(self.base_url + endpoint, headers=headers)