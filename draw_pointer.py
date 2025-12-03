SHAPE = "circle"   # "line", "circle"
SIZE = 200
SCALE = 4 # higher number = better anti-aliasing = slower generation

START_AT = 80      # distance from center (in px)
LENGTH = 20        # length OR radius (depends on shape)
POINTER_THICKNESS = 10
POINTER_COLOR = (255, 0, 0, 150)

ROUND_START = True
ROUND_END   = True



# ------  ========   --------

IMG_WIDTH = SIZE
IMG_HEIGHT = SIZE

from PIL import Image, ImageDraw
from IPython.display import display
import math


def draw_pointer(pos, preview=False, preview_window=False):
    width, height = IMG_WIDTH*SCALE, IMG_HEIGHT*SCALE
    cx, cy = width//2, height//2
    
    img = Image.new("RGBA", (width, height), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    
    # scaled units
    start_at = START_AT * SCALE
    length   = LENGTH * SCALE
    thickness = POINTER_THICKNESS * SCALE
    r = thickness/2  # round cap radius
    
    # angle in radians
    angle = math.radians((pos/60)*360 - 90)
    
    # start point
    x_start = cx + start_at * math.cos(angle)
    y_start = cy + start_at * math.sin(angle)
    
    # draw selected shape
    if SHAPE == "line":
        x_end = cx + (start_at + length) * math.cos(angle)
        y_end = cy + (start_at + length) * math.sin(angle)
        
        # main line
        draw.line(
            [x_start, y_start, x_end, y_end],
            fill=POINTER_COLOR,
            width=thickness
        )
        
        # round caps
        if ROUND_START:
            draw.ellipse(
                [x_start - r, y_start - r, x_start + r, y_start + r],
                fill=POINTER_COLOR
            )
        if ROUND_END:
            draw.ellipse(
                [x_end - r, y_end - r, x_end + r, y_end + r],
                fill=POINTER_COLOR
            )
    
    elif SHAPE == "circle":
        circle_r = length
        draw.ellipse(
            [x_start - circle_r, y_start - circle_r,
             x_start + circle_r, y_start + circle_r],
            outline=POINTER_COLOR,
            width=thickness
        )
    
    # anti-aliasing
    img_small = img.resize((IMG_WIDTH, IMG_HEIGHT), Image.Resampling.LANCZOS)
    if preview:
        display(img_small)
        if preview_window:
            img_small.show()
    else:
        return img_small

draw_pointer(10)


