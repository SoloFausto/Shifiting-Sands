from pyray import *
from raylib import *

# --- Expanded Level Tilemap Definition (50x16 tiles = 2000px wide) ---

LEVEL_PATH = "assets/level.txt"
TILE_ROWS = len(open(LEVEL_PATH).readlines())
TILE_COLS = len(open(LEVEL_PATH).readline().strip())
TILE_SIZE = 40

WINDOW_WIDTH, WINDOW_HEIGHT = 1024, 768
WORLD_WIDTH = TILE_COLS * TILE_SIZE
WORLD_HEIGHT = TILE_ROWS * TILE_SIZE

SOUNDS = {}
PAUSE_KEY = KEY_BACKSPACE
UP_KEY = KEY_W
DOWN_KEY = KEY_S
LEFT_KEY = KEY_A
RIGHT_KEY = KEY_D
JUMP_KEY = KEY_SPACE
FONT_SIZE = max(20, int(WINDOW_WIDTH * 0.03))

# --- Game Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
      # Size of one tile in pixels
GRAVITY = 1800.0        # Downward acceleration (pixels/s/s)
JUMP_VELOCITY = -750.0  # Initial upward velocity on jump
STOMP_BOUNCE = JUMP_VELOCITY * 0.6 # Reduced jump velocity for bounce
PLAYER_SPEED = 300.0    # Player horizontal movement speed
ENEMY_SPEED = 100.0     # Enemy horizontal movement speed
PLAYER_WIDTH = TILE_SIZE * 0.8
PLAYER_HEIGHT = TILE_SIZE * 0.9

# --- Tilemap Definitions ---
TEXTURES = {}


TILE_AIR = 0
TILE_SOLID = 1
TILE_COIN = 2
TILE_ENEMY = 3
TILE_SAND_BLOCK = 4


