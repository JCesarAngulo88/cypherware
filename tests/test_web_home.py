import pytest
import time
from tests.test_data import *
from pages.home_page import HomePage
from pages.contact_page import ContactPage

import logging
logger = logging.getLogger(__name__)

@pytest.mark.usefixtures("driver")
class TestHomePage:

    @pytest.mark.debug
    def test_home_page(self, driver):
        logger.info("\nTest Home Page")
        home = HomePage(driver)
        home.open_home()
        title_result = home.get_home_title()
        header1_result = home.get_header1_text()
        header2_result = home.get_header2_text()
        header3_result = home.get_header3_text()
        # Assertions
        assert title_result == HOME_PAGE_TITLE, f"Fail! Expected result: {HOME_PAGE_TITLE}. Actual Result {title_result}"
        logger.info(f"Pass! Expected result: {HOME_PAGE_TITLE} . Actual Result {title_result}")
        assert header1_result == HOME_HEADER_1, f"Fail! Expected result: {HOME_HEADER_1}. Actual Result {header1_result}"
        logger.info(f"Pass! Expected result: {HOME_PAGE_TITLE} . Actual Result {header1_result}")
        assert header2_result == HOME_HEADER_2, f"Fail! Expected result: {HOME_HEADER_2}. Actual Result {header2_result}"
        logger.info(f"Pass! Expected result: {HOME_PAGE_TITLE} . Actual Result {header2_result}")
        assert header3_result == HOME_HEADER_3, f"Fail! Expected result: {HOME_HEADER_3}. Actual Result {header3_result}"
        logger.info(f"Pass! Expected result: {HOME_PAGE_TITLE} . Actual Result {header3_result}")

    @pytest.mark.debug
    def test_return_home_page(self, driver):
        logger.info("\nTest Return Home Page")
        home = HomePage(driver)
        contact = ContactPage(driver)
        home.open_home()
        title_result = home.get_home_title()
        header1_result = home.get_header1_text()
        header2_result = home.get_header2_text()
        header3_result = home.get_header3_text()
        
        home.go_to_contact()
        
        cont_h1 = contact.get_contact_header1_text()
        logger.info(f"Contact H1: {cont_h1}")

        contact.return_home_page()

        title_result_return = home.get_home_title()
        header1_result_return = home.get_header1_text()
        header2_result_return = home.get_header2_text()
        header3_result_return = home.get_header3_text()
        assert title_result == title_result_return
        assert header1_result == header1_result_return
        assert header2_result == header2_result_return
        assert header3_result == header3_result_return

        # Assertions
        assert title_result == title_result_return, f"Fail! Expected result: {title_result}. Actual Result {title_result_return}"
        logger.info(f"Pass! Expected result: {title_result_return}. Actual Result {title_result}")
        assert header1_result == header1_result_return, f"Fail! Expected result: {header1_result}. Actual Result {header1_result_return}"
        logger.info(f"Pass! Expected result: {header1_result}. Actual Result {header1_result_return}")
        assert header2_result == header2_result_return, f"Fail! Expected result: {header2_result}. Actual Result {header2_result_return}"
        logger.info(f"Pass! Expected result: {header2_result}. Actual Result {header2_result_return}")
        assert header3_result == header3_result_return, f"Fail! Expected result: {header3_result}. Actual Result {header3_result_return}"
        logger.info(f"Pass! Expected result: {header3_result}. Actual Result {header3_result_return}")
