import requests
from client import SpireClient

class BaseClient:
    def __init__(self, client: SpireClient):
        self.client = client

    def _get(self, endpoint, params=None):
        url = f"{self.client.base_url}/{endpoint.lstrip('/')}"
        response = requests.get(url, auth=self.client.auth, headers=self.client.headers, params=params)
        response.raise_for_status()
        return response.json()

    def _post(self, endpoint, data=None, json=None):
        url = f"{self.client.base_url}/{endpoint.lstrip('/')}"
        response = requests.post(url, auth=self.client.auth, headers=self.client.headers, data=data, json=json)
        return self._handle_response(response)

    def _put(self, endpoint, data=None, json=None):
        url = f"{self.client.base_url}/{endpoint.lstrip('/')}"
        response = requests.put(url, auth=self.client.auth, headers=self.client.headers, data=data, json=json)
        response.raise_for_status()
        return response.json()

    def _delete(self, endpoint):
        url = f"{self.client.base_url}/{endpoint.lstrip('/')}"
        response = requests.delete(url, auth=self.client.auth, headers=self.client.headers)
        return self._handle_response(response)
    
    def _handle_response(self, response):
        try:

            content = response.json()
        except ValueError:
            content = response.text
        return{
            "status_code": response.status_code,
            "url": response.url,
            "content": content
        }
        