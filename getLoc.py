import pyautogui
from pynput.mouse import Listener

def get_pixel_location():
    x, y = pyautogui.position()
    print(f"Pixel location: x={x}, y={y}")
    print("Modify main.py so the constants match accordingly")
    print(f"MI_WINDOW_TOP_LEFT_X = {x}")
    print(f"MI_WINDOW_TOP_LEFT_Y = {y}")

def on_click(x, y, button, pressed):
    if button == button.left and pressed:
        get_pixel_location()

with Listener(on_click=on_click) as listener:
    listener.join()

