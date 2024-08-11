import keyboard
from PIL import ImageGrab
from config import TELEGRAM_BOT_TOKEN_CONFIG, CHAT_ID_CONFIG
import requests
import time
import os
from io import BytesIO

TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_TOKEN'] or TELEGRAM_BOT_TOKEN_CONFIG 
CHAT_ID = os.environ['CHAT_ID'] or CHAT_ID_CONFIG 

def send_screenshot_to_telegram(image):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    buffer = BytesIO()
    image.save(buffer, format='PNG')  # Save the image to the BytesIO buffer
    buffer.seek(0)  # Rewind the buffer to the beginning
    files = {'photo': ('screenshot.png', buffer, 'image/png')}
    data = {'chat_id': CHAT_ID}
    response = requests.post(url, files=files, data=data)
    if response.status_code == 200:
        print("Screenshot sent successfully!")
    else:
        print(f"Failed to send screenshot. Status code: {response.status_code}, Response: {response.text}")


def take_screenshot():
    screenshot = ImageGrab.grab()
    filename = f"screenshot_{int(time.time())}.png"
    print(f"Screenshot saved as {filename}")
    send_screenshot_to_telegram(screenshot.tobytes())

def main():
    print("Listening for the shortcut...")
    keyboard.add_hotkey('ctrl+k', take_screenshot)

    keyboard.wait('esc')  # Wait for the user to press the 'esc' key
    print("Terminating...");
if __name__ == "__main__":
    main()

