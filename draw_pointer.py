
from PIL import Image, ImageDraw
from IPython.display import display
import math
def draw_pointer(pos, configs_dic, preview=False, preview_window=False):
    width, height = int(configs_dic["pointer"]["POINTER_SIZE"] * configs_dic["pointer"]["POINTER_SCALE"]), \
                    int(configs_dic["pointer"]["POINTER_SIZE"] * configs_dic["pointer"]["POINTER_SCALE"])
    cx, cy = width // 2, height // 2

    img = Image.new("RGBA", (width, height), (0,0,0,0))
    draw = ImageDraw.Draw(img)

    # scaled units
    start_at = configs_dic["pointer"]["POINTER_START_AT"] * configs_dic["pointer"]["POINTER_SCALE"]
    length   = configs_dic["pointer"]["POINTER_LENGTH"] * configs_dic["pointer"]["POINTER_SCALE"]
    thickness = configs_dic["pointer"]["POINTER_THICKNESS"] * configs_dic["pointer"]["POINTER_SCALE"]
    r = thickness / 2  # round cap radius

    # angle in radians
    angle = math.radians((pos/60)*360 - 90)

    # start point
    x_start = cx + start_at * math.cos(angle)
    y_start = cy + start_at * math.sin(angle)

    # draw selected shape
    if configs_dic["pointer"]["POINTER_SHAPE"] == "line":
        x_end = cx + (start_at + length) * math.cos(angle)
        y_end = cy + (start_at + length) * math.sin(angle)

        # main line
        draw.line(
            [x_start, y_start, x_end, y_end],
            fill=configs_dic["pointer"]["POINTER_COLOR"],
            width=thickness
        )

        # round caps
        if configs_dic["pointer"]["POINTER_ROUND_START"]:
            draw.ellipse(
                [x_start - r, y_start - r, x_start + r, y_start + r],
                fill=configs_dic["pointer"]["POINTER_COLOR"]
            )
        if configs_dic["pointer"]["POINTER_ROUND_END"]:
            draw.ellipse(
                [x_end - r, y_end - r, x_end + r, y_end + r],
                fill=configs_dic["pointer"]["POINTER_COLOR"]
            )

    elif configs_dic["pointer"]["POINTER_SHAPE"] == "circle":
        circle_r = length
        draw.ellipse(
            [x_start - circle_r, y_start - circle_r,
             x_start + circle_r, y_start + circle_r],
            outline=configs_dic["pointer"]["POINTER_COLOR"],
            width=thickness
        )

    # anti-aliasing
    img_small = img.resize(
        (configs_dic["pointer"]["POINTER_SIZE"], configs_dic["pointer"]["POINTER_SIZE"]),
        Image.Resampling.LANCZOS
    )
    if preview:
        display(img_small)
        if preview_window:
            img_small.show()
    else:
        return img_small
