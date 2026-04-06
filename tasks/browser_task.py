from core.system import active_window
from core.keyboard import send_key
import config

def open_surfe_extension():
    active_window(class_window=config.BROWSER_WINDOW)
    send_key(keys=config.SHORTCUT_OPEN_SURFE_EXTENSION, delay=0.5)

def refrest_tab():
    active_window(class_window=config.BROWSER_WINDOW)
    send_key(keys=config.SHORTCUT_REFRESH_TAB_BROWSER, delay=0.5)
