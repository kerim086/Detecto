# Website used for testing - https://humanbenchmark.com/tests/reactiontime
import mss
from PIL import Image
import pyautogui
import time
import keyboard

target_color = (59, 52, 47)

region = {
    "top": 465,
    "left": 800,
    "width": 150,
    "height": 150
}

running = False
color_found = False

def toggle():
    global running
    running = not running
    print("Scanner:", "ON" if running else "OFF")

keyboard.add_hotkey("F8", toggle)  # Hotkey: F8 to start / stop the scan

with mss.mss() as sct:
    print("Press F8, to beginn or to stop the Scanner.")

    while True:
        if keyboard.is_pressed("Esc"):
            break

        if running:
            screenshot = sct.grab(region)
            img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
            pixels = img.load()

            found = False

            for x in range(img.width):
                for y in range(img.height):
                    if pixels[x, y] == target_color:
                        found = True
                        break
                if found:
                    break

            if found and not color_found:
                pyautogui.click()
                print("Color detected - Click")
                color_found = True
            elif not found:
                color_found = False

        time.sleep(0.50)
