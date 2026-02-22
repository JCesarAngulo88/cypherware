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

    def login(self, username: str = None, password: str = None):
        """Login and set auth token"""
        credentials = {
            "username": username or Config.USERNAME,
            "password": password or Config.PASSWORD
        }

        response = self.post(Endpoints.LOGIN, json=credentials)
        token = response.json().get("access_token")
        if token:
            self.set_auth_token(token)
        return response