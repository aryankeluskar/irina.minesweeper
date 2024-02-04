import pyautogui
from PIL import Image
import pygetwindow as gw


def capture_minesweeper_map():
    # Adjust the coordinates based on your screen resolution and Minesweeper position
    top_left_x, top_left_y = 121,226
    bottom_right_x, bottom_right_y = 297, 401

    screenshot = pyautogui.screenshot(region=(top_left_x, top_left_y, bottom_right_x - top_left_x, bottom_right_y - top_left_y))
    return screenshot

def process_minesweeper_map(screenshot):
    image_data = screenshot.load()
    width, height = screenshot.size

    minesweeper_map = []

    for y in range(height):
        row = []
        for x in range(width):
            pixel = image_data[x, y]
            
            # You may need to adjust these color values based on your Minesweeper theme
            if pixel == (255, 255, 255):  # Unopened box
                row.append('U')
            elif pixel == (192, 192, 192):  # Opened box
                row.append('O')
            elif pixel == (0, 0, 255):  # Mine
                row.append('M')
            else:
                # Extract the number from the color or use a different marker for numbers
                row.append('N')

        minesweeper_map.append(row)

    return minesweeper_map

def main():

    mine_window = gw.getWindowsWithTitle('Minesweeper')
    mine_window[0].activate()
    minesweeper_screenshot = capture_minesweeper_map()
    minesweeper_map = process_minesweeper_map(minesweeper_screenshot)

    for row in minesweeper_map:
        print(' '.join(row))

if __name__ == "__main__":
    main()
