# cypherware-webapp/tests/api/api_utils/api_client.py
import requests
import logging
from typing import Optional, Dict, Any
from tests.api.config.api_settings import Config
from tests.api.config.endpoints import Endpoints

logger = logging.getLogger(__name__)

class APIClient:
    """Wrapper for API requests with built-in authentication and retry logic"""

    def __init__(self, base_url: str = None):
        self.base_url = base_url or Config.BASE_URL
        self.session = requests.Session()
        self.token = None
        self.session.headers.update(Config.DEFAULT_HEADERS)

    def login(self, email="admin@cypherware.com", password="password123"):
        """
        Performs authentication against the /api/login endpoint.
        If successful, it updates the session headers with the JWT token.
        """
        url = f"{self.base_url}{Endpoints.LOGIN}"
        payload = {"email": email, "password": password}

        logger.info(f"Initiating login request to {url} for user: {email}")

        try:
            # Send the login request
            response = self.session.post(url, json=payload)

            # If the server returns 200, we extract the token
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("token")
                # (GET, POST, DELETE) will automatically include this token.
                self.session.headers.update({
                    "Authorization": f"Bearer {self.token}"
                })

                logger.info("Login successful. JWT token applied to session headers.")
                return response
            else:
                logger.error(f"Login failed. Status: {response.status_code}, Msg: {response.text}")
                return response

        except Exception as e:
            logger.error(f"Error during login process: {str(e)}")
            raise

    def set_auth_token(self, token: str):
        """Set authentication token"""
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        self.token = token

    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make HTTP request with error handling"""
        url = f"{self.base_url}{endpoint}"

        # Add timeout if not specified
        if 'timeout' not in kwargs:
            kwargs['timeout'] = Config.TEST_TIMEOUT

        logger.debug(f"Making {method} request to {url}")

        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise

    # HTTP method shortcuts
    def get(self, endpoint: str, params: Optional[Dict] = None, **kwargs):
        return self._request("GET", endpoint, params=params, **kwargs)

    def post(self, endpoint: str, data: Optional[Dict] = None, json: Optional[Dict] = None, **kwargs):
        return self._request("POST", endpoint, data=data, json=json, **kwargs)

    def put(self, endpoint: str, data: Optional[Dict] = None, json: Optional[Dict] = None, **kwargs):
        return self._request("PUT", endpoint, data=data, json=json, **kwargs)

    def patch(self, endpoint: str, data: Optional[Dict] = None, json: Optional[Dict] = None, **kwargs):
        return self._request("PATCH", endpoint, data=data, json=json, **kwargs)

    def delete(self, endpoint: str, **kwargs):
        return self._request("DELETE", endpoint, **kwargs)
