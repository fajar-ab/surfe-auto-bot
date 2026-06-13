import os
import time

import pyautogui
import pyperclip

from config import BROWSER


def browser_fokus():
    os.system(
        f"xdotool windowactivate --sync $(xdotool search --onlyvisible --class '{BROWSER}' | tail -1)"
    )


def open_extension():
    browser_fokus()
    time.sleep(2)
    pyautogui.hotkey("alt", "shift", "s")


def close_tab():
    browser_fokus()
    time.sleep(0.3)
    pyautogui.hotkey("ctrl", "w")


def refresh_tab():
    browser_fokus()
    time.sleep(0.3)
    pyautogui.hotkey("ctrl", "r")


def get_current_url():
    browser_fokus()
    time.sleep(0.3)
    pyautogui.hotkey("ctrl", "l")
    time.sleep(0.2)
    pyautogui.hotkey("ctrl", "c")
    time.sleep(0.2)
    pyautogui.press("esc")

    return pyperclip.paste()
