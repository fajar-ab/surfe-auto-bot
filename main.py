import pyautogui
import time
import os

def open_extension():
    os.system("xdotool windowactivate --sync $(xdotool search --onlyvisible --class 'Brave' | tail -1)")
    time.sleep(0.5)
    pyautogui.hotkey('alt', 'shift', 's')

open_extension()