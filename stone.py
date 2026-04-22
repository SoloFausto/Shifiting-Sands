import math
from raylib import *
from settings import *
from sand import SAND_SIZE
from mineable import STONE_SIZE

STONE_RADIUS = 3
STONE_SPEED = 900.0


class Stone:
    def __init__(self, x: float, y: float, target_x: float, target_y: float):
        self.x = x
        self.y = y
        dx = target_x - x
        dy = target_y - y
        dist = math.sqrt(dx * dx + dy * dy) or 1.0
        self.vx = (dx / dist) * STONE_SPEED
        self.vy = (dy / dist) * STONE_SPEED
        self.active = True

    def update(self, delta_time: float, level, sand, mineable):
        #trajectory largely from what we did in class
        if not self.active:
            return

        self.vy += GRAVITY * delta_time
        self.x += self.vx * delta_time
        self.y += self.vy * delta_time

        if self.x < 0 or self.x >= WORLD_WIDTH or self.y < 0 or self.y >= WORLD_HEIGHT:
            self.active = False
            return

        col = int(self.x / TILE_SIZE)
        row = int(self.y / TILE_SIZE)
        if 0 <= row < TILE_ROWS and 0 <= col < TILE_COLS and level[row][col] == TILE_SOLID:
            self.active = False
            return

        sand_gx = int(self.x / SAND_SIZE)
        sand_gy = int(self.y / SAND_SIZE)
        if (sand_gx, sand_gy) in sand.occupied:
            self.active = False
            self.toggle_sand_clump_active(sand, sand_gx, sand_gy)
            return

        mineable_gx = int(self.x / STONE_SIZE)
        mineable_gy = int(self.y / STONE_SIZE)
        if (mineable_gx, mineable_gy) in mineable.occupied:
            self.active = False
            self.toggle_mineable_clump_active(mineable, mineable_gx, mineable_gy)
            
            
           
           
    def toggle_sand_clump_active(self, sand, gx, gy):
        colided_grain = [g for g in sand.grains if g.gx == gx and g.gy == gy][0]
        
        colided_grain.active = True       
                     
        to_visit = [colided_grain]

        while to_visit:
            current = to_visit.pop()
            for other in sand.grains:
                if other.active:
                    continue
                if abs(other.gx - current.gx) <= 1 and abs(other.gy - current.gy) <= 1:
                    other.active = True
                    to_visit.append(other)
    
    def toggle_mineable_clump_active(self, mineable, gx, gy):
        colided_grain = [g for g in mineable.grains if g.gx == gx and g.gy == gy][0]
        
        colided_grain.active = True       
                     
        to_visit = [colided_grain]

        while to_visit:
            current = to_visit.pop()
            for other in mineable.grains:
                if other.active:
                    continue
                if abs(other.gx - current.gx) <= 2 and abs(other.gy - current.gy) <= 2:
                    other.active = True
                    

    def draw(self):
        if self.active:
            DrawCircle(int(self.x), int(self.y), STONE_RADIUS, DARKGRAY)
            DrawCircleLines(int(self.x), int(self.y), STONE_RADIUS, BLACK)
