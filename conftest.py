import pytest
import logging
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Create a logger instance for this module
logger = logging.getLogger(__name__)

# --- Path Configuration ---
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


def pytest_configure(config):
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

@pytest.fixture(scope="session", autouse=True)
def initialize_database():
    """
    Ensures that the database tables are created before any tests run.
    This is essential for the Cypherware app in CI/CD environments.
    """
    try:
        from server import app, db
        # Debugging: Log the connection URI being used (masking sensitive parts)
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', 'NOT SET')
        logger.info(
            f"Connecting to database for initialization: {db_uri.split('@')[-1] if '@' in db_uri else 'Local/No Pass'}")

        with app.app_context():
            logger.info("Initializing Cypherware database tables...")
            db.create_all()
            logger.info("Database tables initialized successfully.")
    except ImportError as e:
        logger.error(f"Could not import server or db: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during database initialization: {e}")
    yield

@pytest.fixture(scope="function")
def driver(request):
    """
    Initializes the WebDriver. 
    Supports local (headed) and CI (headless) execution based on environment variables.
    """
    chrome_options = Options()
    
    # Check if we are running in GitHub Actions (CI)
    is_ci = os.getenv("CI_ENVIRONMENT") == "true" or os.getenv("GITHUB_ACTIONS") == "true"

    if is_ci:
        logger.info("CI detected: Enabling Headless Chrome.")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        service = Service()
    else:
        logger.info("Local environment: Enabling Headed Chrome.")
        chrome_options.add_argument("--start-maximized")
        try:
            from config import DRIVER_PATH
            service = Service(DRIVER_PATH)
        except ImportError:
            logger.warning("config.py not found. Using default system Service.")
            service = Service()

    driver = webdriver.Chrome(service=service, options=chrome_options)

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
    return os.getenv("BASE_URL", "http://127.0.0.1:5001")