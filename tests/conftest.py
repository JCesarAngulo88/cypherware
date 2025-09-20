import pytest
import logging
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="class")
def driver(request):
    options = webdriver.ChromeOptions()
    service = Service("/Users/jcesar/projects/cypherware-webapp/myenv/chromedriver")
    
    #options.add_argument("--start-maximized")
    #driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver = webdriver.Chrome(service=service, options=options)
    request.cls.driver = driver
    yield driver
    driver.quit()

# Create a logger instance for this module
logger = logging.getLogger(__name__)

# This fixture will set up the logger for the entire test run.
@pytest.fixture(scope="session", autouse=True)
def setup_logger():
    """
    Configures the root logger to output to a file and the console.
    This fixture will be automatically used for all tests.
    """
    print("Get into setup logger function fixture")
    # Define the log file path
    log_file_path = os.path.join(os.path.dirname(__file__), "urban_routes_test.log")

    # Set the format for the log messages
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # File handler to write logs to a file
    file_handler = logging.FileHandler(log_file_path, mode='w')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    # Console handler to print logs to the terminal
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    # Change this line from logging.DEBUG to logging.INFO
    console_handler.setLevel(logging.INFO)

    # --- Add these lines to specifically silence third-party loggers ---
    logging.getLogger("selenium.webdriver.remote.remote_connection").setLevel(logging.WARNING)
    logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)

    # You can also set these to logging.ERROR if you don't want to see any warnings
    # from these modules, but WARNING is a good compromise.

    # ------------------------------------------------------------------

    # Get the root logger and add the handlers
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # Log a message to confirm the logger is set up
    logger.info("Logger has been configured.")