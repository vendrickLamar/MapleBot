import os
import time
import cv2
import numpy as np
import pyautogui
import keyboard
import pygetwindow as gw
from datetime import datetime
from PIL import ImageGrab

# Create output folders
os.makedirs("player_training/positive", exist_ok=True)
os.makedirs("player_training/negative", exist_ok=True)
os.makedirs("captures", exist_ok=True)

def get_maplestory_window():
    try:
        window = gw.getWindowsWithTitle("MapleStory")[0]
        if window.isMinimized:
            print("MapleStory window is minimized. Please restore it.")
            return None
        return window
    except IndexError:
        print("Could not find a window titled 'MapleStory'. Is the game running?")
        return None

def take_window_screenshot(window, label, auto_mode=False):
    # Get window region (left, top, width, height)
    left, top, width, height = window.left, window.top, window.width, window.height

    # Use PIL to grab the image from the region
    bbox = (left, top, left + width, top + height)
    screenshot = ImageGrab.grab(bbox)

    # Convert to OpenCV format
    image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Save with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')

    if auto_mode:
        # Save to captures folder when in auto mode
        filename = f"captures/capture_{timestamp}.png"
        cv2.imwrite(filename, image)
        print(f"[AUTO] Saved screenshot: {filename}")
    else:
        # Save to label folder (positive/negative) when in manual mode
        filename = f"{label}/{label}_{timestamp}.png"
        cv2.imwrite(filename, image)
        print(f"[{label.upper()}] Saved screenshot: {filename}")

def take_automatic_screenshot():
    """Take a screenshot automatically and save it to the captures folder"""
    window = get_maplestory_window()
    if window:
        take_window_screenshot(window, None, auto_mode=True)
    return window is not None

print("Ready! Press 'd' for POSITIVE, 'n' for NEGATIVE, 'a' to toggle AUTO mode, 'esc' to exit.")

auto_mode = False
last_auto_capture_time = 0
auto_capture_interval = 2.0  # seconds between automatic captures

while True:
    current_time = time.time()

    # Handle automatic captures if auto_mode is enabled
    if auto_mode and (current_time - last_auto_capture_time) >= auto_capture_interval:
        if take_automatic_screenshot():
            last_auto_capture_time = current_time

    # Handle keyboard inputs
    if keyboard.is_pressed('d'):
        window = get_maplestory_window()
        if window:
            take_window_screenshot(window, "positive")
        while keyboard.is_pressed('d'): pass  # Wait for release
    elif keyboard.is_pressed('n'):
        window = get_maplestory_window()
        if window:
            take_window_screenshot(window, "negative")
        while keyboard.is_pressed('n'): pass
    elif keyboard.is_pressed('a'):
        auto_mode = not auto_mode
        status = "ENABLED" if auto_mode else "DISABLED"
        print(f"[AUTO] {status}")
        while keyboard.is_pressed('a'): pass  # Wait for release
    elif keyboard.is_pressed('esc'):
        print("Exiting...")
        break

    time.sleep(0.1)
