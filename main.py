import subprocess
import warnings
import pyautogui
import time
from PIL import ImageGrab
import pygetwindow as gw
from prob import *
import asyncio
import concurrent.futures



# Define the RGB values as constants
ONE = (0, 0, 255)
TWO = (0,128,0)
THREE = (255, 0, 0)
OPENED = (192, 192, 192)
UNOPENED = (226, 226, 226)
UNOPENED2 = (236, 236, 236)
MINE = (0,0,0)
LINE = (173, 173, 173)
LINE2 = (128, 128, 128)
FOUR = (0,0,128)

ROWS = 9
COLS = 9
MINES = 10


alrClicked = [[False for i in range(COLS)] for j in range(ROWS)]
mineMap = [[] for i in range(ROWS)]

for i in range(ROWS):
    mineMap[i] = [0 for j in range(COLS)]

# Create a hashmap to store the RGB values
color_map = {
    THREE: "THREE",
    TWO: "TWO",
    ONE: "ONE",
    OPENED: "OPENED",
    MINE: "MINE",
    FOUR: "FOUR"
}

async def getCell(top_left_x, top_left_y, bottom_right_x, bottom_right_y, mat_i, mat_j):
    region_screenshot = ImageGrab.grab(bbox=(top_left_x, top_left_y, bottom_right_x, bottom_right_y))
    for i in range(region_screenshot.width):
        for j in range(region_screenshot.height):
            pixel_color = region_screenshot.getpixel((i, j))
            if pixel_color == UNOPENED or pixel_color == UNOPENED2:
                mineMap[mat_i][mat_j] = None
                return None
            elif pixel_color == ONE:
                mineMap[mat_i][mat_j] = 1
                alrClicked[mat_i][mat_j] = True
                return 1
            elif pixel_color == TWO:
                mineMap[mat_i][mat_j] = 2
                alrClicked[mat_i][mat_j] = True
                return 2
            elif pixel_color == THREE:
                mineMap[mat_i][mat_j] = 3
                alrClicked[mat_i][mat_j] = True
                return 3
            elif pixel_color == FOUR:
                mineMap[mat_i][mat_j] = 4
                alrClicked[mat_i][mat_j] = True
                return 4
            elif pixel_color == MINE:
                mineMap[mat_i][mat_j] = -1
                return -1
            else:
                if pixel_color != OPENED:
                    pass
                    # print("Unknown color found: ", pixel_color)


async def obtain_mine():
    tasks = []
    for i in range(9):
        for j in range(9):
            task = asyncio.ensure_future(getCell(121+j*20, 230+i*20, 137+j*20, 245+i*20, i, j))
            # await getCell(121+j*20, 230+i*20, 137+j*20, 245+i*20, i, j)
            tasks.append(task)
    await asyncio.gather(*tasks)
    return mineMap




async def main():
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

    mine_window = gw.getWindowsWithTitle('Minesweeper')
    if not mine_window:
        process = subprocess.Popen(exe_path)
        time.sleep(2)
    mine_window[0].activate()

    print('Minesweeper opened successfully!')
    # Get the screenshot of the Minesweeper window
    top_left_x, top_left_y = 121,226
    bottom_right_x, bottom_right_y = 121+ROWS*20, 226+COLS*20

    moved = False

    while True:        
        moved = False
        # Check if only None and 1.0 are left in probsBoard
        if all(cell is None or cell == 1.0 for row in probsBoard for cell in row):
            break

        mineMap = await obtain_mine()

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

        print("-----------------------------------")
        print("Moved: ", moved)

        # for i in range(len(alrClicked)):
        #     print(alrClicked[i])

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


if __name__ == '__main__':
    asyncio.run(main())