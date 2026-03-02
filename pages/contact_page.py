from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ContactPage(BasePage):
    HEADER_PROJECT_INQUIRY: tuple = (By.CSS_SELECTOR, "h1.contact-title")
    INPUT_NAME_CONTACT: tuple = (By.ID, "user_name")
    INPUT_EMAIL_ADDRESS_CONTACT: tuple = (By.ID, "email_address")
    INPUT_PHONE_NUMBER_CONTACT: tuple = (By.ID, "phone_number")
    INPUT_SERVICE_TYPE_CONTACT: tuple = (By.ID, "service_type")
    INPUT_PROJECT_NAME_CONTACT: tuple = (By.ID, "project_name")
    INPUT_PROJECT_DESCRIPTION_CONTACT: tuple = (By.ID, "project_description")
    BUTTON_EXECUTE_TRANSMISSION: tuple = (By.XPATH, "//button[@class='submit-button' or text()='EXECUTE TRANSMISSION']")

    HEADER = (By.TAG_NAME, "h1")
    HOME_LINK: tuple[str, str] = (By.LINK_TEXT, "Home")
    def open_contact(self):
        self.open("/contact")

    def get_contact_header1_text(self):
        return self.get_text(self.HEADER)
    
    def return_home_page(self):
        self.click(self.HOME_LINK)

    def get_header_text(self):
        return self.driver.find_element(*self.HEADER_PROJECT_INQUIRY).text

    def write_input_name(self, full_name):
        """"""
        self.type(self.INPUT_NAME_CONTACT, full_name)

    def get_input_full_name(self) -> str:
        """Get input value from locator"""
        return self.get_input_value(self.INPUT_NAME_CONTACT)

    def write_input_email(self, full_email):
        """Write input value to locator"""
        self.type(self.INPUT_EMAIL_ADDRESS_CONTACT, full_email)


