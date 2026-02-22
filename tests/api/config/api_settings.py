# cypherware-webapp/tests/api/config/api_settings.py
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration settings for API testing"""

    # Base URLs
    BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:5001")
    #STAGING_URL = os.getenv("STAGING_URL", "https://staging-api.example.com")

    # Authentication
    API_KEY = os.getenv("API_KEY", "your-api-key-here")
    USERNAME = os.getenv("API_USERNAME", "testuser")
    PASSWORD = os.getenv("API_PASSWORD", "testpass")

    # Test settings
    TEST_TIMEOUT = int(os.getenv("TEST_TIMEOUT", 30))
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))

    # Headers
    DEFAULT_HEADERS = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }