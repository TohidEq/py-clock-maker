
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
        "FRAME_SPECIAL_NUMBERS": {
            3: {"length": -1, "thickness": -1, "color": None},
            6: {"length": -1, "thickness": -1, "color": None},
            9: {"length": -1, "thickness": -1, "color": None},
            12: {"length": -1, "thickness": -1, "color": None},
        },
        "FRAME_SIZE": 200,
    }
}

# AVAILABLE THEMES :: https://ttkthemes.readthedocs.io/en/latest/themes.html

# Adapta Aquativo Arc Black Blue Breeze Clearlooks  Elegance Equilux ITFT1 Keramik Kroc Plastik Radiance(Ubuntu) Scid themes Smog winxpblue yaru

# TRY lowercase NAMES FOR THEME !!!

WINDOW_THEME = ("yaru")

WINDOW_TITLE = ("🕐 Clock Maker")
WINDOW_SIZE = ("1280x800")