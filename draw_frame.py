SIZE = 200
SCALE = 4 # higher number = better anti-aliasing = slower generation
CLOCK_PADDING = 10

HAS_BORDER = True
BORDER_WIDTH = 2
BORDER_COLOR = (0, 0, 0, 255)

CLOCK_BG_COLOR = (255, 255, 255, 100)  # only inside the clock

# - Numbers Signs -
HAS_NUMBERS = True
NUMBER_STYLE = "rectangle" # "rectangle", "circle", "line"
NUMBER_LENGTH = 20
NUMBER_THICKNESS = 4
NUMBER_COLOR = (200, 0, 0, 100)
NUMBER_OFFSET = 10
NUMBER_RADIUS = 2

SPECIAL_NUMBERS = {
    3: {"length": None, "thickness": None, "color": None},
    6: {"length": None, "thickness": None, "color": None},
    9: {"length": None, "thickness": None, "color": None},
    12: {"length": None, "thickness": None, "color": None},
}

# ------  ========   --------

IMG_WIDTH = SIZE
IMG_HEIGHT = SIZE


from PIL import Image, ImageDraw
from IPython.display import display
import math


def draw_frame(preview=False, preview_window=False):
    width, height = IMG_WIDTH*SCALE, IMG_HEIGHT*SCALE
    img = Image.new("RGBA", (width, height), (0,0,0,0))  # fully transparent
    draw = ImageDraw.Draw(img)

    center = (width // 2, height // 2)
    radius = min(width, height)//2 - (BORDER_WIDTH*SCALE if HAS_BORDER else 0) - (CLOCK_PADDING*SCALE)

    # fill clock face
    draw.ellipse(
        [center[0]-radius, center[1]-radius, center[0]+radius, center[1]+radius],
        fill=CLOCK_BG_COLOR
    )

    # draw clock border
    if HAS_BORDER and BORDER_WIDTH > 0:
        draw.ellipse(
            [center[0]-radius, center[1]-radius, center[0]+radius, center[1]+radius],
            outline=BORDER_COLOR,
            width=BORDER_WIDTH*SCALE
        )

    # draw hour marks
    if HAS_NUMBERS:
        for hour in range(1, 13):
            angle = math.radians((hour/12)*360 - 90)
            outer_r = radius - NUMBER_OFFSET*SCALE
            x_outer = center[0] + outer_r * math.cos(angle)
            y_outer = center[1] + outer_r * math.sin(angle)

            length = SPECIAL_NUMBERS.get(hour, {}).get("length") or NUMBER_LENGTH*SCALE
            thickness = SPECIAL_NUMBERS.get(hour, {}).get("thickness") or NUMBER_THICKNESS*SCALE
            color = SPECIAL_NUMBERS.get(hour, {}).get("color") or NUMBER_COLOR

            if NUMBER_STYLE == 'circle':
                temp = Image.new("RGBA", (length, length), (0,0,0,0))
                d = ImageDraw.Draw(temp)
                d.ellipse([0,0,length,length], fill=color)
                temp = temp.rotate(-math.degrees(angle), expand=True, resample=Image.Resampling.BICUBIC)
                img.paste(temp, (int(x_outer-temp.width//2), int(y_outer-temp.height//2)), temp)

            elif NUMBER_STYLE == 'rectangle':
                temp = Image.new("RGBA", (length, length), (0,0,0,0))
                d = ImageDraw.Draw(temp)
                d.rounded_rectangle([0,0,length,length], radius=NUMBER_RADIUS*SCALE, fill=color)
                temp = temp.rotate(-math.degrees(angle), expand=True, resample=Image.Resampling.BICUBIC)
                img.paste(temp, (int(x_outer-temp.width//2), int(y_outer-temp.height//2)), temp)

            elif NUMBER_STYLE == 'line':
                x_inner = center[0] + (outer_r - length) * math.cos(angle)
                y_inner = center[1] + (outer_r - length) * math.sin(angle)
                draw.line([x_inner, y_inner, x_outer, y_outer], fill=color, width=thickness)

    # resize for anti-aliasing
    img_small = img.resize((IMG_WIDTH, IMG_HEIGHT), Image.Resampling.LANCZOS)
    if preview:
        display(img_small)
        if preview_window:
            img_small.show()
    else: 
        return img_small


draw_frame()

