import os
import time
import io
from selenium.webdriver.common.by import By
from PIL import Image


def take_full_page_screenshot(driver, test_name, filename=None):
    """
    Take a full page screenshot using Chrome DevTools for true full page capture.
    Args:
        driver: Selenium webdriver instance
        test_name: Name of the test case (e.g., 'test_file_upload')
        filename: Optional custom filename, defaults to test_name + '.png'
    """
    try:
        screenshots_dir = 'screenshots'
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)

        if filename is None:
            filename = f"{test_name}.png"

        screenshot_path = os.path.join(screenshots_dir, filename)

        # Try Chrome DevTools full page screenshot first (no window resizing needed)
        try:
            screenshot_data = driver.execute_cdp_cmd('Page.captureScreenshot', {
                'format': 'png',
                'captureBeyondViewport': True,  # This captures the full page
                'fromSurface': True
            })

            # Decode base64 and save
            import base64
            screenshot_bytes = base64.b64decode(screenshot_data['data'])

            with open(screenshot_path, 'wb') as f:
                f.write(screenshot_bytes)

            # Get image dimensions for logging
            img = Image.open(io.BytesIO(screenshot_bytes))
            width, height = img.size
            print(f'Chrome DevTools full page screenshot saved: {screenshot_path} (Size: {width}x{height})')

        except Exception as cdp_error:
            print(f'Chrome DevTools screenshot failed: {cdp_error}, falling back to manual method')

            # Fallback: maximize window temporarily for full page capture
            original_size = driver.get_window_size()
            driver.maximize_window()
            time.sleep(1)

            try:
                _take_full_page_screenshot_manual(driver, screenshot_path, test_name)
            finally:
                # Restore original window size
                driver.set_window_size(original_size['width'], original_size['height'])

    except Exception as e:
        print(f'Failed to take full page screenshot {filename}: {str(e)}')
        # Fallback to regular screenshot
        try:
            if filename is None:
                filename = f"{test_name}.png"
            screenshot_path = os.path.join(screenshots_dir, filename)
            driver.save_screenshot(screenshot_path)
            print(f'Regular screenshot saved as fallback: {screenshot_path}')
        except Exception as e2:
            print(f'Failed to take screenshot {filename}: {str(e2)}')


def _take_full_page_screenshot_manual(driver, screenshot_path, test_name):
    """Manual full page screenshot using scrolling and stitching"""

    # Get total page dimensions
    total_width = driver.execute_script("return Math.max(document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth);")
    total_height = driver.execute_script("return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")

    # Get viewport dimensions
    viewport_width = driver.execute_script("return window.innerWidth;")
    viewport_height = driver.execute_script("return window.innerHeight;")

    print(f'Manual method - Viewport: {viewport_width}x{viewport_height}, Total page: {total_width}x{total_height}')

    # If page fits in viewport, just take a regular screenshot
    if total_width <= viewport_width and total_height <= viewport_height:
        driver.save_screenshot(screenshot_path)
        print(f'Single screenshot saved (page fits in viewport): {screenshot_path}')
        return

    # Scroll to top first
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(0.5)

    screenshots = []
    current_scroll = 0

    # Handle vertical scrolling only
    while current_scroll < total_height:
        # Take screenshot of current viewport
        screenshot = driver.get_screenshot_as_png()
        screenshots.append((current_scroll, screenshot))

        # Scroll down
        scroll_amount = viewport_height - 100  # 100px overlap
        current_scroll += scroll_amount
        driver.execute_script(f"window.scrollTo(0, {current_scroll});")
        time.sleep(0.5)

        # Check if we've reached the bottom
        actual_scroll = driver.execute_script("return window.pageYOffset;")
        if actual_scroll == current_scroll - scroll_amount:
            break

    # Combine screenshots
    if screenshots:
        # Create combined image
        combined_image = Image.new('RGB', (viewport_width, total_height), (255, 255, 255))

        for scroll_pos, screenshot_data in screenshots:
            screenshot_img = Image.open(io.BytesIO(screenshot_data))
            y_position = min(scroll_pos, total_height - viewport_height)
            crop_height = min(viewport_height, total_height - y_position)

            if crop_height < viewport_height:
                screenshot_img = screenshot_img.crop((0, 0, viewport_width, crop_height))

            combined_image.paste(screenshot_img, (0, y_position))

        combined_image.save(screenshot_path)
        print(f'Manual full page screenshot saved: {screenshot_path} (Size: {viewport_width}x{total_height})')
    else:
        driver.save_screenshot(screenshot_path)
        print(f'Fallback screenshot saved: {screenshot_path}')


def get_test_file_path(filename):
    return os.path.join('test_data', filename)
