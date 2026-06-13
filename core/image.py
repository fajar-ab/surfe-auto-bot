import time
from pathlib import Path

import pyautogui

from config import CONFIDENCE, IMAGE_CACHE, INTERVAL


def load_images(folder_name: str):
    folder_path = Path.cwd() / "images" / folder_name
    extensions = ("*.png", "*.jpg", "*.jpeg", "*.bmp")

    if not folder_path.exists():
        return []

    images = []
    for ext in extensions:
        images.extend(sorted(folder_path.glob(ext)))

    return images


def get_images(folder_name: str):
    if folder_name not in IMAGE_CACHE:
        IMAGE_CACHE[folder_name] = load_images(folder_name)
    return IMAGE_CACHE[folder_name]


def find_image(images, min_search_time=0.5, region=None):
    """
    Optimized image search with optional region support.
    """
    for img in images:
        try:
            result = pyautogui.locateOnScreen(
                str(img),
                confidence=CONFIDENCE,
                grayscale=True,
                minSearchTime=min_search_time,
                region=region,
            )
            if result:
                return result
        except Exception:
            # pyautogui.locateOnScreen can throw ImageNotFoundException in some versions
            # or other screen capture related errors. We skip and continue.
            continue
    return None


def wait_for(folder, timeout=60, interval=INTERVAL, is_running=None):
    start = time.time()
    images = get_images(folder)

    if not images:
        return None

    while time.time() - start < timeout:
        if is_running and not is_running():
            return None

        elapsed = int(time.time() - start)
        # We'll use a logger later, for now keep print but better
        # print(f"[{elapsed//60:02}:{elapsed%60:02}] Waiting for {folder}...")

        result = find_image(images)
        if result:
            return result

        time.sleep(interval)

    return None


def click(match_result, duration=0.3):
    if not match_result:
        return False

    x, y = pyautogui.center(match_result)
    pyautogui.click(x, y, duration=duration)
    return True


def click_from_folder(folder, min_search_time=0.5, region=None):
    result = find_image(get_images(folder), min_search_time, region=region)
    return click(result)
