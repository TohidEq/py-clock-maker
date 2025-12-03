configs_dic = {
    "pointer": {
        "POINTER_SHAPE": "circle",   # "line", "circle"
        "POINTER_SCALE": 4,          # higher number = better anti-aliasing = slower generation
        "POINTER_START_AT": 80,      # distance from center (in px)
        "POINTER_LENGTH": 20,        # length OR radius (depends on shape)
        "POINTER_THICKNESS": 10,
        "POINTER_COLOR": (255, 0, 0, 150),
        "POINTER_ROUND_START": True,
        "POINTER_ROUND_END": True,
        "POINTER_SIZE": 200,
    },
    "frame": {
        "FRAME_SCALE": 4,                  # higher number = better anti-aliasing = slower generation
        "FRAME_CLOCK_PADDING": 10,
        "FRAME_HAS_BORDER": True,
        "FRAME_BORDER_RADIUS": 2,
        "FRAME_BORDER_COLOR": (0, 0, 0, 255),
        "FRAME_CLOCK_BG_COLOR": (255, 255, 255, 100),  # only inside the clock
        "FRAME_HAS_NUMBERS": True,
        "FRAME_NUMBER_SHAPE": "rectangle", # "rectangle", "circle", "line"
        "FRAME_NUMBER_LENGTH": 20,
        "FRAME_NUMBER_THICKNESS": 4,
        "FRAME_NUMBER_COLOR": (200, 0, 0, 100),
        "FRAME_NUMBER_OFFSET": 10,
        "FRAME_NUMBER_RADIUS": 2,
        "FRAME_SPECIAL_NUMBERS": {
            3: {"length": None, "thickness": None, "color": None},
            6: {"length": None, "thickness": None, "color": None},
            9: {"length": None, "thickness": None, "color": None},
            12: {"length": None, "thickness": None, "color": None},
        },
        "FRAME_SIZE": 200,
    }
}

import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk

class App:
    def __init__(self):
        self.root = ThemedTk(theme="equilux")
        self.root.title("Dark Theme App")
        self.root.geometry("800x600")

        self.setup_ui()

    def setup_ui(self):
        # Main container
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        # Left section with tabs
        left_section = tk.Frame(main_container)
        left_section.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create notebook with tabs
        notebook = ttk.Notebook(left_section)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Tab 1
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text=" Frame ")
        label1 = ttk.Label(tab1, text="Hello", font=("Arial", 14))
        label1.pack(padx=20, pady=20)

        # Tab 2
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text=" Pointer ")
        label2 = ttk.Label(tab2, text="Goodbye", font=("Arial", 14))
        label2.pack(padx=20, pady=20)

        # Right section - 320px width
        self.right_section = tk.Frame(main_container, width=320, bg="gray20")
        self.right_section.pack(side=tk.RIGHT, fill=tk.Y)
        self.right_section.pack_propagate(False)  # Keep fixed width


        # Title label
        title_label = ttk.Label(
            self.right_section,
            text="Background Color",
            font=("Arial", 10)
        )
        title_label.pack(side=tk.TOP, anchor="nw", padx=5, pady=(5, 0))

        # Container for radio buttons
        radio_frame = tk.Frame(self.right_section, bg=self.right_section["bg"])
        radio_frame.pack(side=tk.TOP, anchor="nw", padx=5, pady=5)

        # Radio buttons for background color
        self.bg_color_var = tk.StringVar(value="gray20")
        colors = [("White", "white"), ("Black", "black"), ("Gray", "gray")]

        for text, color in colors:
            rb = ttk.Radiobutton(
                radio_frame,
                text=text,
                value=color,
                variable=self.bg_color_var,
                command=self.update_bg_color
            )
            rb.pack(side=tk.LEFT, padx=(0,5))

    def update_bg_color(self):
        color = self.bg_color_var.get()
        self.right_section.config(bg=color)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()