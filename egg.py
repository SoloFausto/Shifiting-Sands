import random
import math
from raylib import *
from pyray import *
from settings import *
class Egg:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        pass
    def draw(self):
        tex = TEXTURES["egg"]
        src_rect = Rectangle(0, 0, tex.width, tex.height)
        dest_rect = Rectangle(self.x, self.y, 39, 20)
        draw_texture_pro(tex, src_rect, dest_rect, Vector2(0, 0), 0.0, WHITE)