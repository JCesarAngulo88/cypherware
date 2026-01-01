import pytest
import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Create a logger instance for this module
logger = logging.getLogger(__name__)

@pytest.fixture(scope="session", autouse=True)
def initialize_database():
    """
    Ensures that the database tables are created before any tests run.
    This is essential for the Cypherware app in CI/CD environments.
    """
    try:
        from server import app, db
        with app.app_context():
            logger.info("Initializing Cypherware database tables...")
            db.create_all()
    except ImportError as e:
        logger.error(f"Could not import server or db: {e}")
    yield

@pytest.fixture(scope="class")
def driver(request):
    """
    Initializes the WebDriver. 
    Supports local (headed) and CI (headless) execution based on environment variables.
    """
    chrome_options = Options()
    
    # Check if we are running in GitHub Actions (CI)
    is_ci = os.getenv("CI_ENVIRONMENT") == "true" or os.getenv("GITHUB_ACTIONS") == "true"

    if is_ci:
        logger.info("Running in CI environment: Enabling headless mode.")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        # System path handles ChromeDriver in GitHub runners
        service = Service()
    else:
        logger.info("Running in local environment.")
        chrome_options.add_argument("--start-maximized")
        # Try to import local path from config.py
        try:
            from config import DRIVER_PATH
            service = Service(DRIVER_PATH)
        except ImportError:
            logger.warning("config.py not found. Using default system Service.")
            service = Service()

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

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    logger.info("Logger has been configured.")

@pytest.fixture
def base_url():
    """Returns the URL of the running Flask server."""
    return os.getenv("BASE_URL", "http://127.0.0.1:5000")