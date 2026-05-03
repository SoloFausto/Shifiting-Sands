import random
from raylib import *
from pyray import *
from settings import *
from mineable import STONE_SIZE

class Dynamite:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 0.0
        self.exploded = False
        self.exploding = False
        self.frame = 1
    
    def update(self, delta_time):
        if self.exploding:
            self.timer += delta_time
            if self.timer >= 0.05:  # change frame roughly every 0.05s
                self.timer = 0.0
                self.frame += 1
                if self.frame >= 6:
                    self.exploding = False
                    self.exploded = True
            
    def draw(self):
        if self.exploded:
            return
            
        if self.exploding:
            tex = TEXTURES["dynamite_explosion"]
            frame_width = 32
            scale = 3
            src_rect = Rectangle(self.frame * frame_width, 0, frame_width, tex.height)
            dest_rect = Rectangle(self.x - (frame_width*scale) / 2, self.y - tex.height / 2, frame_width * scale, tex.height * scale)
            draw_texture_pro(tex, src_rect, dest_rect, Vector2(0, 0), 0.0, WHITE)
        else:
            tex = TEXTURES["dynamite"]
            dest_rect = Rectangle(self.x - tex.width / 2, self.y - tex.height / 2, tex.width, tex.height)
            draw_texture_pro(tex, Rectangle(0, 0, tex.width, tex.height), dest_rect, Vector2(0, 0), 0.0, WHITE)
        
    def explode(self, level, sand, mineable,player,enemies):
        if self.exploding or self.exploded:
            return
        self.exploding = True
        self.frame = 0
        self.timer = 0.0
        
        explosion_radius = TILE_SIZE * 1.25
        
        # Check for sand and mineable grains within explosion radius
        for grain in sand.grains:
            grain_x = grain.gx * SAND_SIZE + SAND_SIZE / 2
            grain_y = grain.gy * SAND_SIZE + SAND_SIZE / 2
            dist = ((grain_x - self.x) ** 2 + (grain_y - self.y) ** 2) ** 0.5
            if dist <= explosion_radius and (grain.gx, grain.gy) in sand.occupied:
                sand.toggle_sand_clump_active(grain.gx, grain.gy)
        
        for grain in mineable.grains:
            grain_x = grain.gx * STONE_SIZE + STONE_SIZE / 2
            grain_y = grain.gy * STONE_SIZE + STONE_SIZE / 2
            dist = ((grain_x - self.x) ** 2 + (grain_y - self.y) ** 2) ** 0.5
            if dist <= explosion_radius and (grain.gx, grain.gy) in mineable.occupied:
                mineable.toggle_mineable_clump_active(grain.gx, grain.gy)
        
        player_center_x = player.x + player.width / 2
        player_center_y = player.y + player.height / 2
        dist = ((player_center_x - self.x) ** 2 + (player_center_y - self.y) ** 2) ** 0.5
        if dist <= explosion_radius:
            player.reset()
            
        for enemy in enemies:
            enemy_center_x = enemy.x + enemy.width / 2
            enemy_center_y = enemy.y + enemy.height / 2
            dist = ((enemy_center_x - self.x) ** 2 + (enemy_center_y - self.y) ** 2) ** 0.5
            if dist <= explosion_radius:
                enemies.pop(enemies.index(enemy))