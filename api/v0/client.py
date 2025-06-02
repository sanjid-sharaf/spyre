import requests
import requests.auth
from config import BASE_URL

class SpireClient:
    def __init__(self, company, username, password,):
        self.base_url = f"{BASE_URL}/{company}"
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }
        self.auth = requests.auth.HTTPBasicAuth(username, password)
        se

