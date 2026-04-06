import pyautogui
import time
from typing import Sequence

def send_key(keys: Sequence[str], delay: float = 0.2) -> None:
    time.sleep(delay)
    pyautogui.hotkey(*keys)