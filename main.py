# Website used for testing - https://humanbenchmark.com/tests/reactiontime
import mss
from PIL import Image
import pydirectinput
import time
import keyboard

target_color = None

region = {
    "top": 465,
    "left": 800,
    "width": 150,
    "height": 150
}

running = False
color_found = False

def pick_color():
    global target_color
    x, y = pydirectinput.position()

    with mss.mss() as sct:
        monitor = {
            "top": y,
            "left": x,
            "width": 1,
            "height": 1
        }
        shot = sct.grab(monitor)
        image = Image.frombytes("RGB", shot.size, shot.rgb)
        r, g, b = image.getpixel((0, 0))
        target_color = (int(r), int(g), int(b))
        print(f"Picked color at ({x},{y}): RGB={target_color}")

def toggle():
    global running
    running = not running
    print("Scanner:", "ON" if running else "OFF")

keyboard.add_hotkey("F8", toggle)# Hotkey: F8 to start / stop the scan
keyboard.add_hotkey("F7", pick_color)

with mss.mss() as sct:
    print("Press F8, to beginn or to stop the Scanner.")
    print(f"Current color: {target_color}, press F7 to pick new color.")

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
                pydirectinput.click()
                print("Color detected - Click")
                color_found = True
            elif not found:
                color_found = False

        time.sleep(0.50)
