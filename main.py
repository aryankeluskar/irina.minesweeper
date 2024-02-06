import subprocess
import sys
import warnings
import pyautogui
import time
from PIL import ImageGrab
from prob import *
import win32con, win32gui

ROWS = 16
COLS = 16
MINES = 40

# Define the RGB values as constants
ONE = (0, 0, 255)
TWO = (0,128,0)
TWO2 = (1,128,1)
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

probsBoard = [[0.0 for i in range(COLS)] for j in range(ROWS)]
alrClicked = [[True for i in range(COLS)] for j in range(ROWS)]

mine_window = win32gui.FindWindow(None, "Minesweeper")
if mine_window == 0:
    process = subprocess.Popen(exe_path)
    time.sleep(2)
    pyautogui.click(228, 278)
    pyautogui.click(254, 361)
    pyautogui.click(160, 323)
    
else:
    print(win32gui.GetWindowText(mine_window))
    win32gui.ShowWindow(mine_window, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(mine_window)
    time.sleep(5)

pyautogui.click(228, 278)
pyautogui.click(254, 361)
pyautogui.click(160, 323)

print('Minesweeper opened successfully!')
# Get the screenshot of the Minesweeper window
top_left_x, top_left_y = 121,226
bottom_right_x, bottom_right_y = 121+ROWS*20, 226+COLS*20

# screenshot = pyautogui.screenshot(region=(top_left_x, top_left_y, bottom_right_x - top_left_x, bottom_right_y - top_left_y))

# screenshot.save('ss.png')

def getCell(whole_ss, top_left_x, top_left_y, bottom_right_x, bottom_right_y, mat_i, mat_j):
    region_screenshot = whole_ss.crop((top_left_x, top_left_y, bottom_right_x, bottom_right_y))
    region_screenshot.save(f'{mat_i}{mat_j}.png')
    if region_screenshot.getpixel((0,0)) == (255, 255, 255):
        alrClicked[mat_i][mat_j] = False
        return None
    elif region_screenshot.getpixel((4,9)) == THREE:
        # its actually 5
        alrClicked[mat_i][mat_j] = True
        return 5
    elif region_screenshot.getpixel((9,7)) == ONE:
        alrClicked[mat_i][mat_j] = True
        return 1
    elif region_screenshot.getpixel((11,6)) == TWO or region_screenshot.getpixel((11,6)) == TWO2 or region_screenshot.getpixel((13,6)) == TWO or region_screenshot.getpixel((13,6)) == TWO2:
        alrClicked[mat_i][mat_j] = True
        return 2
    elif region_screenshot.getpixel((11,8)) == THREE:
        alrClicked[mat_i][mat_j] = True
        return 3
    elif region_screenshot.getpixel((12,9)) == FOUR:
        alrClicked[mat_i][mat_j] = True
        return 4
    elif region_screenshot.getpixel((13,12)) == MINE or region_screenshot.getpixel((11,14)) == MINE:
        alrClicked[mat_i][mat_j] = True
        return -1


def obtain_mine():
    whole_screenshot = ImageGrab.grab(bbox=(120,225, 120+(COLS+1)*20, 225+(ROWS+1)*20))
    whole_screenshot.save('ss.png')                      
    # return None                
    mineMap = [[] for i in range(ROWS)]
    for i in range(ROWS):
        mineMap[i] = [0 for j in range(COLS)]
    for i in range(ROWS):
        for j in range(COLS):
            mineMap[i][j] = getCell(whole_screenshot, 10+j*20, 19+i*20, 25+j*20, 34+i*20, i, j)
    return mineMap

moved = False



while True:        
    moved = False
    mineMap = obtain_mine()
    # print("got here")
    # Check if only None and 1.0 are left in probsBoard
    for i in mineMap:
        for j in i:
            if j == -1:
                print("MINE FOUND")
                sys.exit(0)


    # for row in mineMap:
    #     print(row)


    probsBoard = calcprobs(mineMap, MINES)
    # for row in probsBoard:
    #     print(row)

    for i in range(len(probsBoard)):
        for j in range(len(probsBoard[0])):
            if probsBoard[i][j] == 0.0 and not alrClicked[i][j]:
                moved = True
                pyautogui.click(138+j*20, 250+i*20)
                # time.sleep(1)
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
                    print("Found lower")
                    min_prob = probsBoard[i][j]
                    min_prob_cell = (i, j)

        pyautogui.click(138 + min_prob_cell[1] * 20, 250 + min_prob_cell[0] * 20)
        alrClicked[min_prob_cell[0]][min_prob_cell[1]] = True
        # time.sleep(0.01)