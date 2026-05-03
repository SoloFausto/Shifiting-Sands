import random
import math
from raylib import *
from pyray import *
from settings import *
class Gems:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tile_id = random.randint(0, 4),random.randint(0, 5)

    def update(self):
        pass
    def draw(self):
        tex = TEXTURES["gems"]
        frame_width = tex.width // 5
        frame_height = tex.height // 6
        src_rect = Rectangle(self.tile_id[0] * frame_width, self.tile_id[1] * frame_height, frame_width, frame_height)
        dest_rect = Rectangle(self.x-TILE_SIZE/2, self.y-TILE_SIZE/2, TILE_SIZE, TILE_SIZE)
        draw_texture_pro(tex, src_rect, dest_rect, Vector2(0, 0), 0.0, WHITE)