import os

# Game constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60
TILE_SIZE = 40

# Pacman size
PACMAN_RADIUS = 12

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Direction constants
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
STOP = (0, 0)

# Mob constants
MOB_SPEED = 2

# Food constants
FOOD_RADIUS = 3
FOOD_SCORE = 10

# Highscore file
HIGHSCORE_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "highscore.txt"
)
