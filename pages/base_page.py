from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

import logging
logger = logging.getLogger(__name__)

class BasePage:
    def __init__(self, driver, base_url="http://127.0.0.1:5000"):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 30)

    def open(self, path="/"):
        self.driver.get(self.base_url + path)

    def find(self, locator, expected_text: str = None):
        """
            This method finds the web element locator
            Params: locator, expected_text
            Return: Object Web Element
        """
        try:
            if expected_text:
                logging.info(f"Enter in if expected_text: {expected_text}")
                self.wait.until(EC.text_to_be_present_in_element(locator, expected_text))
            return self.wait.until(EC.presence_of_element_located(locator))
        except (TimeoutException, NoSuchElementException, StaleElementReferenceException) as e:
            logger.error(f"Timeout Exception error: {e}. Check locator object: {locator}")
            return None

    # def wait_for_text(self, locator, expected_text):
    #     return self.wait.until(EC.text_to_be_present_in_element(locator, expected_text))

    def click(self, locator):
        element = self.find(locator)
        element.click()

    def type(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator, expected_text: str = None):
        try:
            return self.find(locator, expected_text).text
        except Exception as e:
            logger.error(f"Error getting text from element {locator}: {e}")
            return None
    
    def get_title(self):
        return self.driver.title
    
    def wait_for_element(self, locator, timeout=10):
        """Waits for a specific element to be visible on the page."""
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
    
    def wait_for_elements(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located(locator))

    def wait_for_button(self, locator, timeout=10):
        """Waits for a specific button to be clickable on the page."""
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
    
    def wait_for_clickable(self, locator, timeout=10):
        """Waits for a specific element to be clickable on the page."""
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
    
    def wait_for_invisibility(self, locator, timeout=10):
        """Waits for a specific element to become invisible on the page."""
        return WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )