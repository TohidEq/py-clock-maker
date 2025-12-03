import tkinter as tk
from tkinter import ttk, colorchooser
from ttkthemes import ThemedTk

class App:
    def __init__(self):
        self.configs_dic = {
            "pointer": {
                "POINTER_SHAPE": "circle",
                "POINTER_SCALE": 4,
                "POINTER_START_AT": 80,
                "POINTER_LENGTH": 20,
                "POINTER_THICKNESS": 10,
                "POINTER_COLOR": (255, 0, 0, 150),
                "POINTER_ROUND_START": True,
                "POINTER_ROUND_END": True,
                "POINTER_SIZE": 200,
            },
            "frame": {
                "FRAME_SCALE": 4,
                "FRAME_CLOCK_PADDING": 10,
                "FRAME_HAS_BORDER": True,
                "FRAME_BORDER_RADIUS": 2,
                "FRAME_BORDER_COLOR": (0, 0, 0, 255),
                "FRAME_CLOCK_BG_COLOR": (255, 255, 255, 100),
                "FRAME_HAS_NUMBERS": True,
                "FRAME_NUMBER_SHAPE": "rectangle",
                "FRAME_NUMBER_LENGTH": 20,
                "FRAME_NUMBER_THICKNESS": 4,
                "FRAME_NUMBER_COLOR": (200, 0, 0, 100),
                "FRAME_NUMBER_OFFSET": 10,
                "FRAME_NUMBER_RADIUS": 2,
                "FRAME_SPECIAL_NUMBERS": {3:{},6:{},9:{},12:{}},
                "FRAME_SIZE": 200,
            }
        }

        self.root = ThemedTk(theme="equilux")
        self.root.title("Optimized Dark Theme App")
        self.root.geometry("1200x700")  # صفحه بزرگ‌تر
        self.setup_ui()

    def setup_ui(self):
        # Main container
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)

        # Left: Frame Controls (1/2)
        self.left_section = tk.Frame(main_container, width=600)
        self.left_section.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.left_section.pack_propagate(False)
        self.create_frame_controls(self.left_section)

        # Middle: Pointer Controls (1/4)
        self.middle_section = tk.Frame(main_container, width=300)
        self.middle_section.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.middle_section.pack_propagate(False)
        self.create_pointer_controls(self.middle_section)

        # Right: Background Color + Update (1/4)
        self.right_section = tk.Frame(main_container, width=300, bg="gray20")
        self.right_section.pack(side=tk.LEFT, fill=tk.Y)
        self.right_section.pack_propagate(False)

        # Right section contents
        title_label = ttk.Label(self.right_section, text="Background Color", font=("Arial", 10))
        title_label.pack(side=tk.TOP, anchor="nw", padx=5, pady=(5,0))

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






    def create_frame_controls(self, parent):
        self.frame_numeric_vars = {}
        numeric_settings = [
            ("FRAME_SCALE", "Frame Scale", 4),
            ("FRAME_CLOCK_PADDING", "Clock Padding", 10),
            ("FRAME_BORDER_RADIUS", "Border Radius", 2),
            ("FRAME_NUMBER_LENGTH", "Number Length", 20),
            ("FRAME_NUMBER_THICKNESS", "Number Thickness", 4),
            ("FRAME_NUMBER_OFFSET", "Number Offset", 10),
            ("FRAME_NUMBER_RADIUS", "Number Radius", 2),
        ]
        for key,label,default in numeric_settings:
            self.create_numeric_control_frame(parent, key, label, default)

        # Booleans
        self.has_border_var = tk.BooleanVar(value=self.configs_dic["frame"]["FRAME_HAS_BORDER"])
        tk.Checkbutton(parent, text="Has Border", variable=self.has_border_var).pack(anchor="w")
        self.has_numbers_var = tk.BooleanVar(value=self.configs_dic["frame"]["FRAME_HAS_NUMBERS"])
        tk.Checkbutton(parent, text="Has Numbers", variable=self.has_numbers_var).pack(anchor="w")

        # Number Shape
        self.number_shape_var = tk.StringVar(value=self.configs_dic["frame"]["FRAME_NUMBER_SHAPE"])
        ttk.Combobox(parent, textvariable=self.number_shape_var,
                     values=["rectangle","circle","line"], state="readonly").pack(pady=5)

        # Colors
        self.number_color_preview = tk.Frame(parent, height=30,
                                             bg=self.rgb_to_hex(self.configs_dic["frame"]["FRAME_NUMBER_COLOR"][:3]))
        self.number_color_preview.pack(fill="x", pady=2)

        tk.Button(parent, text="Pick Number Color",
                  command=lambda:self.pick_frame_color("FRAME_NUMBER_COLOR", self.number_color_preview)).pack(pady=2)

    # Pointer Controls
    def create_pointer_controls(self, parent):
        self.numeric_vars = {}
        self.shape_var = tk.StringVar(value=self.configs_dic["pointer"]["POINTER_SHAPE"])
        ttk.Combobox(parent, textvariable=self.shape_var,
                     values=["line","circle"], state="readonly").pack(pady=5)

        numeric_settings = [
            ("POINTER_SCALE","Scale",4),
            ("POINTER_START_AT","Start At",80),
            ("POINTER_LENGTH","Length",20),
            ("POINTER_THICKNESS","Thickness",10),
            ("POINTER_SIZE","Pointer Size",200)
        ]
        for key,label,default in numeric_settings:
            self.create_numeric_control(parent,key,label,default)

        # Round start/end
        self.round_start_var = tk.BooleanVar(value=self.configs_dic["pointer"]["POINTER_ROUND_START"])
        tk.Checkbutton(parent,text="Round Start",variable=self.round_start_var).pack(anchor="w")
        self.round_end_var = tk.BooleanVar(value=self.configs_dic["pointer"]["POINTER_ROUND_END"])
        tk.Checkbutton(parent,text="Round End",variable=self.round_end_var).pack(anchor="w")

        # Color
        self.color_preview = tk.Frame(parent, height=30,
                                      bg=self.rgb_to_hex(self.configs_dic["pointer"]["POINTER_COLOR"][:3]))
        self.color_preview.pack(fill="x", pady=2)
        tk.Button(parent,text="Pick RGB Color",command=self.pick_color).pack(pady=2)

    # Numeric controls
    def create_numeric_control_frame(self,parent,key,label,default):
        frame = tk.Frame(parent)
        frame.pack(fill="x", pady=2)
        tk.Label(frame,text=label+":", width=20).pack(side="left")
        var = tk.DoubleVar(value=default)
        self.frame_numeric_vars[key] = var
        tk.Entry(frame,textvariable=var,width=10).pack(side="left")

    def create_numeric_control(self,parent,key,label,default):
        frame = tk.Frame(parent)
        frame.pack(fill="x", pady=2)
        tk.Label(frame,text=label+":", width=15).pack(side="left")
        var = tk.DoubleVar(value=default)
        self.numeric_vars[key] = var
        tk.Entry(frame,textvariable=var,width=10).pack(side="left")

    # Colors
    def pick_color(self):
        color = colorchooser.askcolor(title="Pick RGB Color",
                                     initialcolor=self.rgb_to_hex(self.configs_dic["pointer"]["POINTER_COLOR"][:3]))
        if color[0]:
            r,g,b = map(int,color[0])
            self.color_preview.config(bg=self.rgb_to_hex((r,g,b)))

    def pick_frame_color(self,color_key,preview_widget):
        color = colorchooser.askcolor(title=f"Pick {color_key} Color",
                                     initialcolor=self.rgb_to_hex(self.configs_dic["frame"][color_key][:3]))
        if color[0]:
            r,g,b = map(int,color[0])
            preview_widget.config(bg=self.rgb_to_hex((r,g,b)))

    def update_all_values(self):
        # Pointer
        self.configs_dic["pointer"]["POINTER_SHAPE"] = self.shape_var.get()
        for key,var in self.numeric_vars.items():
            self.configs_dic["pointer"][key] = var.get()
        self.configs_dic["pointer"]["POINTER_ROUND_START"] = self.round_start_var.get()
        self.configs_dic["pointer"]["POINTER_ROUND_END"] = self.round_end_var.get()
        hex_color = self.color_preview.cget("bg").lstrip('#')
        r=int(hex_color[0:2],16); g=int(hex_color[2:4],16); b=int(hex_color[4:6],16)
        self.configs_dic["pointer"]["POINTER_COLOR"] = (r,g,b,150)

        # Frame
        for key,var in self.frame_numeric_vars.items():
            self.configs_dic["frame"][key] = var.get()
        self.configs_dic["frame"]["FRAME_HAS_BORDER"] = self.has_border_var.get()
        self.configs_dic["frame"]["FRAME_HAS_NUMBERS"] = self.has_numbers_var.get()
        self.configs_dic["frame"]["FRAME_NUMBER_SHAPE"] = self.number_shape_var.get()
        hex_color = self.number_color_preview.cget("bg").lstrip('#')
        r=int(hex_color[0:2],16); g=int(hex_color[2:4],16); b=int(hex_color[4:6],16)
        self.configs_dic["frame"]["FRAME_NUMBER_COLOR"] = (r,g,b,150)
        # print("Updated configs:", self.configs_dic)

    def rgb_to_hex(self,rgb):
        return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'

    def update_bg_color(self):
        color = self.bg_color_var.get()
        self.right_section.config(bg=color)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()