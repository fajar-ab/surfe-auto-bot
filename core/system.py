import os

def active_window(class_window: str) -> None:
    cmd = f"xdotool windowactivate --sync $(xdotool search --onlyvisible --class '{class_window}' | tail -1)"
    os.system(cmd)