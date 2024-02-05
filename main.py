import subprocess
import warnings
import pyautogui
import time
from PIL import ImageGrab
import pygetwindow as gw
from prob import *
import asyncio
import concurrent.futures


ROWS = 9
COLS = 9
MINES = 10


alrClicked = [[False for i in range(COLS)] for j in range(ROWS)]

# Define the RGB values as constants
ONE = (0, 0, 255)
TWO = (0,128,0)
THREE = (255, 0, 0)
OPENED = (192, 192, 192)
MINE = (0,0,0)
LINE = (173, 173, 173)
LINE2 = (128, 128, 128)
FOUR = (0,0,128)

# Create a hashmap to store the RGB values
color_map = {
    THREE: "THREE",
    TWO: "TWO",
    ONE: "ONE",
    OPENED: "OPENED",
    MINE: "MINE",
    FOUR: "FOUR"
}

# Suppress all warnings
warnings.filterwarnings("ignore")

# Specify the path to the .exe file
exe_path = './WINMINE.EXE'

# Open the .exe file
# process = subprocess.Popen(exe_path)
# open the window

probsBoard = [[] for i in range(9)]
for i in range(9):
    probsBoard[i] = [0 for j in range(9)]        

time.sleep(2)
mine_window = gw.getWindowsWithTitle('Minesweeper')
if not mine_window:
    process = subprocess.Popen(exe_path)
mine_window[0].activate()

print('Minesweeper opened successfully!')
# Get the screenshot of the Minesweeper window
top_left_x, top_left_y = 121,226
bottom_right_x, bottom_right_y = 121+ROWS*20, 226+COLS*20

screenshot = pyautogui.screenshot(region=(top_left_x, top_left_y, bottom_right_x - top_left_x, bottom_right_y - top_left_y))

screenshot.save('ss.png')

def getCell(top_left_x, top_left_y, bottom_right_x, bottom_right_y):
    region_screenshot = ImageGrab.grab(bbox=(top_left_x, top_left_y, bottom_right_x, bottom_right_y))
    for i in range(region_screenshot.width):
        for j in range(region_screenshot.height):
            pixel_color = region_screenshot.getpixel((i, j))
            if pixel_color == (223, 223, 223):
                return "Unopened"
            elif pixel_color == ONE:
                return "One"
            elif pixel_color == TWO:
                return "Two"
            elif pixel_color == THREE:
                return "Three"
            elif pixel_color == FOUR:
                return "Four"
            elif pixel_color == MINE:
                return "Mine"


def obtain_mine():
    mineMap = [[] for i in range(ROWS)]
    for i in range(ROWS):
        mineMap[i] = [0 for j in range(COLS)]
    for i in range(9):
        for j in range(9):
            currCell = getCell(121+j*20, 230+i*20, 137+j*20, 245+i*20)
            # print(currCell)
            if currCell == "Unopened":
                mineMap[i][j] = None
            if currCell == "One":
                mineMap[i][j] = 1
            elif currCell == "Two":
                mineMap[i][j] = 2
            elif currCell == "Three":
                mineMap[i][j] = 3
            elif currCell == "Four":
                mineMap[i][j] = 4
            elif currCell == "Mine":
                mineMap[i][j] = -1
    return mineMap

moved = False



while True:        
    moved = False
    # Check if only None and 1.0 are left in probsBoard
    if all(cell is None or cell == 1.0 for row in probsBoard for cell in row):
        break

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
                if not probsBoard[i][j] == None and probsBoard[i][j] < min_prob:
                    min_prob = probsBoard[i][j]
                    min_prob_cell = (i, j)

        pyautogui.click(121 + min_prob_cell[1] * 20, 230 + min_prob_cell[0] * 20)
        time.sleep(0.01)