import pytest
import logging
logger = logging.getLogger(__name__)

from pages.base_page import BasePage

@pytest.mark.usefixtures("driver")
class TestContactPage(BasePage):

    @pytest.mark.debug
    def test_valid_name_input_field(self, driver):
        logger.info("Test name: Input Valid Name")
        logger.info("Test ID: WC_1")
        

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