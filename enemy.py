import random
import math
from raylib import *
from pyray import *
from settings import *
class Enemy:
    def __init__(self, x, y):
        # Position (top-left for collision)
        self.x = x
        self.y = y
        self.width = TILE_SIZE * 0.7
        self.height = TILE_SIZE * 0.7
        
        # Physics/Movement
        self.vx = getattr(self, 'vx', ENEMY_SPEED) # Start moving right
        self.vy = 0.0 
        self.is_grounded = False
        self.animation_timer = 0.0
        self.draw_state = 0 # For animation frames

    def get_rect(self):
        """Returns the enemy's collision bounding box."""
        return (self.x, self.y, self.width, self.height)

    def update(self, delta_time, level,player,enemies,sand,mineable):
        # 1. Apply Gravity
        if self.is_grounded:
            self.vy = 0.0
        self.vy += GRAVITY * delta_time
        self.is_grounded = False 

        # 2. Apply Movement 

        # Apply X movement
        self.x += self.vx * delta_time
        self.handle_tile_collision(level, 'X')
        self.handle_enemy_collision(enemies, 'X')
        self.handle_sand_collision(sand, sand.toggle_sand_clump_active, 'X', SAND_SIZE)
        self.handle_sand_collision(mineable, lambda gx, gy: None, 'X', STONE_SIZE)
        # Apply Y movement
        self.y += self.vy * delta_time
        self.handle_tile_collision(level, 'Y')
        self.handle_enemy_collision(enemies, 'Y')
        self.handle_sand_collision(sand, sand.toggle_sand_clump_active, 'Y', SAND_SIZE)
        self.handle_sand_collision(mineable, lambda gx, gy: None, 'Y', STONE_SIZE)
        
        if self.vx != 0.0:
            self.animation_timer += delta_time
            if self.animation_timer > 0.1: # 0.1s per frame
                self.draw_state = (self.draw_state + 1) % 3
                self.animation_timer = 0.0
        else:
            self.draw_state = 0
            self.animation_timer = 0.0
                 
    def handle_tile_collision(self, level, axis):
        """Enemy collision: reverses direction on horizontal wall contact, respects vertical floor contact."""
        enemy_rect = self.get_rect()
        px, py, pw, ph = enemy_rect
        
        min_col = int(px / TILE_SIZE)
        max_col = int((px + pw) / TILE_SIZE)
        min_row = int(py / TILE_SIZE)
        max_row = int((py + ph) / TILE_SIZE)

        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                
                if row < 0 or row >= TILE_ROWS or col < 0 or col >= TILE_COLS:
                    continue
                
                if level[row][col] == TILE_SOLID:
                    tile_rect = (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    
                    if CheckCollisionRecs(enemy_rect, tile_rect):
                        
                        if axis == 'X':
                            # Reverses direction on horizontal collision
                            if self.vx > 0:
                                self.x = tile_rect[0] - self.width
                            elif self.vx < 0:
                                self.x = tile_rect[0] + TILE_SIZE
                            self.vx *= -1 # Reverse direction
                            
                        elif axis == 'Y':
                            if self.vy >= 0: # Hitting Ground
                                self.y = tile_rect[1] - self.height
                                self.is_grounded = True 
                                
                            self.vy = 0.0 
                            
                        enemy_rect = self.get_rect() # Update rect after resolution

    def handle_enemy_collision(self, enemies, axis):
        enemy_rect = self.get_rect()
        for other in enemies:
            if other == self:
                continue
            other_rect = other.get_rect()
            if CheckCollisionRecs(enemy_rect, other_rect):
                if axis == 'X':
                    if self.x < other.x:
                        self.x = other.x - self.width
                        self.vx = -abs(self.vx)
                        other.vx = abs(other.vx)
                    else:
                        self.x = other.x + other.width
                        self.vx = abs(self.vx)
                        other.vx = -abs(other.vx)
                elif axis == 'Y':
                    if self.y < other.y:
                        self.y = other.y - self.height
                        self.is_grounded = True
                        self.vy = 0.0
                    else:
                        self.y = other.y + other.height
                        self.vy = 0.0
                enemy_rect = self.get_rect()
    def handle_sand_collision(self, sand, toggle_clump_active, axis, size):
        # Function largely done with the help of AI.
        px, py, pw, ph = self.x, self.y, self.width, self.height
        min_gx = int(px / size)
        max_gx = int((px + pw - 1) / size)
        min_gy = int(py / size)
        max_gy = int((py + ph - 1) / size)

        if axis == 'Y':
            # Find the topmost grain (smallest gy) that overlaps the player.
            top_gy = None
            for gy in range(min_gy, max_gy + 1):
                for gx in range(min_gx, max_gx + 1):
                    if (gx, gy) not in sand.occupied:
                        continue
                    g_rect = (gx * size, gy * size, size, size)
                    if CheckCollisionRecs((self.x, self.y, self.width, self.height), g_rect):
                        if top_gy is None or gy < top_gy:
                            top_gy = gy
                        break
            if top_gy is not None:
                if self.vy >= 0:
                    self.y = top_gy * size - self.height
                    self.is_grounded = True
                else:
                    self.y = (top_gy + 1) * size
                self.vy = 0.0
            elif self.vy >= 0:
                feet_y = self.y + self.height
                probe_gy = int(feet_y / size)
                for g in [probe_gy, probe_gy + 1]:
                    for gx in range(min_gx, max_gx + 1):
                        if (gx, g) in sand.occupied:
                            toggle_clump_active(gx, g)
                            if g * size - feet_y < size:
                                self.is_grounded = True
                                return

        elif axis == 'X':
            top_gy = None
            top_gx = None
            for gy in range(min_gy, max_gy + 1):
                for gx in range(min_gx, max_gx + 1):
                    if (gx, gy) not in sand.occupied:
                        continue
                    g_rect = (gx * size, gy * size, size, size)
                    if CheckCollisionRecs((self.x, self.y, self.width, self.height), g_rect):
                        if top_gy is None or gy < top_gy:
                            top_gy = gy
                            top_gx = gx
                        break
            if top_gy is None:
                return
            # Wall — block horizontal movement
            if self.vx > 0:
                self.x = top_gx * size - self.width
            elif self.vx < 0:
                self.x = (top_gx + 1) * size
            self.vx = 0.0
    def draw(self):
        tex = TEXTURES["enemy"]
        frame_width = tex.width // 8

        if self.vx > 0: # Moving Right
            src_rect = Rectangle(self.draw_state * frame_width, 0, frame_width, tex.height)
            

        else: # Moving Left
            src_rect = Rectangle(self.draw_state * frame_width, 0, frame_width * -1, tex.height)
            
        
            
        scale = self.height / 32.0
        draw_width = frame_width * scale
        draw_height = tex.height * scale

        dest_rect = Rectangle(self.x + self.width / 2, self.y + self.height, draw_width, draw_height)
        origin = Vector2(draw_width / 2, draw_height)
        draw_texture_pro(tex, src_rect, dest_rect, origin, 0.0, WHITE)

