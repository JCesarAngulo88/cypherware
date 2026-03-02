import pytest
import logging
import time
from pages.contact_page import ContactPage
from tests.web.contact.test_data_contact import *
logger = logging.getLogger(__name__)

@pytest.mark.usefixtures("driver")
class TestContactPage:

    @pytest.mark.parametrize("contact_name", DATA_TEST_FULL_NAME_INPUT_FIELD)
    @pytest.mark.debug
    def test_valid_name_input_field(self, driver, contact_name):
        logger.info("\nTest name: Input Valid Name")
        logger.info("\nTest ID: WC_1")

        contact = ContactPage(driver)
        contact.open_contact()
        time.sleep(2)
        form_header = contact.get_contact_header1_text()
        logger.info(f"\nThe Form title is: {form_header}")

        assert form_header == FORM_CONTACT_NAME, f"\nFail. The Form title expected: {FORM_CONTACT_NAME}, The Form title received: {form_header}"
        logger.info(f"\nPass. The Form title expected: {FORM_CONTACT_NAME}, The Form title received: {form_header}")

        contact.write_input_name(contact_name)
        time.sleep(2)

        actual_full_name = contact.get_input_full_name()
        logger.info(f"\nThe Full Name is: {actual_full_name}")

        assert contact_name == actual_full_name, f"Fail. Expected {'Julio Angulo'}. Received: {actual_full_name}"
        logger.info(f"Pass. Expected {'Julio Angulo'}. Received: {actual_full_name}")

    @pytest.mark.debug
    def test_valid_email_input_field(self, driver):
        logger.info("Test name: Input Valid Email")
        logger.info("Test ID: WC_2")

    @pytest.mark.debug
    def test_valid_phone_number_input_field(self, driver):
        logger.info("Test name: Input Valid Phone Number")
        logger.info("Test ID: WC_3")

    @pytest.mark.debug
    def test_valid_service_type_input_selector(self, driver):
        logger.info("Test name: Valid Selector Service Type")
        logger.info("Test ID: WC_4")

    @pytest.mark.debug
    def test_valid_project_name_input_field(self, driver):
        logger.info("Test name: Input Valid Project Name")
        logger.info("Test ID: WC_5")

    @pytest.mark.debug
    def test_valid_project_description_input_field(self, driver):
        logger.info("Test name: Input Valid Project Description")
        logger.info("Test ID: WC_1")


    #preparacion, comunicacion,soft. mantener la comunicacion para cada empresa

    #comunicacion: potencial mi comunicacion no verbal, gestos, movimientos de manos etc etc

    #skills, datos duros o datos que generen impacto

    #espectavia salarial, hacerla en un rango, preguntar mas formaciones