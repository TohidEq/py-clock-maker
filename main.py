import math
import tkinter as tk
from tkinter import ttk, colorchooser
from ttkthemes import ThemedTk
from PIL import Image, ImageDraw, ImageTk
from IPython.display import display


from draw_frame import draw_frame
from draw_pointer import draw_pointer

from export_images import export_frame, export_pointer

import config

class App:
    def __init__(self):
        self.img_config_dic=config.img_config_dic
        self.configs_dic = config.configs_dic
        self.root = ThemedTk(theme=config.WINDOW_THEME)
        self.root.title(config.WINDOW_TITLE)
        self.root.geometry(config.WINDOW_SIZE)
        self.img_labels = []
        self.setup_ui()


    def convert_float_values_to_ints(self):

        def _convert(x):
            if isinstance(x, dict):
                return {k: _convert(v) for k, v in x.items()}
            elif isinstance(x, list):
                return [_convert(i) for i in x]
            elif isinstance(x, tuple):
                return tuple(_convert(i) for i in x)
            elif isinstance(x, float):
                return int(x)
            return x

        self.configs_dic = _convert(self.configs_dic)

    def add_image_section(self):
        """Add image section to right panel"""
        # Separator
        ttk.Separator(self.right_section, orient='horizontal').pack(fill='x', pady=10)

        # Title for image section
        preview_title = ttk.Label(
            self.right_section,
            text="Preview Images",
            font=("Arial", 11, "bold")
        )
        preview_title.pack(anchor="nw", padx=5, pady=(0, 10))

        # Container for images
        images_container = tk.Frame(self.right_section, bg=self.right_section["bg"])
        images_container.pack(fill=tk.BOTH, expand=True, padx=5)

        # Create two image labels
        for i in range(2):
            frame = ttk.LabelFrame(images_container, text=f"Image {i+1}", padding=5)
            frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

            # Create label for image
            img_label = ttk.Label(frame)
            img_label.pack(pady=5)
            self.img_labels.append(img_label)

        # Display default images

        self.update_images()




    def show_placeholder_images(self):
        """Show placeholder images if draw functions fail"""

        # عکس placeholder اول
        img1 = Image.new('RGB', (280, 200), color='lightblue')
        draw = ImageDraw.Draw(img1)
        draw.rectangle([20, 20, 260, 180], outline='blue', width=2)
        draw.text((140, 100), "Frame Preview", fill='black', anchor='mm')

        # عکس placeholder دوم
        img2 = Image.new('RGB', (280, 200), color='lightgreen')
        draw = ImageDraw.Draw(img2)
        draw.ellipse([50, 50, 230, 150], outline='green', width=2)
        draw.text((140, 100), "Pointer Preview", fill='black', anchor='mm')

        # تبدیل به PhotoImage
        photo1 = ImageTk.PhotoImage(img1)
        photo2 = ImageTk.PhotoImage(img2)

        # نمایش در لیبل‌ها
        if len(self.img_labels) >= 2:
            self.img_labels[0].config(image=photo1)
            self.img_labels[1].config(image=photo2)

            # نگهداری رفرنس
            self.img_labels[0].image = photo1
            self.img_labels[1].image = photo2



    def pil_to_tk(self, pil_img, width=200, height=200, bg_color=None):
        """Convert transparent PIL image to Tk-compatible image"""

        pil_img = pil_img.resize((width, height), Image.Resampling.LANCZOS)

        # Tkinter cannot display real transparency → composite needed
        if pil_img.mode == "RGBA":
            if bg_color is None:
                bg_color = self.bg_color_var.get()  #ui background
                # print(self.bg_color_var.get())
                # print(self.bg_color_var.get())
                # print(self.bg_color_var.get())
                # print(self.bg_color_var.get())
            background = Image.new("RGB", pil_img.size, bg_color)
            background.paste(pil_img, mask=pil_img.split()[3])  # use alpha channel
            pil_img = background

        return ImageTk.PhotoImage(pil_img)


    def update_images(self):
        try:
            # -------- Frame image (PIL) --------
            img1_pil = draw_frame(self.configs_dic)  # ← این PIL می‌سازه
            img1 = self.pil_to_tk(img1_pil)

            # -------- Pointer image (PIL) --------
            import random
            pos = random.randint(0, 60)
            img2_pil = draw_pointer(pos, self.configs_dic)  # ← اینم PIL
            img2 = self.pil_to_tk(img2_pil)

            # نمایش در لیبل‌ها
            if len(self.img_labels) >= 2:
                self.img_labels[0].config(image=img1)
                self.img_labels[1].config(image=img2)

                # نگهداری رفرنس
                self.img_labels[0].image = img1
                self.img_labels[1].image = img2

        except Exception as e:
            # print(f"Error updating images: {e}")
            self.show_placeholder_images()

    def export_frame_images(self):
        export_frame(configs_dic = self.configs_dic,
            base_dir = self.img_config_dic["BASE_DIR"],
            frame_dir = self.img_config_dic["FRAME_DIR"])


    def export_h_images(self):
        export_pointer(configs_dic = self.configs_dic,
            hms="h",
            base_dir = self.img_config_dic["BASE_DIR"],
            pointer_dir = self.img_config_dic["POINTER_DIR"],
            save_dir = self.img_config_dic["H_POINTER_DIR"])

    def export_m_images(self):
        export_pointer(configs_dic = self.configs_dic,
            hms="m",
            base_dir = self.img_config_dic["BASE_DIR"],
            pointer_dir = self.img_config_dic["POINTER_DIR"],
            save_dir = self.img_config_dic["M_POINTER_DIR"])

    def export_s_images(self):
        export_pointer(configs_dic = self.configs_dic,
            hms="s",
            base_dir = self.img_config_dic["BASE_DIR"],
            pointer_dir = self.img_config_dic["POINTER_DIR"],
            save_dir = self.img_config_dic["S_POINTER_DIR"])



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

        # Tab 2 (Special Numbers)
        tab3 = ttk.Frame(notebook)
        notebook.add(tab3, text=" Special Numbers ")
        self.create_special_numbers_controls(tab3)

        # Tab 3 (Pointer)
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text=" Pointer ")
        self.create_pointer_controls(tab2)



        # Right Section
        self.right_section = tk.Frame(main_container, width=320, bg="#F5F6F7")
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

        self.bg_color_var = tk.StringVar(value="white")
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




        # Frame for time buttons
        time_btn_frame = ttk.Frame(self.right_section)
        time_btn_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=6, pady=10)

        # Title for image section
        preview_title = ttk.Label(
            self.right_section,
            text="   Export Images:",
            font=("Arial", 11, "bold")
        )
        preview_title.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=2)


        btn_width = 6

        frame_btn = ttk.Button(
            time_btn_frame,
            text="Frame",
            command=self.export_frame_images,
            width=btn_width
        )
        frame_btn.grid(row=0, column=0, padx=2)

        hh_btn = ttk.Button(
            time_btn_frame,
            text="H",
            command=self.export_h_images,
            width=btn_width
        )
        hh_btn.grid(row=0, column=1, padx=2)

        mm_btn = ttk.Button(
            time_btn_frame,
            text="M",
            command=self.export_m_images,
            width=btn_width
        )
        mm_btn.grid(row=0, column=2, padx=2)

        ss_btn = ttk.Button(
            time_btn_frame,
            text="S",
            command=self.export_s_images,
            width=btn_width
        )
        ss_btn.grid(row=0, column=3, padx=2)

        preview_btn= ttk.Button(
            self.right_section,
            text="Update Preview",
            command=self.update_all_values
        )
        preview_btn.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=10)
        self.add_image_section()


    def create_special_numbers_controls(self, parent):


          # Main container for special numbers controls
        main_frame = tk.Frame(parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create a container with two columns
        columns_container = tk.Frame(main_frame)
        columns_container.pack(fill=tk.BOTH, expand=True)

        # Left column for 12 and 3
        left_column = tk.Frame(columns_container)
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # Right column for 6 and 9
        right_column = tk.Frame(columns_container)
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        #000000
        # Create controls for each special number (3, 6, 9, 12)
        special_numbers = [3, 6, 9, 12]

        # Create variables for special numbers if they don't exist
        if not hasattr(self, 'special_numbers_vars'):
            self.special_numbers_vars = {}

        # for num in special_numbers:
            # self.create_special_number_control(main_frame, num)

        self.create_special_number_control(left_column, 12)
        self.create_special_number_control(left_column, 3)

        # Column 2: 6 and 9 (vertically stacked)
        self.create_special_number_control(right_column, 6)
        self.create_special_number_control(right_column, 9)

        # Separator

        # Separator
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=20)

        # Apply to all button
        apply_all_btn = ttk.Label(main_frame, text="The (-1) is same as normal numbers value")
        apply_all_btn.pack(pady=10)





    def create_special_number_control(self, parent, number):
        """Create controls for one special number"""
        frame = ttk.LabelFrame(parent, text=f"Number {number}", padding=10)
        frame.pack(fill="x", padx=5, pady=10)

        # Initialize variables for this number if they don't exist
        if number not in self.special_numbers_vars:
            # Get color value (could be tuple like (255,255,255,100))
            color_value = self.configs_dic["frame"]["FRAME_SPECIAL_NUMBERS"][number]["color"] or \
                        self.configs_dic["frame"]["FRAME_NUMBER_COLOR"]

            # Convert to list and ensure we have 4 values (RGBA)
            if isinstance(color_value, tuple):
                color_list = list(color_value)
            else:
                color_list = list(color_value)

            # If color has only 3 values (RGB), add alpha (255 = fully opaque)
            if len(color_list) == 3:
                color_list.append(255)
            elif len(color_list) < 3:
                # Fallback to white with full opacity
                color_list = [255, 255, 255, 255]

            self.special_numbers_vars[number] = {
                "length": tk.DoubleVar(value=self.configs_dic["frame"]["FRAME_SPECIAL_NUMBERS"][number]["length"] or
                                    self.configs_dic["frame"]["FRAME_NUMBER_LENGTH"]),
                "thickness": tk.DoubleVar(value=self.configs_dic["frame"]["FRAME_SPECIAL_NUMBERS"][number]["thickness"] or
                                        self.configs_dic["frame"]["FRAME_NUMBER_THICKNESS"]),
                "color": color_list  # Now this is a list [R, G, B, A]
            }

        # Length control
        length_frame = ttk.Frame(frame)
        length_frame.pack(fill="x", pady=5)

        ttk.Label(length_frame, text="Length:", width=8).pack(side="left")

        var = self.special_numbers_vars[number]["length"]

        minus_btn = ttk.Button(length_frame, text="-", width=3,
                            command=lambda: self.adjust_special_number_value(number, "length", -1))
        minus_btn.pack(side="left", padx=(0, 5))

        entry = ttk.Entry(length_frame, textvariable=var, width=10)
        entry.pack(side="left")

        plus_btn = ttk.Button(length_frame, text="+", width=3,
                            command=lambda: self.adjust_special_number_value(number, "length", 1))
        plus_btn.pack(side="left", padx=(5, 0))

        # Thickness control
        thickness_frame = ttk.Frame(frame)
        thickness_frame.pack(fill="x", pady=5)

        ttk.Label(thickness_frame, text="Thickness:", width=8).pack(side="left")

        var_thickness = self.special_numbers_vars[number]["thickness"]

        minus_btn2 = ttk.Button(thickness_frame, text="-", width=3,
                            command=lambda: self.adjust_special_number_value(number, "thickness", -1))
        minus_btn2.pack(side="left", padx=(0, 5))

        entry2 = ttk.Entry(thickness_frame, textvariable=var_thickness, width=10)
        entry2.pack(side="left")

        plus_btn2 = ttk.Button(thickness_frame, text="+", width=3,
                            command=lambda: self.adjust_special_number_value(number, "thickness", 1))
        plus_btn2.pack(side="left", padx=(5, 0))

        # Color control
        color_frame = ttk.Frame(frame)
        color_frame.pack(fill="x", pady=5)

        ttk.Label(color_frame, text="Color:", width=8).pack(side="left")

        # Color preview - using only RGB for background color
        preview_color = self.special_numbers_vars[number]["color"]
        color_preview = tk.Frame(color_frame, height=20, width=60,
                                bg=self.rgb_to_hex(preview_color[:3]))
        color_preview.pack(side="left", padx=(0, 10))

        # Store reference to preview widget
        self.special_numbers_vars[number]["preview_widget"] = color_preview

        # Color picker button
        color_btn = ttk.Button(color_frame, text="Pick Color",
                            command=lambda n=number: self.pick_special_number_color(n))
        color_btn.pack(side="left")

        # Alpha control (شفافیت)
        alpha_frame = ttk.Frame(frame)
        alpha_frame.pack(fill="x", pady=5)

        ttk.Label(alpha_frame, text="Alpha:", width=8).pack(side="left")

        # Get current alpha value (index 3 in color list)
        current_alpha = self.special_numbers_vars[number]["color"][3]

        # Create IntVar for alpha
        alpha_var = tk.IntVar(value=current_alpha)

        # Store alpha variable reference
        self.special_numbers_vars[number]["alpha_var"] = alpha_var

        # Create scale widget (slider)
        alpha_scale = ttk.Scale(
            alpha_frame,
            from_=0,
            to=255,
            variable=alpha_var,
            command=lambda val, n=number: self.update_special_number_alpha(n, int(float(val)))
        )
        alpha_scale.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # Label to show current alpha value
        alpha_label = ttk.Label(alpha_frame, text=str(current_alpha), width=4)
        alpha_label.pack(side="left")

        # Store reference to alpha label
        self.special_numbers_vars[number]["alpha_label"] = alpha_label





    def update_special_number_alpha(self, number, alpha_value):
        """Update alpha color"""
        self.special_numbers_vars[number]["color"][3] = alpha_value

        self.special_numbers_vars[number]["alpha_label"].config(text=str(alpha_value))


    def adjust_special_number_value(self, number, property_name, delta):
        """Adjust value for special number property"""
        var = self.special_numbers_vars[number][property_name]
        current = var.get()
        new_value = round(current + delta, 1)
        var.set(new_value)

    def pick_special_number_color(self, number):
        """Pick color for special number"""
        current_color = self.special_numbers_vars[number]["color"][:3]
        color = colorchooser.askcolor(title=f"Pick Color for Number {number}",
                                    initialcolor=self.rgb_to_hex(current_color))
        if color[0]:
            r, g, b = [int(c) for c in color[0]]
            # Update preview widget
            self.special_numbers_vars[number]["preview_widget"].config(bg=self.rgb_to_hex((r, g, b)))
            # Update color in memory (keep alpha from original)
            current_alpha = self.special_numbers_vars[number]["color"][3]
            self.special_numbers_vars[number]["color"] = [r, g, b, current_alpha]



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
            ("POINTER_SCALE", "Scale", config.configs_dic["pointer"]["POINTER_SCALE"]),
            ("POINTER_START_AT", "Start At (px)", config.configs_dic["pointer"]["POINTER_START_AT"]),
            ("POINTER_LENGTH", "Length/Radius", config.configs_dic["pointer"]["POINTER_LENGTH"]),
            ("POINTER_THICKNESS", "Thickness", config.configs_dic["pointer"]["POINTER_THICKNESS"]),
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
                                command=lambda v: self.update_alpha(int(v)))
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
        self.create_numeric_control_frame(left_column, "FRAME_SCALE", "Frame Scale", 4)
        self.create_numeric_control_frame(left_column, "FRAME_CLOCK_PADDING", "Clock Padding", 10)

        # Has Border checkbox
        bool_frame1 = ttk.LabelFrame(left_column, text="Frame Border", padding=10)
        bool_frame1.pack(fill="x", padx=5, pady=5)

        self.has_border_var = tk.BooleanVar(value=self.configs_dic["frame"]["FRAME_HAS_BORDER"])
        has_border_cb = ttk.Checkbutton(bool_frame1, text="Has Border",
                                        variable=self.has_border_var)
        has_border_cb.pack(anchor="w", pady=2)

        self.create_numeric_control_frame(left_column, "FRAME_BORDER_THICKNESS", "Border Thickness", 2)

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
                                       command=lambda v: self.update_frame_alpha("FRAME_BORDER_COLOR", self.border_color_preview, int(v)))
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
                                   command=lambda v: self.update_frame_alpha("FRAME_CLOCK_BG_COLOR", self.bg_color_preview, int(v)))
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
        self.create_numeric_control_frame(right_column, "FRAME_NUMBER_LENGTH", "Number Length", 20)
        self.create_numeric_control_frame(right_column, "FRAME_NUMBER_THICKNESS", "Number Thickness", 4)

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
                                       variable=self.number_alpha_var)
        number_alpha_slider.pack(side="left", fill="x", expand=True, padx=5)

        self.number_alpha_label = ttk.Label(number_alpha_frame, text=str(self.number_alpha_var.get()), width=3)
        self.number_alpha_label.pack(side="right")

        # More number controls in right column
        self.create_numeric_control_frame(right_column, "FRAME_NUMBER_OFFSET", "Number Offset", 10)
        self.create_numeric_control_frame(right_column, "FRAME_NUMBER_RADIUS", "Number Radius", 2)

        # Frame Size (integer) in right column
        self.create_integer_control_frame(right_column, "FRAME_SIZE", "Frame Size", 200)

    def create_numeric_control(self, parent, config_key, label_text, default_value):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(frame, text=label_text + ":", width=20).pack(side="left")

        var = tk.DoubleVar(value=default_value)
        self.numeric_vars[config_key] = var

        minus_btn = ttk.Button(frame, text="-", width=3,
                              command=lambda: self.adjust_numeric(config_key, -1))
        minus_btn.pack(side="left", padx=(0, 5))

        entry = ttk.Entry(frame, textvariable=var, width=10)
        entry.pack(side="left")

        plus_btn = ttk.Button(frame, text="+", width=3,
                             command=lambda: self.adjust_numeric(config_key, 1))
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
                              command=lambda: self.adjust_numeric_frame(config_key, -1))
        minus_btn.pack(side="left", padx=(0, 5))

        entry = ttk.Entry(frame, textvariable=var, width=10)
        entry.pack(side="left")

        plus_btn = ttk.Button(frame, text="+", width=3,
                             command=lambda: self.adjust_numeric_frame(config_key, 1))
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

        # Update Special Numbers values (in update_all_values function)
        if hasattr(self, 'special_numbers_vars'):
            for number in [3, 6, 9, 12]:
                if number in self.special_numbers_vars:
                    # Get color from preview widget
                    preview_widget = self.special_numbers_vars[number]["preview_widget"]
                    hex_color = preview_widget.cget("bg")
                    hex_color = hex_color.lstrip('#')
                    r = int(hex_color[0:2], 16)
                    g = int(hex_color[2:4], 16)
                    b = int(hex_color[4:6], 16)
                    # Use number color alpha if available, otherwise default
                    color_data = self.special_numbers_vars[number]["color"]
                    a = color_data[3] if len(color_data) > 3 else self.configs_dic["frame"]["FRAME_NUMBER_COLOR"][3]

                    self.configs_dic["frame"]["FRAME_SPECIAL_NUMBERS"][number] = {
                        "length": self.special_numbers_vars[number]["length"].get(),
                        "thickness": self.special_numbers_vars[number]["thickness"].get(),
                        "color": (r, g, b, a)
                    }


        self.convert_float_values_to_ints()

        # print("\n")
        # print("\n")
        # print("Updated all values:")
        # print("\n")
        # print("Pointer:", self.configs_dic["pointer"])
        # print("\n")
        # print("Frame:", self.configs_dic["frame"])
        # print("\n")
        # print("Special Numbers:", self.configs_dic["frame"]["FRAME_SPECIAL_NUMBERS"])
        # print("\n")
        # print("\n")


        self.update_images()

    def rgb_to_hex(self, rgb):
        return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'

    def update_bg_color(self):
        color = self.bg_color_var.get()
        # self.right_section.config(bg=color)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()





