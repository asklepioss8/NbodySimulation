# GENERAL WINDOW SETTINGS
RES = (WIDTH, HEIGHT) = (1440, 1000)
HALF_WIDTH = WIDTH / 2
HALF_HEIGHT = HEIGHT / 2
NULL_SCREEN = (0, 0, 0, 1)
FPS = 60

FAR = HEIGHT
NEAR = -HALF_HEIGHT
DEPTH = FAR - NEAR

# GAME SETTINGS
MAX_DISPLAY_RADIUS = 0.35
OBJ_COUNT = 100
OBJ_RADIUS = 0.001  # the value for the non-translated cube the max value is cube limits
OBJ_MASS = 10

# pretranslation limits
CUBE_CENTER = (0, 0, 0)
CUBE_MARGIN = 0.6
HALF_MARGIN = CUBE_MARGIN / 2
CUBIC_LIMITS = ((-HALF_MARGIN, -HALF_MARGIN, -HALF_MARGIN), (HALF_MARGIN, HALF_MARGIN, HALF_MARGIN))

BODY_INIT_BUFFER = 0.2
INIT_MARGIN = (CUBE_MARGIN - BODY_INIT_BUFFER) / 2  # actually the longest distance on
# any axis that objects can be spawned
INIT_LIMITS = ((-INIT_MARGIN, -INIT_MARGIN, -INIT_MARGIN), (INIT_MARGIN, INIT_MARGIN, INIT_MARGIN))
RATIO = HEIGHT  # ratio is the postcalculational scaling factor


# CONSTANTS
COR = 1  # coefficient of restitution

