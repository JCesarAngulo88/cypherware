# pytest -v -s -m debug tests/api/test_endpoints/test_contact/test_contact.py
import pytest
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
        #response = api_client.get(Endpoints.CONTACTS)
        response = authenticated_client.get(Endpoints.CONTACTS)

        assert response.status_code == 200, f"\nFail. Expected 200 but got {response.status_code}"
        logger.info(f"\nPass. Expected code: 200. API Response: {response.status_code}")

        # Get data json
        response_json = response.json()
        logger.info(f"\nPass. Expected data: {response_json}")

    @pytest.mark.smoke
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
