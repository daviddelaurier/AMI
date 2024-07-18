import pyautogui
import os
from dotenv import load_dotenv

load_dotenv()

def capture_browser():
    browser_screenshots_dir = os.getenv("BROWSER_SCREENSHOTS_DIR")
    if not browser_screenshots_dir:
        raise ValueError("BROWSER_SCREENSHOTS_DIR not set in .env file")
    
    os.makedirs(browser_screenshots_dir, exist_ok=True)
    screenshot_path = os.path.join(browser_screenshots_dir, "browser_screenshot.png")
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)
    return screenshot_path

def get_browser_context():
    try:
        screenshot_path = capture_browser()
        return f"Browser screenshot saved at: {screenshot_path}"
    except Exception as e:
        return f"Error capturing browser screenshot: {str(e)}"

if __name__ == "__main__":
    print(get_browser_context())