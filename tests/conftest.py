import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="session")
def browser():
    """Fixture to provide a Chrome browser instance for testing"""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-images")  # Speed up tests
    chrome_options.add_argument("--disable-javascript")  # Disable JS for faster loading
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Uncomment the line below to run tests in headless mode (no visible browser)
    chrome_options.add_argument("--headless")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    yield driver

    driver.quit()


@pytest.fixture
def login_credentials():
    """Fixture providing test login credentials"""
    return {
        'username': 'hadjhassinejawher',
        'password': 'ChangeIt'
    }


@pytest.fixture
def slow_actions():
    """Fixture providing timing configurations for test actions"""
    return {
        'page_load': 2,  # seconds to wait after page loads
        'input': 0.5,    # seconds to wait after input
        'click': 1,      # seconds to wait after clicks
        'action': 1      # seconds to wait after major actions
    }