import random
import math
from raylib import *
from pyray import *
from settings import *
from sand import SAND_SIZE
from mineable import STONE_SIZE

STEP_HEIGHT = 20  # max pixel height the player can step up over a sand mound
class Player:
    def __init__(self, x, y):
        # Store starting position for reset
        self.start_x = x 
        self.start_y = y
        # Current position (top-left for collision)
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        
        # Physics
        self.vx = 0.0
        self.vy = 0.0
        self.is_grounded = False
        
        # Facing direction (1 for right, -1 for left)
        self.facing = 1

    def get_rect(self):
        """Returns the player's collision bounding box (top-left, width, height)."""
        return (self.x, self.y, self.width, self.height)

    def update(self, delta_time, level, sand=None,mineable=None):
        # 1. Handle Input (Horizontal Movement)
        self.vx = 0.0
        if IsKeyDown(KEY_LEFT) or IsKeyDown(KEY_A):
            self.vx = -PLAYER_SPEED
            self.facing = -1
        if IsKeyDown(KEY_RIGHT) or IsKeyDown(KEY_D):
            self.vx = PLAYER_SPEED
            self.facing = 1

        # 1.5 Handle Mining Input
        if IsKeyPressed(KEY_F) and mineable:
            mine_width = 40
            mine_height = self.height
            mine_x = self.x + self.width if self.facing == 1 else self.x - mine_width
            mine_y = self.y
            mine_point_x = mine_x + (mine_width / 2)
            mine_point_y = mine_y + (mine_height / 2)
            mine_gx = int(mine_point_x / STONE_SIZE)
            mine_gy = int(mine_point_y / STONE_SIZE)
            if (mine_gx, mine_gy) in mineable.occupied:
                mineable.toggle_mineable_clump_active(mine_gx, mine_gy)
            
            

        # --- Velocity Zeroing for Stability ---
        if self.is_grounded:
            self.vy = 0.0
            
        # 2. Handle Input (Jump)
        if (IsKeyPressed(KEY_SPACE) or IsKeyPressed(KEY_UP)) and self.is_grounded:
            self.vy = JUMP_VELOCITY


        # 3. Apply Gravity
        self.vy += GRAVITY * delta_time
        if self.vy > 1000:
            self.vy = 1000

        # --- Reset grounded state at start of frame update ---
        self.is_grounded = False

        # 4. Apply Movement (Separated for X and Y collision checks)
        
        # Apply X movement
        self.x += self.vx * delta_time
        self.handle_tile_collision(level, 'X')
        if sand:
            self.handle_sand_collision(sand, sand.toggle_sand_clump_active, 'X',SAND_SIZE)
            
        if mineable:
            self.handle_sand_collision(mineable, lambda gx, gy: None, 'X',STONE_SIZE)

        # Apply Y movement
        self.y += self.vy * delta_time
        self.handle_tile_collision(level, 'Y')
        if sand:
            self.handle_sand_collision(sand,sand.toggle_sand_clump_active, 'Y',SAND_SIZE)
        if mineable:
            self.handle_sand_collision(mineable, lambda gx, gy: None, 'Y',STONE_SIZE)

        # --- Safety Clamp to World Bounds ---
        self.x = max(0, min(self.x, WORLD_WIDTH - self.width))
        
    def handle_tile_collision(self, level, axis):
        """Performs AABB collision checks against solid tiles and resolves the collision."""
        player_rect = self.get_rect()
        px, py, pw, ph = player_rect
        
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
                    
                    if CheckCollisionRecs(player_rect, tile_rect):
                        
                        if axis == 'X':
                            if self.vx > 0: # Moving Right
                                self.x = tile_rect[0] - self.width
                            elif self.vx < 0: # Moving Left
                                self.x = tile_rect[0] + TILE_SIZE
                            self.vx = 0.0 
                            
                        elif axis == 'Y':
                            if self.vy >= 0: # Falling (Hitting Ground)
                                self.y = tile_rect[1] - self.height
                                self.is_grounded = True 
                            elif self.vy < 0: # Jumping (Hitting Ceiling)
                                self.y = tile_rect[1] + TILE_SIZE
                                
                            self.vy = 0.0 
                            
                        player_rect = self.get_rect()
                        px, py, pw, ph = player_rect
                        
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
            # Find the topmost blocking grain across all columns the player overlaps.
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
            grain_top_px = top_gy * size
            step = (self.y + self.height) - grain_top_px
            if 0 < step <= STEP_HEIGHT:
                # Step up over the mound
                self.y -= step
            else:
                # Wall — block horizontal movement
                if self.vx > 0:
                    self.x = top_gx * size - self.width
                elif self.vx < 0:
                    self.x = (top_gx + 1) * size
                self.vx = 0.0

    def check_collection(self, collectibles):
        """Checks for collision with coins and returns indices of collected coins."""
        collected_indices = []
        player_rect = self.get_rect()
        coin_collision_size = TILE_SIZE * 0.5
        
        for i, (cx, cy) in enumerate(collectibles):
            coin_x = cx - coin_collision_size / 2
            coin_y = cy - coin_collision_size / 2
            coin_rect = (coin_x, coin_y, coin_collision_size, coin_collision_size)
            
            if CheckCollisionRecs(player_rect, coin_rect):
                collected_indices.append(i)
                
        return collected_indices
    
    def check_enemy_collision(self, enemies):
        player_rect = self.get_rect()
        px, py, pw, ph = player_rect
        
        for enemy in enemies:
            enemy_rect = enemy.get_rect()
            
            if CheckCollisionRecs(player_rect, enemy_rect):
                    return True
                    
        return False

    
    def reset(self):
        """Resets the player to their starting position."""
        self.x = self.start_x
        self.y = self.start_y
        self.vx = 0.0
        self.vy = 0.0
        self.is_grounded = False

    def draw(self):
        """Draws the player at their world coordinates."""
        DrawRectangle(int(self.x), int(self.y), int(self.width), int(self.height), BLUE) 
        if self.is_grounded:
             DrawRectangleLines(int(self.x), int(self.y), int(self.width), int(self.height), WHITE)
        else:
             DrawRectangleLines(int(self.x), int(self.y), int(self.width), int(self.height), GRAY)
