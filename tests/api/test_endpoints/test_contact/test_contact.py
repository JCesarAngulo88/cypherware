# pytest -v -s -m debug tests/api/test_endpoints/test_contact/test_contact.py
import pytest
import time
import logging
logger = logging.getLogger(__name__)
from tests.api.config.endpoints import Endpoints

class TestContact:
    """
        Test Suite for verifying the Contacts API endpoints.
        Covers listing, creating, and data integrity.
        CONTACTS = "/api/contacts"
        CONTACTS_BY_ID = "/api/contacts/{id}"
    """

    @pytest.mark.debug
    def test_contact_get_all_contacts(self, authenticated_client):
        """
        Verifies endpoint: Get all contacts saved.
        """
        start_time = time.time()
        response = authenticated_client.get(Endpoints.CONTACTS)
        end_time = time.time()

        assert response.status_code == 200, f"\nFail. Expected 200 but got {response.status_code}"
        logger.info(f"\nPass. Expected code: 200. API Response: {response.status_code}")

        # Get data json
        response_json = response.json()
        logger.info(f"\n\nPass. Expected data: {response_json}\n\n")
        assert isinstance(response_json, list), f"\nFail. Expected a list of contacts, Received: {type(response_json)}"
        logger.info(f"\nPass. Expected list. API Response: {type(response_json)}")

        # Verify structure of the first contact if records exist
        logger.info(f"\nResponse Length = {len(response_json)}")
        if len(response_json) > 0:
            contact = response_json[0]
            expected_keys = ["id", "user_name", "email_address", "service_type"]
            for key in expected_keys:
                assert key in contact, f"\nFail. Missing key '{key}' in contact record"
                logger.info(f"\nPass. Ket matched {key}")

        # Response Time validation
        response_time = end_time - start_time
        assert response_time < .5, f"\nResponse time {response_time:.2f}s exceeded .5s"
        logger.info(f"\nPass. Expected time: T<500ms. API Response Time: {response_time}")


    @pytest.mark.debug
    @pytest.mark.parametrize("id_contact", "1")
    def test_contact_get_contact_id(self, api_client, id_contact):
        """
        Verifies endpoint: Get all contacts saved.
        """
        response = api_client.get(Endpoints.CONTACTS_BY_ID + id_contact)

        assert response.status_code == 200, f"\nFail. Expected 200 but got {response.status_code}"
        logger.info(f"\nPass. Expected code: 200. API Response: {response.status_code}")

        # Get data json
        response_json = response.json()
        logger.info(f"\nPass. Expected data: {response_json}")
