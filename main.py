from pathlib import Path
import pyautogui
import pyperclip
import time
import os

# ================= CONFIG =================
CONFIDENCE = 0.8
INTERVAL = 1
IMAGE_CACHE = {}
VISIT_TIMEOUT = 300

# ================= WINDOW CONTROL =================
def browser_fokus():
    os.system("xdotool windowactivate --sync $(xdotool search --onlyvisible --class 'Brave' | tail -1)")

def open_extension():
    browser_fokus()
    time.sleep(2)
    pyautogui.hotkey('alt', 'shift', 's')

def close_tab():
    browser_fokus()
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'w')

def refresh_tab():
    browser_fokus()
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'r')

def get_current_url():
    browser_fokus()
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'l') 
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.2)

    return pyperclip.paste()

# ================= IMAGE HANDLING =================
def load_images(folder_name: str):
    folder_path = Path.cwd() / "images" / folder_name
    extensions = ('*.png', '*.jpg', '*.jpeg', '*.bmp')

    if not folder_path.exists():
        print(f"[WARNING] Folder tidak ditemukan: {folder_path}")
        return []

    images = []
    for ext in extensions:
        images.extend(sorted(folder_path.glob(ext)))

    return images


def get_images(folder_name: str):
    if folder_name not in IMAGE_CACHE:
        IMAGE_CACHE[folder_name] = load_images(folder_name)
    return IMAGE_CACHE[folder_name]


# ================= CORE ENGINE =================
def find_image(images, min_search_time=0.5):
    for img in images:
        try:
            result = pyautogui.locateOnScreen(
                str(img),
                confidence=CONFIDENCE,
                grayscale=True,
                minSearchTime=min_search_time
            )
            if result:
                return result
        except Exception:
            continue
    return None


def wait_for(folder, timeout=60, interval=INTERVAL):
    start = time.time()
    images = get_images(folder)

    if not images:
        return None

    while time.time() - start < timeout:
        elapsed = int(time.time() - start)
        print(f"\r[{elapsed//60:02}:{elapsed%60:02}] Waiting ...", end="")

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


def click_from_folder(folder, min_search_time=0.5):
    result = find_image(get_images(folder), min_search_time)
    return click(result)


# ================= VERIFICATION =================
def handle_verification():
    if not find_image(get_images("verification_required")):
        return False

    print("[VERIFICATION REQUIRED]")

    if click_from_folder("verification_captcha_button"):
        print("[CLICK CAPTCHA BUTTON]")

    if click_from_folder("verification_re_captcha", min_search_time=5):
        print("[SOLVING CAPTCHA]")

    if wait_for("verification_captcha_finished", timeout=120):
        print("[CAPTCHA FINISHED]")
        close_tab()

    return True


# ================= VISIT =================
def handle_visit(timeout=30):
    start_time = time.time()

    while time.time() - start_time < timeout:
        elapsed = int(time.time() - start_time)
        print(f"[{elapsed//60:02}:{elapsed%60:02}] Visit Waiting ...")

        url = get_current_url()
        if not url or "https://surfe.be/meta-redirect" in url:
            continue

        if "https://surfe.be/video/view/" in url:
            surfe_video_view()

        if find_image(get_images("visit_error_page")):
            print("[PAGE ERROR]")
            close_tab()

            success = handle_surfe_report("no_reward")
            if not success:
                print("[REPORT FAILED]")

            close_tab()

            return False

        if find_image(get_images("visit_wait_finished")):
            print("[TASK FINISHED]")
            close_tab()

            return True
    
    return False


def surfe_video_view():
    if click_from_folder("surfe_video_view", min_search_time=20):
        print("[Video Surfe View]")

    return True


def handle_surfe_report(reason="no_reward"):
    open_extension()
    print("[OPEN EXTENSION]")

    if not click_from_folder("surfe_report_dislike", min_search_time=20):
        return False

    print("[FEEDBACK PAGE]")

    path = f"surfe_report_feedback/{reason}"

    if click_from_folder(path, min_search_time=40):
        print(f"[Reason] {reason} selected!")
        pyautogui.press("enter", interval=0.5)

        return True

    print(f"[WARNING] Failed or unknown reason: {reason}")
    return False


# ================= EXTENSION TASK =================
def handle_extension_task():
    if find_image(get_images("task_surfe_exists"), min_search_time=2):
        print("[TASK FOUND]")

        if click_from_folder("task_start_buttom"):
            print("[CLICK START]")
        
        return False
    
    if find_image(get_images("task_surfe_unexists"), min_search_time=2):
        print("[TASK NOT FOUND]")

        return True

    return True


# ================= MAIN LOOP =================
def main(is_running):
    while is_running():
        open_extension()
        print("[OPEN EXTENSION]")
        time.sleep(3)

        if handle_verification():
            continue

        if handle_extension_task():
            continue

        if handle_visit(timeout=VISIT_TIMEOUT):
            continue

        time.sleep(2)

