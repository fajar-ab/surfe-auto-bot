import time

from config import VISIT_TIMEOUT
from core.logger import logger
from core.window import open_extension
from tasks.surfe import handle_extension_task, handle_visit
from tasks.verification import handle_verification

# Stats
stats = {"tasks_completed": 0, "reports_made": 0, "start_time": None}


def main(is_running, skip_state):
    stats["start_time"] = time.time()

    while is_running():
        try:
            open_extension()
            logger.info("OPEN EXTENSION")
            time.sleep(3)

            if handle_verification():
                continue

            if handle_extension_task():
                continue

            if handle_visit(skip_state, timeout=VISIT_TIMEOUT, is_running=is_running):
                stats["tasks_completed"] += 1
                continue

            time.sleep(2)
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            time.sleep(5)
