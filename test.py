import tkinter as tk
from tkinter import ttk, colorchooser
from ttkthemes import ThemedTk

class App:
    def __init__(self):
        self.configs_dic = {
            "pointer": {
                "POINTER_SHAPE": "circle",
                "POINTER_SCALE": 4.0,
                "POINTER_START_AT": 80.0,
                "POINTER_LENGTH": 20.0,
                "POINTER_THICKNESS": 10.0,
                "POINTER_COLOR": (255, 0, 0, 150),
                "POINTER_ROUND_START": True,
                "POINTER_ROUND_END": True,
                "POINTER_SIZE": 200,
            },
            "frame": {
                "FRAME_SCALE": 4.0,
                "FRAME_CLOCK_PADDING": 10.0,
                "FRAME_HAS_BORDER": True,
                "FRAME_BORDER_RADIUS": 2.0,
                "FRAME_BORDER_COLOR": (0, 0, 0, 255),
                "FRAME_CLOCK_BG_COLOR": (255, 255, 255, 100),
                "FRAME_HAS_NUMBERS": True,
                "FRAME_NUMBER_SHAPE": "rectangle",
                "FRAME_NUMBER_LENGTH": 20.0,
                "FRAME_NUMBER_THICKNESS": 4.0,
                "FRAME_NUMBER_COLOR": (200, 0, 0, 100),
                "FRAME_NUMBER_OFFSET": 10.0,
                "FRAME_NUMBER_RADIUS": 2.0,
                "FRAME_SPECIAL_NUMBERS": {
                    3: {"length": None, "thickness": None, "color": None},
                    6: {"length": None, "thickness": None, "color": None},
                    9: {"length": None, "thickness": None, "color": None},
                    12: {"length": None, "thickness": None, "color": None},
                },
                "FRAME_SIZE": 200,
            }
        }

        self.root = ThemedTk(theme="arc")
        self.root.title("Dark Theme App")
        self.root.geometry("1280x800")
        self.setup_ui()

    def setup_ui(self):
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        left_section = tk.Frame(main_container)
        left_section.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        notebook = ttk.Notebook(left_section)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Tab 1 (Frame)
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text=" Frame ")
        self.create_frame_controls(tab1)

        # Tab 2 (Pointer)
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text=" Pointer ")
        self.create_pointer_controls(tab2)

        # Right Section
        self.right_section = tk.Frame(main_container, width=320, bg="gray20")
        self.right_section.pack(side=tk.RIGHT, fill=tk.Y)
        self.right_section.pack_propagate(False)

        title_label = ttk.Label(
            self.right_section,
            text="Background Color",
            font=("Arial", 10)
        )
        title_label.pack(side=tk.TOP, anchor="nw", padx=5, pady=(5, 0))

        radio_frame = tk.Frame(self.right_section, bg=self.right_section["bg"])
        radio_frame.pack(side=tk.TOP, anchor="nw", padx=5, pady=5)

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

        update_btn = ttk.Button(
            self.right_section,
            text="Update Values",
            command=self.update_all_values
        )
        update_btn.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=10)

    def create_pointer_controls(self, parent):
        # Main container for pointer controls
        main_frame = tk.Frame(parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left column for controls before Pointer Options
        left_column = tk.Frame(main_frame)
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Right column for Pointer Options and below
        right_column = tk.Frame(main_frame)
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Left Column Controls
        shape_frame = ttk.LabelFrame(left_column, text="Pointer Shape", padding=10)
        shape_frame.pack(fill="x", padx=5, pady=5)

        self.shape_var = tk.StringVar(value=self.configs_dic["pointer"]["POINTER_SHAPE"])
        shape_combobox = ttk.Combobox(shape_frame, textvariable=self.shape_var,
                                      values=["line", "circle"], state="readonly", width=15)
        shape_combobox.pack(pady=5)

        # Numeric controls in left column
        numeric_settings = [
            ("POINTER_SCALE", "Scale", 4.0),
            ("POINTER_START_AT", "Start At (px)", 80.0),
            ("POINTER_LENGTH", "Length/Radius", 20.0),
            ("POINTER_THICKNESS", "Thickness", 10.0),
        ]

        self.numeric_vars = {}
        for key, label, default in numeric_settings:
            self.create_numeric_control(left_column, key, label, default)

        # Color controls in left column
        color_frame = ttk.LabelFrame(left_column, text="Pointer Color", padding=10)
        color_frame.pack(fill="x", padx=5, pady=5)

        self.color_preview = tk.Frame(color_frame, height=30,
                                      bg=self.rgb_to_hex(self.configs_dic["pointer"]["POINTER_COLOR"][:3]))
        self.color_preview.pack(fill="x", pady=(0, 5))

        color_btn = ttk.Button(color_frame, text="Pick RGB Color",
                               command=self.pick_color)
        color_btn.pack(pady=5)

        alpha_frame = ttk.Frame(color_frame)
        alpha_frame.pack(fill="x", pady=5)

        ttk.Label(alpha_frame, text="Alpha:").pack(side="left", padx=(0, 5))

        self.alpha_var = tk.IntVar(value=self.configs_dic["pointer"]["POINTER_COLOR"][3])
        alpha_slider = ttk.Scale(alpha_frame, from_=0, to=255, variable=self.alpha_var,
                                command=lambda v: self.update_alpha(int(float(v))))
        alpha_slider.pack(side="left", fill="x", expand=True, padx=5)

        self.alpha_label = ttk.Label(alpha_frame, text=str(self.alpha_var.get()), width=3)
        self.alpha_label.pack(side="right")

        # Right Column Controls (Pointer Options and below)
        bool_frame = ttk.LabelFrame(right_column, text="Pointer Options", padding=10)
        bool_frame.pack(fill="x", padx=5, pady=5)

        self.round_start_var = tk.BooleanVar(value=self.configs_dic["pointer"]["POINTER_ROUND_START"])
        round_start_cb = ttk.Checkbutton(bool_frame, text="Round Start",
                                        variable=self.round_start_var)
        round_start_cb.pack(anchor="w", pady=2)

        self.round_end_var = tk.BooleanVar(value=self.configs_dic["pointer"]["POINTER_ROUND_END"])
        round_end_cb = ttk.Checkbutton(bool_frame, text="Round End",
                                      variable=self.round_end_var)
        round_end_cb.pack(anchor="w", pady=2)

        # Pointer Size in right column
        self.create_integer_control(right_column, "POINTER_SIZE", "Pointer Size", 200)

    def create_frame_controls(self, parent):
        # Main container for frame controls
        main_frame = tk.Frame(parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left column for controls before Numbers section
        left_column = tk.Frame(main_frame)
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Right column for Numbers section and below
        right_column = tk.Frame(main_frame)
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Left Column Controls
        self.create_numeric_control_frame(left_column, "FRAME_SCALE", "Frame Scale", 4.0)
        self.create_numeric_control_frame(left_column, "FRAME_CLOCK_PADDING", "Clock Padding", 10.0)

        # Has Border checkbox
        bool_frame1 = ttk.LabelFrame(left_column, text="Frame Border", padding=10)
        bool_frame1.pack(fill="x", padx=5, pady=5)

        self.has_border_var = tk.BooleanVar(value=self.configs_dic["frame"]["FRAME_HAS_BORDER"])
        has_border_cb = ttk.Checkbutton(bool_frame1, text="Has Border",
                                        variable=self.has_border_var)
        has_border_cb.pack(anchor="w", pady=2)

        self.create_numeric_control_frame(left_column, "FRAME_BORDER_RADIUS", "Border Radius", 2.0)

        # Border Color
        border_color_frame = ttk.LabelFrame(left_column, text="Border Color", padding=10)
        border_color_frame.pack(fill="x", padx=5, pady=5)

        self.border_color_preview = tk.Frame(border_color_frame, height=30,
                                            bg=self.rgb_to_hex(self.configs_dic["frame"]["FRAME_BORDER_COLOR"][:3]))
        self.border_color_preview.pack(fill="x", pady=(0, 5))

        border_color_btn = ttk.Button(border_color_frame, text="Pick Border Color",
                                     command=lambda: self.pick_frame_color("FRAME_BORDER_COLOR", self.border_color_preview))
        border_color_btn.pack(pady=5)

        self.border_alpha_var = tk.IntVar(value=self.configs_dic["frame"]["FRAME_BORDER_COLOR"][3])
        border_alpha_frame = ttk.Frame(border_color_frame)
        border_alpha_frame.pack(fill="x", pady=5)

        ttk.Label(border_alpha_frame, text="Alpha:").pack(side="left", padx=(0, 5))

        border_alpha_slider = ttk.Scale(border_alpha_frame, from_=0, to=255,
                                       variable=self.border_alpha_var,
                                       command=lambda v: self.update_frame_alpha("FRAME_BORDER_COLOR", self.border_color_preview, int(float(v))))
        border_alpha_slider.pack(side="left", fill="x", expand=True, padx=5)

        self.border_alpha_label = ttk.Label(border_alpha_frame, text=str(self.border_alpha_var.get()), width=3)
        self.border_alpha_label.pack(side="right")

        # Clock BG Color
        bg_color_frame = ttk.LabelFrame(left_column, text="Clock Background Color", padding=10)
        bg_color_frame.pack(fill="x", padx=5, pady=5)

        self.bg_color_preview = tk.Frame(bg_color_frame, height=30,
                                        bg=self.rgb_to_hex(self.configs_dic["frame"]["FRAME_CLOCK_BG_COLOR"][:3]))
        self.bg_color_preview.pack(fill="x", pady=(0, 5))

        bg_color_btn = ttk.Button(bg_color_frame, text="Pick BG Color",
                                 command=lambda: self.pick_frame_color("FRAME_CLOCK_BG_COLOR", self.bg_color_preview))
        bg_color_btn.pack(pady=5)

        self.bg_alpha_var = tk.IntVar(value=self.configs_dic["frame"]["FRAME_CLOCK_BG_COLOR"][3])
        bg_alpha_frame = ttk.Frame(bg_color_frame)
        bg_alpha_frame.pack(fill="x", pady=5)

        ttk.Label(bg_alpha_frame, text="Alpha:").pack(side="left", padx=(0, 5))

        bg_alpha_slider = ttk.Scale(bg_alpha_frame, from_=0, to=255,
                                   variable=self.bg_alpha_var,
                                   command=lambda v: self.update_frame_alpha("FRAME_CLOCK_BG_COLOR", self.bg_color_preview, int(float(v))))
        bg_alpha_slider.pack(side="left", fill="x", expand=True, padx=5)

        self.bg_alpha_label = ttk.Label(bg_alpha_frame, text=str(self.bg_alpha_var.get()), width=3)
        self.bg_alpha_label.pack(side="right")

        # Right Column Controls (Numbers section and below)
        # Has Numbers checkbox
        bool_frame2 = ttk.LabelFrame(right_column, text="Numbers", padding=10)
        bool_frame2.pack(fill="x", padx=5, pady=5)

        self.has_numbers_var = tk.BooleanVar(value=self.configs_dic["frame"]["FRAME_HAS_NUMBERS"])
        has_numbers_cb = ttk.Checkbutton(bool_frame2, text="Has Numbers",
                                         variable=self.has_numbers_var)
        has_numbers_cb.pack(anchor="w", pady=2)

        # Number Shape
        shape_frame = ttk.LabelFrame(right_column, text="Number Shape", padding=10)
        shape_frame.pack(fill="x", padx=5, pady=5)

        self.number_shape_var = tk.StringVar(value=self.configs_dic["frame"]["FRAME_NUMBER_SHAPE"])
        shape_combobox = ttk.Combobox(shape_frame, textvariable=self.number_shape_var,
                                      values=["rectangle", "circle", "line"], state="readonly", width=15)
        shape_combobox.pack(pady=5)

        # Number controls in right column
        self.create_numeric_control_frame(right_column, "FRAME_NUMBER_LENGTH", "Number Length", 20.0)
        self.create_numeric_control_frame(right_column, "FRAME_NUMBER_THICKNESS", "Number Thickness", 4.0)

        # Number Color
        number_color_frame = ttk.LabelFrame(right_column, text="Number Color", padding=10)
        number_color_frame.pack(fill="x", padx=5, pady=5)

        self.number_color_preview = tk.Frame(number_color_frame, height=30,
                                            bg=self.rgb_to_hex(self.configs_dic["frame"]["FRAME_NUMBER_COLOR"][:3]))
        self.number_color_preview.pack(fill="x", pady=(0, 5))

        number_color_btn = ttk.Button(number_color_frame, text="Pick Number Color",
                                     command=lambda: self.pick_frame_color("FRAME_NUMBER_COLOR", self.number_color_preview))
        number_color_btn.pack(pady=5)

        self.number_alpha_var = tk.IntVar(value=self.configs_dic["frame"]["FRAME_NUMBER_COLOR"][3])
        number_alpha_frame = ttk.Frame(number_color_frame)
        number_alpha_frame.pack(fill="x", pady=5)

        ttk.Label(number_alpha_frame, text="Alpha:").pack(side="left", padx=(0, 5))

        number_alpha_slider = ttk.Scale(number_alpha_frame, from_=0, to=255,
                                       variable=self.number_alpha_var,
                                       command=lambda v: self.update_frame_alpha("FRAME_NUMBER_COLOR", self.number_color_preview, int(float(v))))
        number_alpha_slider.pack(side="left", fill="x", expand=True, padx=5)

        self.number_alpha_label = ttk.Label(number_alpha_frame, text=str(self.number_alpha_var.get()), width=3)
        self.number_alpha_label.pack(side="right")

        # More number controls in right column
        self.create_numeric_control_frame(right_column, "FRAME_NUMBER_OFFSET", "Number Offset", 10.0)
        self.create_numeric_control_frame(right_column, "FRAME_NUMBER_RADIUS", "Number Radius", 2.0)

        # Frame Size (integer) in right column
        self.create_integer_control_frame(right_column, "FRAME_SIZE", "Frame Size", 200)

    def create_numeric_control(self, parent, config_key, label_text, default_value):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(frame, text=label_text + ":", width=20).pack(side="left")

        var = tk.DoubleVar(value=default_value)
        self.numeric_vars[config_key] = var

        minus_btn = ttk.Button(frame, text="-", width=3,
                              command=lambda: self.adjust_numeric(config_key, -0.1))
        minus_btn.pack(side="left", padx=(0, 5))

        entry = ttk.Entry(frame, textvariable=var, width=10)
        entry.pack(side="left")

        plus_btn = ttk.Button(frame, text="+", width=3,
                             command=lambda: self.adjust_numeric(config_key, 0.1))
        plus_btn.pack(side="left", padx=(5, 0))

    def create_numeric_control_frame(self, parent, config_key, label_text, default_value):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(frame, text=label_text + ":", width=25).pack(side="left")

        var = tk.DoubleVar(value=default_value)
        if not hasattr(self, 'frame_numeric_vars'):
            self.frame_numeric_vars = {}
        self.frame_numeric_vars[config_key] = var

        minus_btn = ttk.Button(frame, text="-", width=3,
                              command=lambda: self.adjust_numeric_frame(config_key, -0.1))
        minus_btn.pack(side="left", padx=(0, 5))

        entry = ttk.Entry(frame, textvariable=var, width=10)
        entry.pack(side="left")

        plus_btn = ttk.Button(frame, text="+", width=3,
                             command=lambda: self.adjust_numeric_frame(config_key, 0.1))
        plus_btn.pack(side="left", padx=(5, 0))

    def create_integer_control_frame(self, parent, config_key, label_text, default_value):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(frame, text=label_text + ":", width=25).pack(side="left")

        var = tk.IntVar(value=default_value)
        if not hasattr(self, 'frame_numeric_vars'):
            self.frame_numeric_vars = {}
        self.frame_numeric_vars[config_key] = var

        minus_btn = ttk.Button(frame, text="-", width=3,
                              command=lambda: self.adjust_integer_frame(config_key, -1))
        minus_btn.pack(side="left", padx=(0, 5))

        entry = ttk.Entry(frame, textvariable=var, width=10)
        entry.pack(side="left")

        plus_btn = ttk.Button(frame, text="+", width=3,
                             command=lambda: self.adjust_integer_frame(config_key, 1))
        plus_btn.pack(side="left", padx=(5, 0))

    def adjust_numeric_frame(self, config_key, delta):
        current = self.frame_numeric_vars[config_key].get()
        new_value = round(current + delta, 1)
        self.frame_numeric_vars[config_key].set(new_value)

    def adjust_integer_frame(self, config_key, delta):
        current = self.frame_numeric_vars[config_key].get()
        new_value = current + delta
        self.frame_numeric_vars[config_key].set(new_value)

    def pick_frame_color(self, color_key, preview_widget):
        current_color = self.configs_dic["frame"][color_key][:3]
        color = colorchooser.askcolor(title=f"Pick {color_key} Color",
                                     initialcolor=self.rgb_to_hex(current_color))
        if color[0]:
            r, g, b = [int(c) for c in color[0]]
            preview_widget.config(bg=self.rgb_to_hex((r, g, b)))

    def update_frame_alpha(self, color_key, preview_widget, alpha):
        if color_key == "FRAME_BORDER_COLOR":
            self.border_alpha_label.config(text=str(alpha))
        elif color_key == "FRAME_CLOCK_BG_COLOR":
            self.bg_alpha_label.config(text=str(alpha))
        elif color_key == "FRAME_NUMBER_COLOR":
            self.number_alpha_label.config(text=str(alpha))

    def create_integer_control(self, parent, config_key, label_text, default_value):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(frame, text=label_text + ":", width=20).pack(side="left")

        var = tk.IntVar(value=default_value)
        self.numeric_vars[config_key] = var

        minus_btn = ttk.Button(frame, text="-", width=3,
                              command=lambda: self.adjust_integer(config_key, -1))
        minus_btn.pack(side="left", padx=(0, 5))

        entry = ttk.Entry(frame, textvariable=var, width=10)
        entry.pack(side="left")

        plus_btn = ttk.Button(frame, text="+", width=3,
                             command=lambda: self.adjust_integer(config_key, 1))
        plus_btn.pack(side="left", padx=(5, 0))

    def adjust_numeric(self, config_key, delta):
        current = self.numeric_vars[config_key].get()
        new_value = round(current + delta, 1)
        self.numeric_vars[config_key].set(new_value)

    def adjust_integer(self, config_key, delta):
        current = self.numeric_vars[config_key].get()
        new_value = current + delta
        self.numeric_vars[config_key].set(new_value)

    def pick_color(self):
        color = colorchooser.askcolor(title="Pick RGB Color",
                                     initialcolor=self.rgb_to_hex(self.configs_dic["pointer"]["POINTER_COLOR"][:3]))
        if color[0]:
            r, g, b = [int(c) for c in color[0]]
            self.color_preview.config(bg=self.rgb_to_hex((r, g, b)))

    def update_alpha(self, alpha):
        self.alpha_label.config(text=str(alpha))
        self.alpha_var.set(alpha)

    def update_all_values(self):
        # Update Pointer values
        self.configs_dic["pointer"]["POINTER_SHAPE"] = self.shape_var.get()

        for key, var in self.numeric_vars.items():
            self.configs_dic["pointer"][key] = var.get()

        self.configs_dic["pointer"]["POINTER_ROUND_START"] = self.round_start_var.get()
        self.configs_dic["pointer"]["POINTER_ROUND_END"] = self.round_end_var.get()

        # Get color from preview
        hex_color = self.color_preview.cget("bg")
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        a = self.alpha_var.get()
        self.configs_dic["pointer"]["POINTER_COLOR"] = (r, g, b, a)

        # Update Frame values
        if hasattr(self, 'frame_numeric_vars'):
            for key, var in self.frame_numeric_vars.items():
                self.configs_dic["frame"][key] = var.get()

        if hasattr(self, 'has_border_var'):
            self.configs_dic["frame"]["FRAME_HAS_BORDER"] = self.has_border_var.get()

        if hasattr(self, 'has_numbers_var'):
            self.configs_dic["frame"]["FRAME_HAS_NUMBERS"] = self.has_numbers_var.get()

        if hasattr(self, 'number_shape_var'):
            self.configs_dic["frame"]["FRAME_NUMBER_SHAPE"] = self.number_shape_var.get()

        # Update Frame colors
        if hasattr(self, 'border_color_preview'):
            hex_color = self.border_color_preview.cget("bg")
            hex_color = hex_color.lstrip('#')
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            a = self.border_alpha_var.get()
            self.configs_dic["frame"]["FRAME_BORDER_COLOR"] = (r, g, b, a)

        if hasattr(self, 'bg_color_preview'):
            hex_color = self.bg_color_preview.cget("bg")
            hex_color = hex_color.lstrip('#')
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            a = self.bg_alpha_var.get()
            self.configs_dic["frame"]["FRAME_CLOCK_BG_COLOR"] = (r, g, b, a)

        if hasattr(self, 'number_color_preview'):
            hex_color = self.number_color_preview.cget("bg")
            hex_color = hex_color.lstrip('#')
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            a = self.number_alpha_var.get()
            self.configs_dic["frame"]["FRAME_NUMBER_COLOR"] = (r, g, b, a)

        print("Updated all values:")
        print("Pointer:", self.configs_dic["pointer"])
        print("Frame:", self.configs_dic["frame"])

    def rgb_to_hex(self, rgb):
        return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'

    def update_bg_color(self):
        color = self.bg_color_var.get()
        self.right_section.config(bg=color)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()