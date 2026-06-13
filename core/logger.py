import logging
import sys


class GUILogHandler(logging.Handler):
    def __init__(self, textbox=None):
        super().__init__()
        self.textbox = textbox

    def emit(self, record):
        msg = self.format(record)
        if self.textbox:
            self.textbox.after(0, self.append, msg + "\n")
        else:
            print(msg)

    def append(self, message):
        self.textbox.insert("end", message)
        self.textbox.see("end")


def setup_logger(name="surfe_bot", textbox=None):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("[%(asctime)s] %(message)s", datefmt="%H:%M:%S")

    # Add console handler if not present
    if not any(
        isinstance(h, logging.StreamHandler) and not isinstance(h, GUILogHandler)
        for h in logger.handlers
    ):
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    # Add GUI handler if textbox is provided and not already present
    if textbox and not any(isinstance(h, GUILogHandler) for h in logger.handlers):
        gh = GUILogHandler(textbox)
        gh.setFormatter(formatter)
        logger.addHandler(gh)

    return logger


# Default logger
logger = setup_logger()
