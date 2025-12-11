import mss
from PIL import Image
import time
import pyautogui

target_color = (75, 219, 106)

region = {
    "top": 300, 
    "left": 500, 
    "width": 200, 
    "height": 200
}

color_found = False

with mss.mss() as sct:
    while True:
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
            color_found = True
        elif not found:
            color_found = False

        time.sleep(0.01)
