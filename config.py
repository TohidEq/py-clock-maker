
img_config_dic={
    "BASE_DIR":"/home/arc/.config/clockimgs/",
    "FRAME_DIR":"frames/",
    "POINTER_DIR":"hms/",
    "H_POINTER_DIR":"h/",
    "M_POINTER_DIR":"m/",
    "S_POINTER_DIR":"s/"
}

configs_dic =  {
    "pointer": {
        "POINTER_SHAPE": "line",
        "POINTER_SCALE": 8,
        "POINTER_START_AT": 47,
        "POINTER_LENGTH": 22,
        "POINTER_THICKNESS": 7,
        "POINTER_COLOR": (180, 120, 40, 255),
        "POINTER_ROUND_START": True,
        "POINTER_ROUND_END": True,
        "POINTER_SIZE": 201,
    },
    "frame": {
        "FRAME_SCALE": 8,
        "FRAME_CLOCK_PADDING": 12,
        "FRAME_HAS_BORDER": False,
        "FRAME_BORDER_RADIUS": 3,
        "FRAME_BORDER_COLOR": (120, 80, 40, 155),
        "FRAME_CLOCK_BG_COLOR": (240, 230, 210, 155),
        "FRAME_HAS_NUMBERS": True,
        "FRAME_NUMBER_SHAPE": "line",
        "FRAME_NUMBER_LENGTH": 18,
        "FRAME_NUMBER_THICKNESS": 3,
        "FRAME_NUMBER_COLOR": (40, 40, 40, 155),
        "FRAME_NUMBER_OFFSET": 10,
        "FRAME_NUMBER_RADIUS": 0,
        "FRAME_SPECIAL_NUMBERS": {
            3: {"length": -1, "thickness": -1, "color": (40, 40, 40, 155)},
            6: {"length": -1, "thickness": -1, "color": (40, 40, 40, 155)},
            9: {"length": -1, "thickness": -1, "color": (40, 40, 40, 155)},
            12: {"length": -1, "thickness": -1, "color": (40, 40, 40, 155)},
        },
        "FRAME_SIZE": 201,
    }
}


# AVAILABLE THEMES :: https://ttkthemes.readthedocs.io/en/latest/themes.html

# Adapta Aquativo Arc Black Blue Breeze Clearlooks  Elegance Equilux ITFT1 Keramik Kroc Plastik Radiance(Ubuntu) Scid themes Smog winxpblue yaru

# TRY lowercase NAMES FOR THEME !!!

WINDOW_THEME = ("yaru")

WINDOW_TITLE = ("🕐 Clock Maker")
WINDOW_SIZE = ("1280x800")