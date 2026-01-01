

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def create_driver():
    service = Service("/Users/jcesar/projects/cypherware-webapp/myenv/chromedriver")
    options = webdriver.ChromeOptions()
    return webdriver.Chrome(service=service, options=options)
