import threading
import time
import tkinter as tk
from tkinter import ttk

from core.logger import setup_logger
from main import main, stats

# ==== STATE ====
running = False
skip_state = {"value": False}
logs_visible = False


# ==== FUNCTION CHECK ====
def is_running():
    return running


def request_skip():
    skip_state["value"] = True
    logger.info("SKIP REQUESTED")


def toggle_logs():
    global logs_visible
    if logs_visible:
        log_frame.grid_remove()
        btn_toggle.config(text="▼ Show Logs")
        root.geometry("300x125")
        logs_visible = False
    else:
        log_frame.grid(row=4, column=0, sticky="nsew", pady=(5, 0))
        btn_toggle.config(text="▲ Hide Logs")
        root.geometry("300x350")
        logs_visible = True


# ==== START / STOP ====
def start_bot():
    global running
    if not running:
        running = True
        logger.info("Automation Started")
        set_status("running")

        threading.Thread(
            target=main, args=(is_running, skip_state), daemon=True
        ).start()

        update_stats()


def stop_bot():
    global running
    running = False
    logger.info("Automation Stopped")
    set_status("stopped")


# ==== STATUS UI ====
def set_status(state):
    if state == "running":
        status_label.config(text="Status: 🟢 Running", style="Running.TLabel")
    elif state == "stopped":
        status_label.config(text="Status: 🔴 Stopped", style="Stopped.TLabel")
    else:
        status_label.config(text="Status: Idle", style="Idle.TLabel")


def update_stats():
    if not running:
        return

    # Calculate uptime
    if stats["start_time"]:
        uptime_seconds = int(time.time() - stats["start_time"])
        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_str = f"{hours:02}:{minutes:02}:{seconds:02}"
    else:
        uptime_str = "00:00:00"

    stats_label.config(text=f"Tasks: {stats['tasks_completed']} | Uptime: {uptime_str}")
    root.after(1000, update_stats)


# ==== GUI SETUP ====
root = tk.Tk()
root.title("Surfe Bot Pro")
root.geometry("300x125")

# ==== STYLE ====
style = ttk.Style()
style.configure("Idle.TLabel", foreground="gray")
style.configure("Running.TLabel", foreground="green")
style.configure("Stopped.TLabel", foreground="red")
style.configure("Small.TButton", font=("TkDefaultFont", 8))

# ==== ROOT CONFIG ====
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# ==== MAIN FRAME ====
main_frame = ttk.Frame(root, padding=5)
main_frame.grid(sticky="nsew")

main_frame.grid_rowconfigure(4, weight=1)
main_frame.grid_columnconfigure(0, weight=1)

# ==== BUTTON FRAME ====
btn_frame = ttk.Frame(main_frame)
btn_frame.grid(row=0, column=0, pady=5)

btn_start = ttk.Button(btn_frame, text="▶ Start", width=8, command=start_bot)
btn_stop = ttk.Button(btn_frame, text="⛔ Stop", width=8, command=stop_bot)
btn_skip = ttk.Button(btn_frame, text="≫ Skip", width=8, command=request_skip)

btn_start.grid(row=0, column=0, padx=2)
btn_stop.grid(row=0, column=1, padx=2)
btn_skip.grid(row=0, column=2, padx=2)

# ==== STATUS & STATS ====
status_label = ttk.Label(main_frame, text="Status: Idle", style="Idle.TLabel")
status_label.grid(row=1, column=0, pady=2)

stats_label = ttk.Label(main_frame, text="Tasks: 0 | Uptime: 00:00:00")
stats_label.grid(row=2, column=0, pady=2)

# ==== TOGGLE BUTTON ====
btn_toggle = ttk.Button(
    main_frame, text="▼ Show Logs", style="Small.TButton", command=toggle_logs
)
btn_toggle.grid(row=3, column=0, pady=2)

# ==== LOG BOX ====
log_frame = ttk.LabelFrame(main_frame, text="Logs")
# Start hidden
# log_frame.grid(row=4, column=0, sticky="nsew", pady=(5, 0))
log_frame.grid_rowconfigure(0, weight=1)
log_frame.grid_columnconfigure(0, weight=1)

log_box = tk.Text(log_frame, height=10, font=("Consolas", 9))
log_box.grid(row=0, column=0, sticky="nsew")

scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=log_box.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
log_box.configure(yscrollcommand=scrollbar.set)

# ==== SETUP LOGGER ====
logger = setup_logger("surfe_bot", log_box)

root.mainloop()
