import pytest
import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Create a logger instance for this module
logger = logging.getLogger(__name__)

@pytest.fixture(scope="class")
def driver(request):
    """
    Initializes the WebDriver. 
    Supports local (headed) and CI (headless) execution.
    """
    chrome_options = Options()
    
    # Check if we are running in GitHub Actions (CI)
    is_ci = os.getenv("CI_ENVIRONMENT") == "true"

    if is_ci:
        logger.info("Running in CI environment: Enabling headless mode.")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        # In CI, we don't pass a specific path, Selenium finds it in the system path
        service = Service()
    else:
        logger.info("Running in local environment.")
        chrome_options.add_argument("--start-maximized")
        # LOCAL PATH: Keep your local path here for your manual runs
        local_driver_path = "/Users/jcesar/projects/cypherware-webapp/myenv/chromedriver"
        service = Service(local_driver_path)

    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Attach driver to the class so tests can access self.driver
    if request.cls is not None:
        request.cls.driver = driver
        
    yield driver
    
    logger.info("Closing WebDriver.")
    driver.quit()

@pytest.fixture(scope="session", autouse=True)
def setup_logger():
    """
    Configures the root logger for the entire test run.
    """
    log_file_path = os.path.join(os.path.dirname(__file__), "app_test.log")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # File handler
    file_handler = logging.FileHandler(log_file_path, mode='w')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # Silence noisy third-party libraries
    logging.getLogger("selenium.webdriver.remote.remote_connection").setLevel(logging.WARNING)
    logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    logger.info("Logger has been configured for the test session.")