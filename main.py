import subprocess
import sys
import warnings
import pyautogui
import time
from PIL import ImageGrab
import pygetwindow as gw
from prob import *
import win32api, win32con, win32gui
import asyncio
import concurrent.futures


ROWS = 9
COLS = 9
MINES = 10

# Define the RGB values as constants
ONE = (0, 0, 255)
TWO = (0,128,0)
THREE = (255, 0, 0)
OPENED = (192, 192, 192)
MINE = (0,0,0)
LINE = (173, 173, 173)
LINE2 = (128, 128, 128)
FOUR = (0,0,128)
FIVE = (128,0,0)

# Create a hashmap to store the RGB values
color_map = {
    THREE: "THREE",
    TWO: "TWO",
    ONE: "ONE",
    OPENED: "OPENED",
    MINE: "MINE",
    FOUR: "FOUR",
    FIVE: "FIVE"
}

# Suppress all warnings
warnings.filterwarnings("ignore")

# Specify the path to the .exe file
exe_path = './WINMINE.EXE'

# Open the .exe file
# process = subprocess.Popen(exe_path)
# open the window

probsBoard = [[] for i in range(ROWS)]
for i in range(ROWS):
    probsBoard[i] = [0 for j in range(COLS)]        

mine_window = win32gui.FindWindow(None, "Minesweeper")
print(mine_window)
if mine_window != 0:
    win32gui.ShowWindow(mine_window, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(mine_window)
else:
    process = subprocess.Popen(exe_path)
    time.sleep(2)
    pyautogui.click(229, 297)
    pyautogui.click(178, 357)
    pyautogui.click(263, 375)
    # time.sleep(2)


print('Minesweeper opened successfully!')
# Get the screenshot of the Minesweeper window
top_left_x, top_left_y = 121,226
bottom_right_x, bottom_right_y = 121+ROWS*20, 226+COLS*20

alrClicked = [[False for i in range(COLS)] for j in range(ROWS)]
mineMap = [[] for i in range(ROWS)]
for i in range(ROWS):
    mineMap[i] = [0 for j in range(COLS)]

# screenshot = pyautogui.screenshot(region=(top_left_x, top_left_y, bottom_right_x - top_left_x, bottom_right_y - top_left_y))

# screenshot.save('ss.png')

def getCell(top_left_x, top_left_y, bottom_right_x, bottom_right_y, mat_i, mat_j):
    region_screenshot = ImageGrab.grab(bbox=(top_left_x, top_left_y, bottom_right_x, bottom_right_y))
    for i in range(region_screenshot.width):
        for j in range(region_screenshot.height):
            pixel_color = region_screenshot.getpixel((i, j))
            if pixel_color == (192, 192, 192):
                continue            
            elif pixel_color == ONE:
                mineMap[mat_i][mat_j] = 1
                alrClicked[mat_i][mat_j] = True
            elif pixel_color == TWO:
                mineMap[mat_i][mat_j] = 2
                alrClicked[mat_i][mat_j] = True
            elif pixel_color == THREE:
                mineMap[mat_i][mat_j] = 3
                alrClicked[mat_i][mat_j] = True
            elif pixel_color == FOUR:
                mineMap[mat_i][mat_j] = 4
                alrClicked[mat_i][mat_j] = True
            elif pixel_color == FIVE:
                mineMap[mat_i][mat_j] = 5
                alrClicked[mat_i][mat_j] = True
            elif pixel_color == MINE:
                # pyautogui.click(223, 194)
                # sys.exit(0)
                mineMap[mat_i][mat_j] = -1
            else:
                mineMap[mat_i][mat_j] = None

def obtain_mine():
    for i in range(ROWS):
        for j in range(COLS):
            getCell(121+j*20, 230+i*20, 137+j*20, 245+i*20, i, j)
    return mineMap

moved = False



while True:        
    moved = False
    # Check if only None and 1.0 are left in probsBoard
    if all(cell is None or cell == 1.0 for row in probsBoard for cell in row):
        break

    mineMap = obtain_mine()
    if all(cell is None for row in mineMap for cell in row):
        pyautogui.click(229, 297)
        pyautogui.click(178, 357)
        pyautogui.click(263, 375)
        mineMap = obtain_mine()

    for row in mineMap:
        print(row)


    probsBoard = calcprobs(mineMap, MINES)
    for row in probsBoard:
        print(row)

    for i in range(len(probsBoard)):
        for j in range(len(probsBoard[0])):
            if probsBoard[i][j] == 0.0 and not alrClicked[i][j]:
                moved = True
                pyautogui.click(121+j*20, 230+i*20)
                alrClicked[i][j] = True
                # time.sleep(0.00001)

    print("-----------------------------------")
    print("Moved: ", moved)

    if not moved:
        print("-----------------------------------")
        print("No 0.0 or 1.0 cells found, clicking on the cell with the lowest probability")
        print("-----------------------------------")
        min_prob = 1.0
        min_prob_cell = None

        for i in range(len(probsBoard)):
            for j in range(len(probsBoard[0])):
                if not probsBoard[i][j] == None and probsBoard[i][j] < min_prob and not alrClicked[i][j]:
                    min_prob = probsBoard[i][j]
                    min_prob_cell = (i, j)

        pyautogui.click(121 + min_prob_cell[1] * 20, 230 + min_prob_cell[0] * 20)
        alrClicked[min_prob_cell[0]][min_prob_cell[1]] = True
        # time.sleep(0.01)