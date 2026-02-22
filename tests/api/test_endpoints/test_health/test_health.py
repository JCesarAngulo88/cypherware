# pytest -v -s -m debug tests/api/test_endpoints/test_health/test_health.py
import pytest
import logging
logger = logging.getLogger(__name__)
from datetime import datetime
from tests.api.config.endpoints import Endpoints


class TestHealth:
    """
    Suite for verifying API system availability and database connectivity.
    Utilizes the APIClient fixture and Endpoints configuration.
    """
    @pytest.mark.debug
    def test_api_health_endpoint(self, api_client):
        """
        Verify the health check responds within an acceptable threshold.
        """
        # Act: Use the centralized client and test_endpoints class
        response = api_client.get(Endpoints.HEALTH)

        # Assert: Status Code
        assert response.status_code == 200, f"\nFail. Expected 200 but got {response.status_code}"
        logger.info(f"\nPass. Expected code: 200. API Response: {response.status_code}")

        # Assert: JSON Body Structure
        data = response.json()
        assert data["status"] == "healthy", f"\nFail. Expected 'healthy' status, got {data['status']}"
        logger.info(f"\nPass. Expected data: 'healthy' status. API data response: {data['status']}")
        assert data["database"] == "connected", "\nFail. Database connection reported as failed"
        logger.info(f"\nPass. Expected database status: 'connected'. API database status response: {data['database']}")

        # Assert: Data Integrity (Timestamp)
        # Verify the timestamp exists and is a valid ISO format string
        try:
            timestamp_str = data["timestamp"]
            datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        except (KeyError, ValueError) as e:
            pytest.fail(f"Health check returned an invalid or missing timestamp: {e}")

    @pytest.mark.debug
    def test_health_response_time(self, api_client):
        """
        Verify the health check responds within an acceptable threshold (e.g., 500ms).
        """
        response = api_client.get(Endpoints.HEALTH)
        # elapsed.total_seconds() returns the time taken for the request
        assert response.elapsed.total_seconds() < 0.5, "\n Fail. Health check is taking too long (> 500ms)"
        logger.info(f"\nPass. Health check on time ({response.elapsed.total_seconds()} seconds)")
