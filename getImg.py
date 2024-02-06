from PIL import ImageGrab
import win32gui, win32con, win32api
import subprocess
import time

exe_path = './WINMINE.EXE'

def getCell(top_left_x, top_left_y, bottom_right_x, bottom_right_y, mat_i, mat_j):
    region_screenshot = ImageGrab.grab(bbox=(top_left_x, top_left_y, bottom_right_x, bottom_right_y))
    region_screenshot.save(f"{mat_i}_{mat_j}.png")

mine_window = win32gui.FindWindow(None, "Minesweeper")
if mine_window == 0:
    process = subprocess.Popen(exe_path)
    time.sleep(2)
else:
    win32gui.ShowWindow(mine_window, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(mine_window)


for i in range(9):
        for j in range(9):
            getCell(121+j*20, 230+i*20, 137+j*20, 245+i*20, i, j)