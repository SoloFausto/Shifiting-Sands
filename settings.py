from pyray import *
from raylib import *


WINDOW_WIDTH, WINDOW_HEIGHT = 2560, 1800

GRID_AMOUNT_X = 350
GRID_AMOUNT_Y = 350 
GAME_CONTROLS = [(KEY_Z,KEY_X),(KEY_N,KEY_M),(KEY_O,KEY_P),(KEY_Q,KEY_W)]
red_player_color = Color(197, 88, 77,255)
blue_player_color = Color(78, 77, 197,255)
green_player_color = Color(108, 209, 99,255)
yellow_player_color = Color(197, 193, 77,255)

PLAYER_COLORS = [red_player_color, green_player_color,yellow_player_color ,blue_player_color]
PLAYER_COLOR_NAMES = ["red", "green", "yellow", "blue"]
PLAYER_CONTROL_NAMES = ["Z/X", "N/M", "O/P", "Q/W"]
TEXTURES = {}
SOUNDS = {}
PAUSE_KEY = KEY_BACKSPACE
WIN_SCORE = 10
FONT_SIZE = max(20, int(WINDOW_WIDTH * 0.03))



CELL_SIZE = min(WINDOW_WIDTH // GRID_AMOUNT_X, WINDOW_HEIGHT // GRID_AMOUNT_Y)
CELL_W = CELL_SIZE
CELL_H = CELL_SIZE
#AI helped me with centering the playfield
PLAYFIELD_WIDTH = CELL_W * GRID_AMOUNT_X
PLAYFIELD_HEIGHT = CELL_H * GRID_AMOUNT_Y
PLAYFIELD_OFFSET_X = (WINDOW_WIDTH - PLAYFIELD_WIDTH) // 2
PLAYFIELD_OFFSET_Y = (WINDOW_HEIGHT - PLAYFIELD_HEIGHT) // 2



def translateGridtoXY(gridcoord):
    top_x = PLAYFIELD_OFFSET_X + (CELL_W * gridcoord.x)
    top_y = PLAYFIELD_OFFSET_Y + (CELL_H * gridcoord.y)
    return Vector2(top_x,top_y)