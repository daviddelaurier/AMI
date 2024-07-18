# TODO: Add a function to capture a specific area of the screen and save it to a file
# TODO: Upscale the image to the max resolution (?) and filesize of 25MB per file
# TODO: The image needs to be converted to base64 to be sent to the Anthropic API.

import pyautogui
import os
from dotenv import load_dotenv

load_dotenv()

def capture_desktop():
    screenshots_dir = os.getenv("SCREENSHOTS_DIR")
    if not screenshots_dir:
        raise ValueError("SCREENSHOTS_DIR not set in .env file")
    
    os.makedirs(screenshots_dir, exist_ok=True)
    screenshot_path = os.path.join(screenshots_dir, "desktop_screenshot.png")
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)
    return screenshot_path

def get_desktop_context():
    try:
        screenshot_path = capture_desktop()
        return f"Desktop screenshot saved at: {screenshot_path}"
    except Exception as e:
        return f"Error capturing desktop screenshot: {str(e)}"

if __name__ == "__main__":
    print(get_desktop_context())