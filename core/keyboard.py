import pyautogui
import time
from typing import Sequence

def send_key(keys: Sequence[str], delay: float) -> None:
    time.sleep(delay)
    pyautogui.hotkey(*keys)