import pytest
import time
import os
import threading
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

    # Enable headless mode in CI environments
    if os.getenv('CI') or os.getenv('GITHUB_ACTIONS') or os.getenv('GITLAB_CI'):
        chrome_options.add_argument("--headless")
        # Set binary location for CI (Ubuntu)
        chrome_options.binary_location = "/usr/bin/chromium-browser"

    chromedriver_path = ChromeDriverManager().install()
    if 'THIRD_PARTY_NOTICES' in chromedriver_path:
        chromedriver_path = chromedriver_path.replace('THIRD_PARTY_NOTICES.chromedriver', 'chromedriver.exe')
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    yield driver

    driver.quit()


@pytest.fixture(scope="session", autouse=True)
def start_flask_app():
    """Start the Flask app in a background thread for testing (only if not in CI)"""
    if os.getenv('CI') or os.getenv('GITHUB_ACTIONS') or os.getenv('GITLAB_CI'):
        yield  # In CI, app is started externally
        return

    from app import app

    def run_app():
        app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False, threaded=True)

    thread = threading.Thread(target=run_app, daemon=True)
    thread.start()
    time.sleep(3)  # Wait for the app to start

    yield  # Tests run here

    # No need to stop the app, daemon thread will be killed when tests end


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