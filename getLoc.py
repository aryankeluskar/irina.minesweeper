import pyautogui
from pynput.mouse import Listener

def get_pixel_location():
    x, y = pyautogui.position()
    print(f"Pixel location: x={x}, y={y}")

def on_click(x, y, button, pressed):
    if button == button.left and pressed:
        get_pixel_location()

with Listener(on_click=on_click) as listener:
    listener.join()
