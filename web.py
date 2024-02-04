import webbrowser
import pyautogui
import time
from PIL import ImageGrab

url = "https://www.google.com/fbx?fbx=minesweeper"
webbrowser.open(url)

print("opened")
time.sleep(5)

# Click on pixel at coordinates (135, 117) of the screen
pyautogui.click(x=135, y=117)
pyautogui.click(x=135, y=159)
pyautogui.click(x=237, y=352)

print("clicked")

def get_pixel_color(x, y):
    screenshot = ImageGrab.grab(bbox=(x, y, x+1, y+1))
    color = screenshot.getpixel((0, 0))
    return color

for i in range(9):
    for j in range(10):
        pyautogui.moveTo(x=75 + 55 * j, y=175 + 55 * i)
        time.sleep(1)
        print(get_pixel_color(75 + 55 * j, 175 + 55 * i))