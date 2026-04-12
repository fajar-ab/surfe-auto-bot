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
    pyautogui.hotkey('ctrl', 'r')

def get_image_files(folder_name: str):
    folder_path = Path.cwd() / "images" / folder_name
    extensions = ('*.png', '*.jpg', '*.jpeg', '*.bmp')
    
    image_files = []
    if folder_path.exists() and folder_path.is_dir():
        for ext in extensions:
            found_files = sorted(list(folder_path.glob(ext)))
            image_files.extend(found_files)
    else:
        print(f"[Warning] Folder {folder_path} tidak ditemukan.")
        
    return image_files

def match_images(path_images: list, min_search_time: float = 1):
    if not path_images:
        return None

    for image_path in path_images:
        try:
            result = pyautogui.locateOnScreen(str(image_path), confidence=0.8, minSearchTime=min_search_time)
            if result:
                return result
        except (pyautogui.ImageNotFoundException, OSError):
            continue
    return None

def wait_for_images(folder_name: str, timeout=60, interval=1):
    start_time = time.time()
    
    path_images = get_image_files(folder_name)
    
    if not path_images:
        print(f"[WARNING!] Tidak ada gambar di folder: {folder_name}")
        return None

    while time.time() - start_time < timeout:
        elapsed = int(time.time() - start_time)
        print(f"\r[{elapsed//60:02}:{elapsed%60:02}] Wait...", end="")
        result = match_images(path_images)
        if result:
            return result
        time.sleep(interval) 

    return None

def click_button(match_result, duration=0.5):
    point_x, point_y = pyautogui.center(match_result)
    pyautogui.click(point_x, point_y, duration=duration)

def verification_required_check():
    return match_images(get_image_files("verification_required"))

def verification_click_solve_captcha():
    match_result = match_images(get_image_files("verification_captcha_button"))
    click_button(match_result)

def verification_click_re_captcha():
    match_result = match_images(get_image_files("verification_re_captcha"), min_search_time=60)
    click_button(match_result)

def verification_captcha_finished():
    result = wait_for_images(folder_name="verification_captcha_finished", timeout=120)
    if result:
        print("[VERIVICATION CAPTHA FINISH]")
        close_tab()

def task_surfe_exists_check():
    return match_images(get_image_files("task_surfe_exists_check"), min_search_time=60)
    
def task_click_start():
    match_result = match_images(get_image_files("task_start_buttom"))
    click_button(match_result)

def task_surfe_video_view():
    match_result = match_images(get_image_files("surfe_video_view"), min_search_time=60)
    click_button(match_result)

def task_wait_finished():
    result = wait_for_images(folder_name="task_wait_finished", timeout=320)
    if result:
        close_tab()

while True:
    open_extension()
    print("[OPEN EXTENSION]")
    time.sleep(3)
    if verification_required_check():
        print("[VERIVICATION REQUIRED]")
        verification_click_solve_captcha()
        print("[VERIVICATION CAPTHA CLICK]")
        verification_click_re_captcha()
        print("[VERIVICATION CAPTHA SOLVE]")
        verification_captcha_finished()
    elif task_surfe_exists_check():
        print("[TASK EXISTS]")
        task_click_start()
        print("[TASK START CLICK]")
        task_wait_finished()
        print("\n[TASK SFINISH]")
    else:
        break
