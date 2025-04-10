# constants.py
# This file contains constants for the kindergarten snake game, including screen dimensions, colors, and game states.

import pygame

# --- Constants ---
SCREEN_WIDTH_INIT = 800
SCREEN_HEIGHT_INIT = 600
FPS = 60

# Game States
STATE_WELCOME = 0
STATE_LEVEL_SELECT = 1
STATE_PLAYING = 2
STATE_WIN_LEVEL_ANIMATING = 3  # Cage break animation
STATE_WIN_LEVEL_CONGRATS = 4   # Congratulations display
STATE_GAME_OVER = 5
STATE_MENU_SELECT = 6          # State for the popup menu

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (211, 0, 0)
BRIGHT_RED = (255, 0, 0)
GREEN = (0, 180, 0)
BRIGHT_GREEN = (0, 255, 0)
BLUE = (0, 0, 200)
DARK_BLUE = (0, 0, 100)        # For number items
BRIGHT_BLUE = (50, 50, 255)
DARK_PURPLE = (80, 0, 80)      # For letter items
BRIGHT_PURPLE = (150, 0, 150)
DARK_CYAN = (0, 80, 80)        # For word items
BRIGHT_CYAN = (0, 255, 255)    
YELLOW = (230, 230, 0)
LIGHT_YELLOW = (255, 255, 150) # Fill for shapes
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GREY = (169, 169, 169)
DARK_GREY = (100, 100, 100)
SNAKE_COLOR = (34, 139, 34)
SNAKE_COLOR_DARK = (0, 100, 0)
CAGE_COLOR = (139, 69, 19)     # Brown
PARTICLE_COLORS = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, WHITE]
SHAPE_NAMES = ["Square", "Triangle", "Rectangle", "Circle", "Pentagon"]

# Level Definitions
LEVELS = {
    1: {'target': 3, 'time': 20, 'speed_mult': 1.0},
    2: {'target': 4, 'time': 20, 'speed_mult': 1.1},
    3: {'target': 6, 'time': 15, 'speed_mult': 1.2},
    4: {'target': 8, 'time': 15, 'speed_mult': 1.3},
    5: {'target': 10,'time': 10, 'speed_mult': 1.4},
}
MAX_LEVEL = len(LEVELS)

# All possible food items
ALL_FOOD_ITEMS = [str(i) for i in range(1, 11)] + \
                 [chr(ord('A') + i) for i in range(26)] + \
                 [("α" if i == 0 else chr(ord('a') + i)) for i in range(26)] + \
                 SHAPE_NAMES

# Initialize fonts - these will be initialized in main.py after pygame init
FONT_TITLE = None
FONT_MEDIUM = None
FONT_SMALL = None
FONT_TINY = None
FONT_HUD = None
FONT_MENU = None

def initialize_fonts():
    """Initialize font objects after pygame is initialized."""
    global FONT_TITLE, FONT_MEDIUM, FONT_SMALL, FONT_TINY, FONT_HUD, FONT_MENU
    
    try:
        FONT_TITLE = pygame.font.SysFont("Arial", 72, bold=True)
        FONT_MEDIUM = pygame.font.SysFont("Consolas", 36)
        FONT_SMALL = pygame.font.SysFont("Consolas", 24)
        FONT_TINY = pygame.font.SysFont("Consolas", 16)
        FONT_HUD = pygame.font.SysFont("Impact", 48)
        FONT_MENU = pygame.font.SysFont("Consolas", 20)
    except Exception as e:
        print(f"Warning: Font loading error ({e}), using default pygame fonts.")
        FONT_TITLE = pygame.font.Font(None, 80)
        FONT_MEDIUM = pygame.font.Font(None, 40)
        FONT_SMALL = pygame.font.Font(None, 30)
        FONT_TINY = pygame.font.Font(None, 20)
        FONT_HUD = pygame.font.Font(None, 55)
        FONT_MENU = pygame.font.Font(None, 26)