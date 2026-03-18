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

    @pytest.mark.smoke
    def test_contact_get_all_contacts(self, authenticated_client):
        """
        Verifies endpoint: Get all contacts saved.
        """
        logger.info("\n\nCheck the endpoint: Get all contacts...")
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


    @pytest.mark.smoke
    @pytest.mark.parametrize("id_contact", "1")
    def test_contact_get_contact_id(self, authenticated_client, id_contact):
        """
        Verifies endpoint: Get all contacts saved.
        """
        logger.info("\n\nCheck the endpoint: Get contact by ID...")
        response = authenticated_client.get(Endpoints.CONTACTS_BY_ID + id_contact)

        assert response.status_code == 200, f"\nFail. Expected 200 but got {response.status_code}"
        logger.info(f"\nPass. Expected code: 200. API Response: {response.status_code}")

        # Get data json
        response_json = response.json()
        logger.info(f"\nPass. Expected data: {response_json}")

    @pytest.mark.debug
    def test_create_new_contact(self, authenticated_client):
        logger.info("Verify endpoint: Create new contact...")
        new_contact_payload = {
            "user_name": "Alaaaaaa",
            "email_address": "newUsertest@cypherware.com",
            "phone_number": "1234567890",
            "service_type": "QA Services",
            "project_name": "Validation Test",
            "project_description": "Testing missing fields"
        }

        response = authenticated_client.post(Endpoints.CONTACTS, json=new_contact_payload, headers=authenticated_client.session.headers)
        data = response.json()
        logger.info(f"\nData response: {data}")
        logger.info(f"\nContent response: {response.headers.get("Content-Type")}")
        logger.info(f"\nContent response length: {response.headers.get("Content-Length")}")
        logger.info(f"\nSession Headers: {authenticated_client.session.headers}")

        if response.status_code != 201:
            logger.error(f"Validation Failed! Server says: {response.json().get('message')}")
        assert response.status_code == 201, f"\nFail. Expected 400 but got {response.status_code}"
        logger.info(f"\nPass. Expected code: 201. API Response: {response.status_code}")

        from server import app, db, Contact  # Import your app and model
        with app.app_context():
            # Use a list comprehension to pull only the names
            contact_names = [c.user_name for c in Contact.query.all()]

            print("List of Contact Names:")
            print(contact_names)
            assert new_contact_payload["user_name"] in contact_names, f"\nFail. Expected {new_contact_payload["user_name"]} but got {contact_names}"
            logger.info(f"\nPass. Expected name {new_contact_payload["user_name"]} DB Response: {contact_names}")






    @pytest.mark.smoke
    def test_error_missing_fields(self, authenticated_client):
        """Verify 400 error when required fields are missing"""
        # Sending a payload missing 'service_type' and 'project_name'
        logger.info("\n\nCheck Error 400 when incomplete payload was provided: ...")
        incomplete_payload = {
            "user_name": "Error Tester",
            "email_address": "test@error.com",
            "phone_number": "1234567890",
            "project_description": "Testing missing fields"
        }

        response = authenticated_client.post(Endpoints.CONTACTS, json=incomplete_payload, raise_error=False)
        assert response.status_code == 400, f"\nFail. Expected 400 but got {response.status_code}"
        logger.info(f"\nPass. Expected code: 400. API Response: {response.status_code}")
        data = response.json()
        assert "Missing required fields" == data["error"], f"\nFail. Expected 'Missing required fields' but got {data['error']}"
        logger.info(f"\nPass. Expected 'Missing required fields' but got {data['error']}")

    @pytest.mark.smoke
    def test_error_invalid_email_format(self, authenticated_client):
        logger.info("\n\nVerify 422 error for logically invalid data (missing @)")
        bad_email_payload = {
            "user_name": "Bad Email",
            "email_address": "invalid-email-string",  # No @ symbol
            "phone_number": "1234567890",
            "service_type": "QA",
            "project_name": "Validation Test",
            "project_description": "Testing email validation"
        }

        response = authenticated_client.post(Endpoints.CONTACTS, json=bad_email_payload, raise_error=False)
        data = response.json()
        logger.info(f"\nData: {data}")
        assert response.status_code == 422, f"\nFail. Expected code: 422. API Response: {response.status_code}"
        logger.info(f"\nPass. Expected code: 422. API Response: {response.status_code}")
        assert response.json()["message"] == "Invalid email format", f"\nFail. Expected: Invalid email format. API Response: {response.json()["message"]}"

    @pytest.mark.smoke
    def test_error_unsupported_media_type(self, authenticated_client):
        logger.info("\n\nVerify 415 error when sending plain text instead of JSON")
        headers = authenticated_client.session.headers.copy()
        headers["Content-Type"] = "text/plain"

        # Request directly here to bypass the automatic JSON formatting
        response = authenticated_client.post(
            Endpoints.CONTACTS,
            data="This is just plain text",
            headers=headers,
            raise_error=False
        )
        data = response.json()
        logger.info(f"\nData response: {data}")
        assert response.status_code == 415, f"Fail. Expected 415 but got {response.status_code}"
        logger.info(f"\nPass. Expected code: 415. API Response: {response.status_code}")
        assert "Content-Type must be application/json" in response.json()["message"], f"\nFail. Expected message: Content-Type must be application/json.API Response {response.json()["message"]}"

    @pytest.mark.smoke
    def test_error_unauthorized_access(self, api_client):
        logger.info("\n\nVerify Error code 401 when authenticated is skipped")
        # Using a fresh requests call without the authenticated session
        response = api_client.post(Endpoints.CONTACTS, json={}, raise_error=False)
        data = response.json()
        logger.info(f"\nData: {data}")
        assert response.status_code == 401, f"Fail. Expected 401 but got {response.status_code}"
        logger.info(f"\nPass. Expected code: 401. API Response: {response.status_code}")
        assert "Token is missing" in response.json().get("message", response.json().get("error")), f"Fail. Expected message: Token is missing. API Response: {response.json().get("message", response.json().get("error"))}"
        logger.info(f"Fail. Expected message: Token is missing. API Response: {response.json().get("message", response.json().get("error"))}")