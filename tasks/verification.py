import time

from core.image import click_from_folder, find_image, get_images, wait_for
from core.logger import logger
from core.window import close_tab


def handle_verification():
    if not find_image(get_images("verification_required")):
        return False

    logger.warning("VERIFICATION REQUIRED")

    if click_from_folder("verification_captcha_button"):
        logger.info("CLICK CAPTCHA BUTTON")

    time.sleep(3)
    if click_from_folder("verification_re_captcha", min_search_time=5):
        logger.info("SOLVING CAPTCHA")

    if wait_for("verification_captcha_finished", timeout=120):
        logger.info("CAPTCHA FINISHED")
        close_tab()

    return True
