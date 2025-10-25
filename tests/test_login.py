import pytest
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .test_utils import take_full_page_screenshot

class TestLogin:
    """Test login and logout functionality"""

    @pytest.mark.smoke
    @pytest.mark.login
    def test_successful_login(self, browser, login_credentials, slow_actions):
        """Test successful login with valid credentials"""
        print("Testing login functionality...")

        browser.get('http://localhost:5000/login')
        time.sleep(slow_actions['page_load'])  # Slow down for visibility

        # Fill login form with delays
        username_input = browser.find_element(By.NAME, 'username')
        password_input = browser.find_element(By.NAME, 'password')
        login_button = browser.find_element(By.XPATH, '//button[@type="submit"]')

        username_input.send_keys(login_credentials['username'])
        time.sleep(slow_actions['input'])

        password_input.send_keys(login_credentials['password'])
        time.sleep(slow_actions['input'])

        login_button.click()
        time.sleep(slow_actions['click'])

        # Verify redirect to files page
        WebDriverWait(browser, 10).until(EC.url_contains('/files'))
        time.sleep(slow_actions['page_load'])

        assert 'Filely' in browser.page_source

        # Take a full page screenshot (handles scrolling automatically)
        time.sleep(2)  # Wait before taking screenshot
        take_full_page_screenshot(browser, 'test_successful_login')

        print("Login successful")

    @pytest.mark.logout
    def test_logout_functionality(self, browser, login_credentials, slow_actions):
        """Test logout functionality"""
        print("Testing logout functionality...")

        # Login first with delays
        browser.get('http://localhost:5000/login')
        time.sleep(slow_actions['page_load'])

        browser.find_element(By.NAME, 'username').send_keys(login_credentials['username'])
        time.sleep(slow_actions['input'])

        browser.find_element(By.NAME, 'password').send_keys(login_credentials['password'])
        time.sleep(slow_actions['input'])

        browser.find_element(By.XPATH, '//button[@type="submit"]').click()
        time.sleep(slow_actions['click'])

        WebDriverWait(browser, 10).until(EC.url_contains('/files'))
        time.sleep(slow_actions['page_load'])

        # Verify we're logged in
        assert 'Logout' in browser.page_source or 'Filely' in browser.page_source

        # Find and click logout button/link
        logout_links = browser.find_elements(By.XPATH, '//a[@title="Logout"]')
        if logout_links:
            logout_links[0].click()
            time.sleep(slow_actions['click'])

        # Verify redirect to login page
        WebDriverWait(browser, 10).until(EC.url_contains('/login'))
        time.sleep(slow_actions['page_load'])

        assert 'login' in browser.current_url.lower()

        print("Logout successful")