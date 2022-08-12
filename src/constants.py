# game constants

SIZE_X, SIZE_Y = 10, 20
FALL_SPEED = 0.5
TYPES = {
    'I': 1,
    'O': 2,
    'T': 3,
    'J': 4,
    'L': 5,
    'S': 6,
    'Z': 7,
}
STUCK_FRAME_TOLERANCE = 20

# GUI constants
BLOC_SIZE = 32
BLOC_LIGHT_EFFECT_SIZE = int(0.125 * BLOC_SIZE)
RIGHT_PANEL_SIZE_X = 6
NEXT_BLOC_FRAME_HEIGHT = 4
BOARD_SIZE_X, BOARD_SIZE_Y = SIZE_X + 2, SIZE_Y + 2
DISPLAY_SIZE_X, DISPLAY_SIZE_Y = int((BOARD_SIZE_X + RIGHT_PANEL_SIZE_X) * BLOC_SIZE), int(BOARD_SIZE_Y * BLOC_SIZE)

BLOC_COLORS = {
    0: [150, 150, 150],         # grey (for contour)
    TYPES['I']: [0, 210, 210],  # cyan
    TYPES['O']: [210, 210, 0],  # yellow
    TYPES['T']: [140, 0, 210],  # purple
    TYPES['J']: [0, 0, 210],    # blue
    TYPES['L']: [210, 140, 0],  # orange
    TYPES['S']: [0, 210, 0],    # green
    TYPES['Z']: [210, 0, 0],    # red
}

BLACK = (0, 0, 0)

FPS = 60
