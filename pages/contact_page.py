from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ContactPage(BasePage):
    HEADER = (By.TAG_NAME, "h1")
    HOME_LINK: tuple[str, str] = (By.LINK_TEXT, "Home")
    def open_contact(self):
        self.open("/contact")

    def get_contact_header1_text(self):
        return self.get_text(self.HEADER)
    
    def return_home_page(self):
        self.click(self.HOME_LINK)
