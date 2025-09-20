from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class HomePage(BasePage):
    HEADER1: tuple[str, str] = (By.TAG_NAME, "h1")
    HEADER2: tuple[str, str] = (By.TAG_NAME, "h2")
    HEADER3: tuple[str, str] = (By.TAG_NAME, "h3")
    CONTACT_LINK: tuple[str, str] = (By.LINK_TEXT, "Contact")

    def open_home(self):
        self.open("/")

    def get_home_title(self):
        return self.get_title()

    def get_header1_text(self):
        return self.get_text(self.HEADER1, "Follow your dreams")
    
    def get_header2_text(self):
        return self.get_text(self.HEADER2, "Software for the future")
    
    def get_header3_text(self):
        return self.get_text(self.HEADER3, "If you can think it, we can build it")

    def go_to_contact(self):
        self.click(self.CONTACT_LINK)
