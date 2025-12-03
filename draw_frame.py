
from PIL import Image, ImageDraw
from IPython.display import display
import math

def draw_frame(configs_dic, preview=False, preview_window=False):
    width  = int(configs_dic["frame"]["FRAME_SIZE"]  * configs_dic["frame"]["FRAME_SCALE"])
    height = int(configs_dic["frame"]["FRAME_SIZE"] * configs_dic["frame"]["FRAME_SCALE"])

    img = Image.new("RGBA", (width, height), (0,0,0,0))
    draw = ImageDraw.Draw(img)

    center = (width // 2, height // 2)

    radius = (
        min(width, height)//2
        - (configs_dic["frame"]["FRAME_BORDER_THICKNESS"] * configs_dic["frame"]["FRAME_SCALE"]
           if configs_dic["frame"]["FRAME_HAS_BORDER"] else 0)
        - (configs_dic["frame"]["FRAME_CLOCK_PADDING"] * configs_dic["frame"]["FRAME_SCALE"])
    )

    # fill clock face
    draw.ellipse(
        [center[0]-radius, center[1]-radius, center[0]+radius, center[1]+radius],
        fill=configs_dic["frame"]["FRAME_CLOCK_BG_COLOR"]
    )

    # draw clock border
    if configs_dic["frame"]["FRAME_HAS_BORDER"] and configs_dic["frame"]["FRAME_BORDER_THICKNESS"] > 0:
        draw.ellipse(
            [center[0]-radius, center[1]-radius, center[0]+radius, center[1]+radius],
            outline=configs_dic["frame"]["FRAME_BORDER_COLOR"],
            width=configs_dic["frame"]["FRAME_BORDER_THICKNESS"] * configs_dic["frame"]["FRAME_SCALE"]
        )

    # draw hour marks
    if configs_dic["frame"]["FRAME_HAS_NUMBERS"]:
        for hour in range(1, 13):
            angle = math.radians((hour/12)*360 - 90)

            outer_r = radius - configs_dic["frame"]["FRAME_NUMBER_OFFSET"] * configs_dic["frame"]["FRAME_SCALE"]

            x_outer = center[0] + outer_r * math.cos(angle)
            y_outer = center[1] + outer_r * math.sin(angle)

            length = 0
            thickness = 0
            normal_length = configs_dic["frame"]["FRAME_NUMBER_LENGTH"] * configs_dic["frame"]["FRAME_SCALE"]
            normal_thickness = configs_dic["frame"]["FRAME_NUMBER_THICKNESS"] * configs_dic["frame"]["FRAME_SCALE"]
            if hour in [3,6,9,12]:
                s_length = configs_dic["frame"]["FRAME_SPECIAL_NUMBERS"][hour]["length"]
                s_thickness= configs_dic["frame"]["FRAME_SPECIAL_NUMBERS"][hour]["thickness"]
                if s_length >=0:
                    length=s_length * configs_dic["frame"]["FRAME_SCALE"]
                else:
                    length = normal_length

                if s_thickness >=0:
                    thickness = s_thickness
                else:
                    thickness = normal_thickness

            else:
                length = normal_length
                thickness = normal_thickness

            color = (
                configs_dic["frame"]["FRAME_SPECIAL_NUMBERS"].get(hour, {}).get("color")
                or configs_dic["frame"]["FRAME_NUMBER_COLOR"])


            if configs_dic["frame"]["FRAME_NUMBER_SHAPE"] == 'circle':
                temp = Image.new("RGBA", (length, length), (0,0,0,0))
                d = ImageDraw.Draw(temp)
                d.ellipse([0,0,length,length], fill=color)
                temp = temp.rotate(-math.degrees(angle), expand=True, resample=Image.Resampling.BICUBIC)
                img.paste(temp, (int(x_outer-temp.width//2), int(y_outer-temp.height//2)), temp)

            elif configs_dic["frame"]["FRAME_NUMBER_SHAPE"] == 'rectangle':
                temp = Image.new("RGBA", (length, length), (0,0,0,0))
                d = ImageDraw.Draw(temp)
                d.rounded_rectangle(
                    [0,0,length,length],
                    radius=configs_dic["frame"]["FRAME_NUMBER_RADIUS"] * configs_dic["frame"]["FRAME_SCALE"],
                    fill=color
                )
                temp = temp.rotate(-math.degrees(angle), expand=True, resample=Image.Resampling.BICUBIC)
                img.paste(temp, (int(x_outer-temp.width//2), int(y_outer-temp.height//2)), temp)

            elif configs_dic["frame"]["FRAME_NUMBER_SHAPE"] == 'line':
                x_inner = center[0] + (outer_r - length) * math.cos(angle)
                y_inner = center[1] + (outer_r - length) * math.sin(angle)
                draw.line([x_inner, y_inner, x_outer, y_outer], fill=color, width=thickness)

    # resize for anti-aliasing
    img_small = img.resize(
        (configs_dic["frame"]["FRAME_SIZE"], configs_dic["frame"]["FRAME_SIZE"]),
        Image.Resampling.LANCZOS
    )

    if preview:
        display(img_small)
        if preview_window:
            img_small.show()
    else:
        return img_small


