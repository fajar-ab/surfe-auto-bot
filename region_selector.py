import tkinter as tk


class RegionSelector:
    def __init__(self):
        self.root = tk.Tk()

        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        self.root.attributes("-topmost", True)
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.overrideredirect(True)

        # On Linux, transparency often needs the window to be visible first
        self.root.wait_visibility(self.root)
        self.root.attributes("-alpha", 0.3)

        # Use a neutral background
        self.canvas = tk.Canvas(
            self.root, cursor="cross", bg="grey", highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        self.start_x = None
        self.start_y = None
        self.rect = None
        self.selection = None

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.root.bind("<Escape>", lambda e: self.root.destroy())

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, 1, 1, outline="red", width=2
        )

    def on_move_press(self, event):
        cur_x, cur_y = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        end_x, end_y = (event.x, event.y)

        # Normalize coordinates
        x1 = min(self.start_x, end_x)
        y1 = min(self.start_y, end_y)
        x2 = max(self.start_x, end_x)
        y2 = max(self.start_y, end_y)

        width = x2 - x1
        height = y2 - y1

        if width > 0 and height > 0:
            self.selection = (x1, y1, width, height)
            print(f"REGION_SELECTED: {self.selection}")
            self.root.destroy()

    def run(self):
        self.root.mainloop()
        return self.selection


if __name__ == "__main__":
    print("Click and drag to select a region. Press ESC to cancel.")
    selector = RegionSelector()
    region = selector.run()
    if region:
        print(f"\nFinal Region: {region}")
        print(f"Format: (x, y, width, height)")
    else:
        print("\nSelection cancelled.")
