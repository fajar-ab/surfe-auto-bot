from pathlib import Path
import pyautogui
import time
import os

def browser_fokus():
    os.system("xdotool windowactivate --sync $(xdotool search --onlyvisible --class 'Brave' | tail -1)")

def open_extension():
    browser_fokus()
    time.sleep(0.5)
    pyautogui.hotkey('alt', 'shift', 's')

def close_tab():
    browser_fokus()
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'w')

def refresh_tab():
    browser_fokus()
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'w')

def match_images(images: list):
    for image_name in images:
        image_path = Path.cwd() / "images" / image_name
        try:
            result = pyautogui.locateOnScreen( str(image_path), confidence=0.5)
            if result:
                return  result
        except pyautogui.ImageNotFoundException:
            continue
    return None

def wait_for_images(images: list, timeout=60, interval=1):
    start_time = time.time()

    while time.time() - start_time < timeout:
        print("Tunggu...")
        result = match_images(images)
        if result:
            return result
        time.sleep(interval)  # jeda biar gak berat CPU

    return None

def cek_verification_required():
    result = match_images(["verification_required.png"])
    return result

def clik_solve_captcha():
    match_result = match_images(["solve_captcha_button.png"])
    point_x, point_y = pyautogui.center(match_result)
    pyautogui.click(point_x, point_y, duration=0.5)

def on_captcha_finished():
    result = wait_for_images(["captcha_solve1.png", "captcha_solve2.png"])
    if result:
        close_tab()


def is_task_surfe_exists():
    result = wait_for_images(["task_exists.png"])
    return result
    
def click_task():
    match_result = match_images(["start_task_button.png"])
    point_x, point_y = pyautogui.center(match_result)
    pyautogui.click(point_x, point_y, duration=0.5)

def on_task_finished():
    result = wait_for_images(["visit_complite1.png", "visit_complite2.png"], timeout=120)
    if result:
        print(result)
        point_x, point_y = pyautogui.center(result)
        pyautogui.click(point_x, point_y, duration=0.5)

open_extension()
time.sleep(2)
if cek_verification_required():
    clik_solve_captcha()
    on_captcha_finished()
elif is_task_surfe_exists():
    click_task()
    on_task_finished()
