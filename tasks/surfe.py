import time

import pyautogui

from config import RULES_URL_ACTIONS
from core.image import click_from_folder, find_image, get_images, wait_for
from core.logger import logger
from core.window import close_tab, get_current_url, open_extension


def handle_extension_task():
    if find_image(get_images("task_surfe_exists"), min_search_time=2):
        logger.info("TASK FOUND")
        if click_from_folder("task_start_buttom"):
            logger.info("CLICK START")
        return False

    if find_image(get_images("task_surfe_unexists"), min_search_time=2):
        logger.info("TASK NOT FOUND")
        close_tab()
        success = handle_surfe_report("multiple_redirects")
        if not success:
            logger.error("REPORT FAILED")
        close_tab()
        return True

    return True


def handle_surfe_report(reason="no_reward"):
    open_extension()
    logger.info("OPEN EXTENSION FOR REPORT")

    if not click_from_folder("surfe_report_dislike", min_search_time=20):
        return False

    logger.info("FEEDBACK PAGE")

    path = f"surfe_report_feedback/{reason}"
    if click_from_folder(path, min_search_time=40):
        logger.info(f"Reason: {reason.replace('_', ' ')} selected!")
        pyautogui.press("enter", interval=0.5)
        return True

    logger.warning(f"Failed or unknown reason: {reason.replace('_', ' ')}")
    return False


def check_url_rules(current_url):
    for rule in RULES_URL_ACTIONS:
        for pattern in rule["patterns"]:
            if pattern in current_url:
                return handle_special_action(rule["action"])
    return None


def handle_special_action(action):
    if action == "cancel_xdg":
        logger.info("XDG DETECTED")
        time.sleep(5)
        pyautogui.press("enter", presses=1)
        return True

    elif action == "surfe_video_view":
        if click_from_folder("surfe_video_view", min_search_time=20):
            logger.info("Video Surfe View")
        return True

    elif action in [
        "multiple_redirects",
        "breaks_extension",
        "no_reward",
        "unable_to_play",
    ]:
        logger.info(f"[DETECTED] {str(action).replace('_', ' ')}")
        close_tab()
        success = handle_surfe_report(
            action
        )  # Use the action directly if it matches reason
        if not success:
            logger.error("REPORT FAILED")
        close_tab()
        return False

    return True


def handle_visit(skip_state, timeout=30, is_running=None):
    start_time = time.time()
    last_handled_url = None

    while time.time() - start_time < timeout:
        if is_running and not is_running():
            return False

        if skip_state["value"]:
            logger.info("TASK SKIPPED")
            skip_state["value"] = False
            close_tab()
            return False

        elapsed = int(time.time() - start_time)
        # logger.debug(f"Visit Waiting... {elapsed}/{timeout}s")

        url = get_current_url()
        if not url or "surfe.be/meta-redirect" in url:
            continue

        if url != last_handled_url:
            result = check_url_rules(url)
            if result is False:
                return False
            if result is True:
                logger.info("ACTION URL: Already handled")
                last_handled_url = url

        if find_image(get_images("visit_youtube_error")) and "www.youtube.com" in url:
            logger.warning("VISIT ERROR: Youtube not play")
            close_tab()
            if not handle_surfe_report("unable_to_play"):
                logger.error("REPORT FAILED")
            close_tab()
            return False

        if find_image(get_images("visit_error_page")):
            logger.warning("VISIT ERROR: Page not play")
            close_tab()
            if not handle_surfe_report("no_reward"):
                logger.error("REPORT FAILED")
            close_tab()
            return False

        if find_image(get_images("visit_wait_finished")):
            logger.info("TASK FINISHED")
            close_tab()
            return True

    logger.info("TASK TIMEOUT")
    close_tab()
    return False
