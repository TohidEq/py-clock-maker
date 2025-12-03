
img_config_dic={
    "BASE_DIR":"/home/arc/.config/clockimgs/",
    "FRAME_DIR":"frames/",
    "POINTER_DIR":"hms/",
    "H_POINTER_DIR":"h/",
    "M_POINTER_DIR":"m/",
    "S_POINTER_DIR":"s/"
}

configs_dic = {
    "pointer": {
        "POINTER_SHAPE": "line",
        "POINTER_SCALE": 3,
        "POINTER_START_AT": 90,
        "POINTER_LENGTH": 25,
        "POINTER_THICKNESS": 6,
        "POINTER_COLOR": (0, 0, 0, 200),
        "POINTER_ROUND_START": True,
        "POINTER_ROUND_END": True,
        "POINTER_SIZE": 180,
    },
    "frame": {
        "FRAME_SCALE": 3,
        "FRAME_CLOCK_PADDING": 5,
        "FRAME_HAS_BORDER": False,
        "FRAME_BORDER_THICKNESS": 0,
        "FRAME_BORDER_COLOR": (0, 0, 0, 255),
        "FRAME_CLOCK_BG_COLOR": (255, 255, 255, 255),
        "FRAME_HAS_NUMBERS": False,
        "FRAME_NUMBER_SHAPE": "line",
        "FRAME_NUMBER_LENGTH": 10,
        "FRAME_NUMBER_THICKNESS": 2,
        "FRAME_NUMBER_COLOR": (0, 0, 0, 150),
        "FRAME_NUMBER_OFFSET": 5,
        "FRAME_NUMBER_RADIUS": 0,
        "FRAME_SPECIAL_NUMBERS": {
            3: {"length": -1, "thickness": -1, "color": None},
            6: {"length": -1, "thickness": -1, "color": None},
            9: {"length": -1, "thickness": -1, "color": None},
            12: {"length": -1, "thickness": -1, "color": None},
        },
        "FRAME_SIZE": 180,
    }
}


# AVAILABLE THEMES :: https://ttkthemes.readthedocs.io/en/latest/themes.html

# Adapta Aquativo Arc Black Blue Breeze Clearlooks  Elegance Equilux ITFT1 Keramik Kroc Plastik Radiance(Ubuntu) Scid themes Smog winxpblue yaru

# TRY lowercase NAMES FOR THEME !!!

WINDOW_THEME = ("yaru")

WINDOW_TITLE = ("🕐 Clock Maker")
WINDOW_SIZE = ("1280x800")