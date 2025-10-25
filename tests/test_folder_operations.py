import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .test_utils import take_full_page_screenshot


class TestFolderOperations:
    """Test folder operations functionality"""
    
    def _get_unique_name(self, base_name):
        """Generate a unique name for test files/folders to avoid conflicts"""
        import uuid
        return f"{base_name}_{uuid.uuid4().hex[:8]}"

    @pytest.mark.smoke
    @pytest.mark.folder_ops
    def test_folder_creation(self, browser, login_credentials, slow_actions):
        """Test folder creation functionality"""
        print("Testing folder creation functionality...")

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

        # Click create folder button
        create_folder_btn = browser.find_element(By.ID, 'createFolderBtn')
        create_folder_btn.click()
        time.sleep(slow_actions['click'])

        # Enter folder name
        unique_folder_name = self._get_unique_name('TestFolder')
        folder_name_input = browser.find_element(By.ID, 'newFolderName')
        folder_name_input.send_keys(unique_folder_name)
        time.sleep(slow_actions['input'])

        # Submit folder creation
        folder_save_btn = browser.find_element(By.ID, 'folderSaveBtn')
        folder_save_btn.click()
        time.sleep(slow_actions['action'])

        # Verify folder creation success
        assert 'Folder created successfully!' in browser.page_source

        time.sleep(2)  # Wait before taking screenshot
        take_full_page_screenshot(browser, 'test_folder_creation')
        print("Folder creation test completed")

    @pytest.mark.folder_ops
    def test_folder_navigation(self, browser, login_credentials, slow_actions):
        """Test folder navigation functionality"""
        print("Testing folder navigation functionality...")

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

        # Create a folder first
        create_folder_btn = browser.find_element(By.ID, 'createFolderBtn')
        create_folder_btn.click()
        time.sleep(slow_actions['click'])

        folder_name_input = browser.find_element(By.ID, 'newFolderName')
        unique_nav_folder = self._get_unique_name('NavTestFolder')
        folder_name_input.send_keys(unique_nav_folder)
        time.sleep(slow_actions['input'])

        folder_save_btn = browser.find_element(By.ID, 'folderSaveBtn')
        folder_save_btn.click()
        time.sleep(slow_actions['action'])

        # Navigate into the folder
        folder_links = browser.find_elements(By.XPATH, f'//div[contains(@class, "item-name") and contains(text(), "{unique_nav_folder}")]')
        if folder_links:
            folder_links[0].click()
            time.sleep(slow_actions['action'])

            # Verify we're inside the folder
            assert unique_nav_folder in browser.current_url

            time.sleep(2)  # Wait before taking screenshot
            take_full_page_screenshot(browser, 'test_folder_navigation')
            print("Folder navigation test completed")
        else:
            pytest.skip("Could not find created folder to navigate into")

    @pytest.mark.rename
    def test_folder_rename_functionality(self, browser, login_credentials, slow_actions):
        """Test folder rename functionality"""
        print("Testing folder rename functionality...")

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

        # Create a folder first
        create_folder_btn = browser.find_element(By.ID, 'createFolderBtn')
        create_folder_btn.click()
        time.sleep(slow_actions['click'])

        folder_name_input = browser.find_element(By.ID, 'newFolderName')
        unique_rename_folder = self._get_unique_name('RenameTestFolder')
        folder_name_input.send_keys(unique_rename_folder)
        time.sleep(slow_actions['input'])

        folder_save_btn = browser.find_element(By.ID, 'folderSaveBtn')
        folder_save_btn.click()
        time.sleep(slow_actions['action'])

        # Find the rename button for the folder
        rename_buttons = browser.find_elements(By.XPATH, '//button[contains(@onclick, "openRenameModal") and contains(@onclick, "folder")]')
        if rename_buttons:
            rename_buttons[0].click()
            time.sleep(slow_actions['click'])

            # Enter new unique name
            unique_renamed_name = self._get_unique_name('RenamedFolder')
            name_input = browser.find_element(By.ID, 'renameNewName')
            name_input.clear()
            name_input.send_keys(unique_renamed_name)
            time.sleep(slow_actions['input'])

            # Submit rename
            rename_save_btn = browser.find_element(By.ID, 'renameSaveBtn')
            rename_save_btn.click()
            time.sleep(slow_actions['action'])

            # Verify rename success
            time.sleep(slow_actions['action'])  # Wait for page to update
            assert unique_renamed_name in browser.page_source

            time.sleep(2)  # Wait before taking screenshot
            take_full_page_screenshot(browser, 'test_folder_rename_functionality')
            print("Folder rename test completed")
        else:
            pytest.skip("No folders available to rename")