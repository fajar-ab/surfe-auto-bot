import tkinter as tk
import threading
import sys

from main import main  
from tkinter import ttk

class PrintToGUI:
    def __init__(self, textbox):
        self.textbox = textbox

    def write(self, message):
        # thread-safe update
        self.textbox.after(0, self.append, message)

    def append(self, message):
        self.textbox.insert(tk.END, message)
        self.textbox.see(tk.END)

    def flush(self):
        pass

# ==== STATE ====
running = False
skip_state = {"value": False}

# ==== FUNCTION CHECK ====
def is_running():
    return running

def request_skip():
    skip_state["value"] = True
    print("[SKIP REQUESTED]")

# ==== START / STOP ====
def start_bot():
    global running
    if not running:
        running = True
        print("\n(Automation Started)\n")
        set_status("running")

        threading.Thread(
            target=main,
            args=(is_running, skip_state),
            daemon=True
        ).start()

def stop_bot():
    global running
    running = False
    print("\n(Automation Stoped)\n")
    set_status("stopped")

# ==== STATUS UI ====
def set_status(state):
    if state == "running":
        status_label.config(text="Status: 🟢 Running", style="Running.TLabel")
    elif state == "stopped":
        status_label.config(text="Status: 🔴 Stopped", style="Stopped.TLabel")
    else:
        status_label.config(text="Status: Idle", style="Idle.TLabel")

# ==== GUI SETUP ====
root = tk.Tk()
root.title("Surfe Bot")
root.geometry("238x220")

# ==== STYLE ====
style = ttk.Style()
style.configure("Idle.TLabel", foreground="gray")
style.configure("Running.TLabel", foreground="green")
style.configure("Stopped.TLabel", foreground="red")

# ==== ROOT CONFIG ====
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# ==== MAIN FRAME ====
main_frame = ttk.Frame(root, padding=2)
main_frame.grid(sticky="nsew")

main_frame.grid_rowconfigure(3, weight=1)
main_frame.grid_columnconfigure(0, weight=1)

# ==== BUTTON FRAME ====
btn_frame = ttk.Frame(main_frame)
btn_frame.grid(row=1, column=0, pady=5)

btn_start = ttk.Button(btn_frame, text="▶ Start", width=6, command=start_bot)
btn_stop = ttk.Button(btn_frame, text="⛔ Stop", width=6, command=stop_bot)
btn_skip = ttk.Button(btn_frame, text="≫ Skip", width=6, command=request_skip)

btn_start.grid(row=0, column=0, padx=5)
btn_stop.grid(row=0, column=1, padx=5)
btn_skip.grid(row=0, column=2, padx=5)

# ==== STATUS ====
status_label = ttk.Label(main_frame, text="Status: Idle", style="Idle.TLabel")
status_label.grid(row=2, column=0, pady=2)

# ==== LOG BOX ====
log_box = tk.Text(main_frame)
log_box.grid(row=3, column=0, sticky="nsew", pady=(5, 0))

# ==== REDIRECT PRINT ====
sys.stdout = PrintToGUI(log_box)

root.mainloop()