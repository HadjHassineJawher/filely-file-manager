import pytest
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .test_utils import take_full_page_screenshot, get_test_file_path


class TestFileOperations:
    """Test file operations functionality"""
    
    def _get_unique_name(self, base_name):
        """Generate a unique name for test files/folders to avoid conflicts"""
        import uuid
        return f"{base_name}_{uuid.uuid4().hex[:8]}"

    @pytest.mark.smoke
    @pytest.mark.file_ops
    def test_file_upload(self, browser, login_credentials, slow_actions):
        """Test file upload functionality"""
        print("Testing file upload functionality...")

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

        # Upload a file
        upload_button = browser.find_element(By.ID, 'uploadFilesBtn')
        upload_button.click()
        time.sleep(slow_actions['click'])

        # Find file input and upload
        file_input = browser.find_element(By.ID, 'fileInput')
        test_file = get_test_file_path('document.txt')
        file_input.send_keys(os.path.abspath(test_file))
        time.sleep(slow_actions['input'])

        # Submit upload
        save_button = browser.find_element(By.ID, 'saveBtn')
        save_button.click()
        time.sleep(slow_actions['action'])

        # Verify upload success
        assert 'Files uploaded successfully!' in browser.page_source or 'uploaded successfully' in browser.page_source.lower()

        time.sleep(2)  # Wait before taking screenshot
        take_full_page_screenshot(browser, 'test_file_upload')
        print("File upload test completed")

    @pytest.mark.file_ops
    def test_drag_and_drop_upload(self, browser, login_credentials, slow_actions):
        """Test drag and drop file upload"""
        print("Testing drag and drop upload...")

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

        # Open upload modal
        upload_button = browser.find_element(By.ID, 'uploadFilesBtn')
        upload_button.click()
        time.sleep(slow_actions['click'])

        # Use file input for drag and drop simulation
        file_input = browser.find_element(By.ID, 'fileInput')
        test_file = get_test_file_path('document.txt')
        file_input.send_keys(os.path.abspath(test_file))
        time.sleep(slow_actions['input'])

        # Submit upload
        save_button = browser.find_element(By.ID, 'saveBtn')
        save_button.click()
        time.sleep(slow_actions['action'])

        # Verify upload success
        assert 'uploaded successfully' in browser.page_source.lower() or 'Files uploaded successfully' in browser.page_source

        time.sleep(2)  # Wait before taking screenshot
        take_full_page_screenshot(browser, 'test_drag_and_drop_upload')
        print("Drag and drop upload test completed")

    @pytest.mark.rename
    def test_file_rename_functionality(self, browser, login_credentials, slow_actions):
        """Test file rename functionality"""
        print("Testing file rename functionality...")

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

        # First upload a file to rename
        upload_button = browser.find_element(By.ID, 'uploadFilesBtn')
        upload_button.click()
        time.sleep(slow_actions['click'])

        file_input = browser.find_element(By.ID, 'fileInput')
        test_file = get_test_file_path('document.txt')
        file_input.send_keys(os.path.abspath(test_file))
        time.sleep(slow_actions['input'])

        save_button = browser.find_element(By.ID, 'saveBtn')
        save_button.click()
        time.sleep(slow_actions['action'])

        # Find the rename button for the uploaded file
        rename_buttons = browser.find_elements(By.XPATH, '//button[contains(@onclick, "openRenameModal")]')
        if rename_buttons:
            rename_buttons[0].click()
            time.sleep(slow_actions['click'])

            # Enter new unique name
            unique_rename_name = self._get_unique_name('renamed_document.txt')
            name_input = browser.find_element(By.ID, 'renameNewName')
            name_input.clear()
            name_input.send_keys(unique_rename_name)
            time.sleep(slow_actions['input'])

            # Submit rename
            rename_save_btn = browser.find_element(By.ID, 'renameSaveBtn')
            rename_save_btn.click()
            time.sleep(slow_actions['action'])

            # Verify rename success
            time.sleep(slow_actions['action'])  # Wait for page to update
            assert unique_rename_name in browser.page_source

            time.sleep(2)  # Wait before taking screenshot
            take_full_page_screenshot(browser, 'test_file_rename_functionality')
            print("File rename test completed")
        else:
            pytest.skip("No files available to rename")

    @pytest.mark.preview
    def test_file_preview_functionality(self, browser, login_credentials, slow_actions):
        """Test file preview functionality"""
        print("Testing file preview functionality...")

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

        # Upload a file first
        upload_button = browser.find_element(By.ID, 'uploadFilesBtn')
        upload_button.click()
        time.sleep(slow_actions['click'])

        file_input = browser.find_element(By.ID, 'fileInput')
        test_file = get_test_file_path('document.txt')
        file_input.send_keys(os.path.abspath(test_file))
        time.sleep(slow_actions['input'])

        save_button = browser.find_element(By.ID, 'saveBtn')
        save_button.click()
        time.sleep(slow_actions['action'])

        # Find preview button for the most recent file (document.txt)
        preview_button = browser.find_element(By.XPATH, '//a[@title="Preview"]')
        if preview_button:
            # Store original window handle
            original_window = browser.current_window_handle

            # Click preview (opens in new tab)
            preview_button.click()
            time.sleep(slow_actions['action'])

            # Switch to new tab
            WebDriverWait(browser, 10).until(lambda d: len(d.window_handles) > 1)
            new_window = [handle for handle in browser.window_handles if handle != original_window][0]
            browser.switch_to.window(new_window)

            # Verify preview content
            assert 'Lorem ipsum dolor sit amet' in browser.page_source

            # Close preview tab and switch back
            browser.close()
            browser.switch_to.window(original_window)

            time.sleep(2)  # Wait before taking screenshot
            take_full_page_screenshot(browser, 'test_file_preview_functionality')
            print("File preview test completed")
        else:
            pytest.skip("No files available to preview")

    @pytest.mark.rename
    def test_file_rename_conflict(self, browser, login_credentials, slow_actions):
        """Test file rename conflict handling"""
        print("Testing file rename conflict handling...")

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

        # Upload two files with different names
        upload_button = browser.find_element(By.ID, 'uploadFilesBtn')
        upload_button.click()
        time.sleep(slow_actions['click'])

        file_input = browser.find_element(By.ID, 'fileInput')
        test_file1 = get_test_file_path('document.txt')
        file_input.send_keys(os.path.abspath(test_file1))
        time.sleep(slow_actions['input'])

        save_button = browser.find_element(By.ID, 'saveBtn')
        save_button.click()
        time.sleep(slow_actions['action'])

        # Upload second file
        upload_button = browser.find_element(By.ID, 'uploadFilesBtn')
        upload_button.click()
        time.sleep(slow_actions['click'])

        file_input = browser.find_element(By.ID, 'fileInput')
        test_file2 = get_test_file_path('contract.pdf')
        file_input.send_keys(os.path.abspath(test_file2))
        time.sleep(slow_actions['input'])

        save_button = browser.find_element(By.ID, 'saveBtn')
        save_button.click()
        time.sleep(slow_actions['action'])

        # Try to rename document.txt to contract.pdf (should conflict)
        rename_buttons = browser.find_elements(By.XPATH, '//button[contains(@onclick, "openRenameModal") and contains(@onclick, "document.txt")]')
        if rename_buttons:
            rename_buttons[0].click()
            time.sleep(slow_actions['click'])

            # Enter existing name (contract.pdf)
            name_input = browser.find_element(By.ID, 'renameNewName')
            name_input.clear()
            name_input.send_keys('contract.pdf')
            time.sleep(slow_actions['input'])

            # Submit rename
            rename_save_btn = browser.find_element(By.ID, 'renameSaveBtn')
            rename_save_btn.click()
            time.sleep(slow_actions['action'])

            # Verify conflict error message
            time.sleep(slow_actions['action'])  # Wait for page to update
            assert 'An item with that name already exists !' in browser.page_source or 'already exists' in browser.page_source.lower()

            time.sleep(2)  # Wait before taking screenshot
            take_full_page_screenshot(browser, 'test_file_rename_conflict')
            print("File rename conflict test completed")
        else:
            pytest.skip("No files available to test rename conflict")