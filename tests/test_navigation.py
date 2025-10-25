import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .test_utils import take_full_page_screenshot


class TestNavigation:
    """Test navigation features"""
    
    def _get_unique_name(self, base_name):
        """Generate a unique name for test files/folders to avoid conflicts"""
        import uuid
        return f"{base_name}_{uuid.uuid4().hex[:8]}"

    @pytest.mark.navigation
    def test_breadcrumb_navigation(self, browser, login_credentials, slow_actions):
        """Test breadcrumb navigation functionality"""
        print("Testing breadcrumb navigation...")

        # Login first
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

        # Create a folder
        create_folder_btn = browser.find_element(By.ID, 'createFolderBtn')
        create_folder_btn.click()
        time.sleep(slow_actions['click'])

        folder_name = self._get_unique_name('BreadcrumbTest')
        folder_name_input = browser.find_element(By.ID, 'newFolderName')
        folder_name_input.send_keys(folder_name)
        time.sleep(slow_actions['input'])

        folder_save_btn = browser.find_element(By.ID, 'folderSaveBtn')
        folder_save_btn.click()
        time.sleep(slow_actions['action'])

        # Navigate into the folder
        folder_link = browser.find_element(By.XPATH, f'//div[contains(@onclick, "navigateToFolder(\'{folder_name}\')")]')
        folder_link.click()
        time.sleep(slow_actions['action'])

        # Verify breadcrumb is present
        breadcrumbs = browser.find_elements(By.CLASS_NAME, 'breadcrumb-item')
        assert len(breadcrumbs) > 0

        # Click on breadcrumb to go back
        home_breadcrumb = browser.find_element(By.XPATH, '//a[contains(@class, "breadcrumb-link") and contains(text(), "Home")]')
        home_breadcrumb.click()
        time.sleep(slow_actions['action'])

        # Verify we're back at root
        assert '/files' in browser.current_url and 'folder_path' not in browser.current_url

        time.sleep(2)  # Wait before taking screenshot
        take_full_page_screenshot(browser, 'test_breadcrumb_navigation')
        print("Breadcrumb navigation test completed")

    @pytest.mark.navigation
    def test_ui_elements_visibility(self, browser, login_credentials, slow_actions):
        """Test that all UI elements are visible and functional"""
        print("Testing UI elements visibility...")

        # Login first
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

        # Check main UI elements are present
        assert browser.find_element(By.ID, 'createFolderBtn').is_displayed()
        assert browser.find_element(By.ID, 'uploadFilesBtn').is_displayed()

        # Check navigation elements
        logout_link = browser.find_elements(By.XPATH, '//a[@title="Logout"]')
        assert len(logout_link) > 0

        # Check table headers
        headers = browser.find_elements(By.XPATH, '//th')
        assert len(headers) >= 4  # Name, Type, Items, Size, Actions

        time.sleep(2)  # Wait before taking screenshot
        take_full_page_screenshot(browser, 'test_ui_elements_visibility')
        print("UI elements visibility test completed")

    @pytest.mark.navigation
    def test_complete_navigation_workflow(self, browser, login_credentials, slow_actions):
        """Test complete navigation workflow with nested folders"""
        print("Testing complete navigation workflow...")

        # Login first
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

        # Create parent folder
        create_folder_btn = browser.find_element(By.ID, 'createFolderBtn')
        create_folder_btn.click()
        time.sleep(slow_actions['click'])

        parent_folder_name = self._get_unique_name('ParentFolder')
        folder_name_input = browser.find_element(By.ID, 'newFolderName')
        folder_name_input.send_keys(parent_folder_name)
        time.sleep(slow_actions['input'])

        folder_save_btn = browser.find_element(By.ID, 'folderSaveBtn')
        folder_save_btn.click()
        time.sleep(slow_actions['action'])

        # Navigate into parent folder
        parent_folder = browser.find_element(By.XPATH, f'//div[contains(@onclick, "navigateToFolder(\'{parent_folder_name}\')")]')
        parent_folder.click()
        time.sleep(slow_actions['action'])

        # Create child folder inside parent
        create_folder_btn = browser.find_element(By.ID, 'createFolderBtn')
        create_folder_btn.click()
        time.sleep(slow_actions['click'])

        child_folder_name = self._get_unique_name('ChildFolder')
        folder_name_input = browser.find_element(By.ID, 'newFolderName')
        folder_name_input.send_keys(child_folder_name)
        time.sleep(slow_actions['input'])

        folder_save_btn = browser.find_element(By.ID, 'folderSaveBtn')
        folder_save_btn.click()
        time.sleep(slow_actions['action'])

        # Navigate into child folder
        child_folder = browser.find_element(By.XPATH, f'//div[contains(@onclick, "navigateToFolder(\'{parent_folder_name}/{child_folder_name}\')")]')
        child_folder.click()
        time.sleep(slow_actions['action'])

        # Verify nested navigation with breadcrumbs
        breadcrumbs = browser.find_elements(By.CLASS_NAME, 'breadcrumb-item')
        assert len(breadcrumbs) >= 2  # Should have Home > ParentFolder > ChildFolder

        # Navigate back using breadcrumbs
        parent_breadcrumb = browser.find_element(By.XPATH, f'//a[contains(@class, "breadcrumb-link") and contains(text(), "{parent_folder_name}")]')
        parent_breadcrumb.click()
        time.sleep(slow_actions['action'])

        # Verify we're back in parent folder
        assert parent_folder_name in browser.current_url
        assert child_folder_name not in browser.current_url

        time.sleep(2)  # Wait before taking screenshot
        take_full_page_screenshot(browser, 'test_complete_navigation_workflow')
        print("Complete navigation workflow test completed")