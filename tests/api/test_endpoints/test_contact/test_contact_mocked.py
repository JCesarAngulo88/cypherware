import pytest
import requests_mock
import logging
logger = logging.getLogger(__name__)
from tests.api.config.endpoints import Endpoints


class TestContactsMocked:
    """
    Suite for verifying the APIClient logic using mocked responses.
    This eliminates the dependency on a running server/database.
    """

    @pytest.mark.debug
    def test_get_all_contacts_mocked(self, api_client):
        """
        GIVEN the API returns a list of contacts
        WHEN the client calls the contacts endpoint
        THEN the client should correctly parse the mocked JSON data
        """
        # 1. Define the "Fake" data we want the API to return
        mock_data = [
            {
                "id": 1,
                "user_name": "Mocked User One",
                "email_address": "mock1@example.com",
                "service_type": "QA Services"
            },
            {
                "id": 2,
                "user_name": "Mocked User Two",
                "email_address": "mock2@example.com",
                "service_type": "Web App"
            }
        ]

        # 2. Setup the Mocker to intercept the specific URL
        with requests_mock.Mocker() as m:
            endpoint_url = f"{api_client.base_url}{Endpoints.CONTACTS}"
            m.get(endpoint_url, json=mock_data, status_code=200)

            # 3. Execute the call via your actual APIClient
            response = api_client.get(Endpoints.CONTACTS)

            # 4. Assertions
            assert response.status_code == 200, f"\nFail. Expected 200 but got {response.status_code}"
            logger.info(f"\nPass. Expected code: 200. API Response: {response.status_code}")
            data = response.json()
            logger.info(f"\n\nData API response: {data}")
            assert len(data) == 2
            assert data[0]["user_name"] == "Mocked User One", f"\nFail. Expected user_name: {data[0]['user_name']}"
            logger.info(f"\n\nPass. Expected Mocked User One. API Response: {data[0]['user_name']}")
            assert data[1]["service_type"] == "Web App", f"\nFail. Expected : {data[1]['service_type']}"
            logger.info(f"\nPass. Expected: Web App. API Response: {data[1]['service_type']}")

    def test_create_contact_mocked(self, api_client, test_user_data):
        """
        GIVEN valid contact data
        WHEN the client sends a POST request
        THEN the client should receive the mocked success confirmation
        """
        # Define what the "Server" should return after a successful creation
        mock_response = {
            "message": "Contact created successfully",
            "id": 99
        }

        with requests_mock.Mocker() as m:
            endpoint_url = f"{api_client.base_url}{Endpoints.CONTACTS}"
            m.post(endpoint_url, json=mock_response, status_code=201)

            # Execute
            response = api_client.post(Endpoints.CONTACTS, json=test_user_data)

            # Assert
            assert response.status_code == 201
            assert response.json()["id"] == 99
            assert response.json()["message"] == "Contact created successfully"

    def test_get_contact_not_found_mocked(self, api_client):
        """
        GIVEN a request for a non-existent contact ID
        WHEN the API returns a 404
        THEN the client should handle the 404 status code correctly
        """
        invalid_id = 404

        with requests_mock.Mocker() as m:
            endpoint_url = f"{api_client.base_url}{Endpoints.CONTACTS}/{invalid_id}"
            m.get(endpoint_url, json={"error": "Not Found"}, status_code=404)

            response = api_client.get(f"{Endpoints.CONTACTS}/{invalid_id}")

            assert response.status_code == 404
            assert response.json()["error"] == "Not Found"

    def test_contacts_server_error_mocked(self, api_client):
        """
        GIVEN the server is experiencing internal errors (500)
        WHEN the client tries to list contacts
        THEN the client receives the 500 status code
        """
        with requests_mock.Mocker() as m:
            endpoint_url = f"{api_client.base_url}{Endpoints.CONTACTS}"
            m.get(endpoint_url, status_code=500)

            response = api_client.get(Endpoints.CONTACTS)

            assert response.status_code == 500