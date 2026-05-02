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
        self.draw_coins()
        # tex = TEXTURES["gems"]
        # frame_width = tex.width // 8

        # if self.vx > 0: # Moving Right
        #     src_rect = Rectangle(self.draw_state * frame_width, 0, frame_width, tex.height)
            

        # else: # Moving Left
        #     src_rect = Rectangle(self.draw_state * frame_width, 0, frame_width * -1, tex.height)
            
        
            
        # scale = self.height / 32.0
        # draw_width = frame_width * scale
        # draw_height = tex.height * scale

        # dest_rect = Rectangle(self.x + self.width / 2, self.y + self.height, draw_width, draw_height)
        # origin = Vector2(draw_width / 2, draw_height)
        # draw_texture_pro(tex, src_rect, dest_rect, origin, 0.0, WHITE)

    def draw_coins(self):
        """Draws the active coins as small yellow diamonds (polygons)."""
        radius = TILE_SIZE * 0.3 / 2 
        v1 = Vector2(self.x, self.y - radius * 2)
        v2 = Vector2(self.x + radius * 1.5, self.y)
        v3 = Vector2(self.x, self.y + radius * 2)
        v4 = Vector2(self.x - radius * 1.5, self.y)
        
        DrawTriangle(v1, v2, v4, YELLOW)
        DrawTriangle(v2, v3, v4, GOLD)
        
        DrawLineV(v1, v3, BLACK)
        DrawLineV(v2, v4, BLACK)