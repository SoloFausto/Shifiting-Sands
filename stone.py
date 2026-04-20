import math
from raylib import *
from settings import *
from sand import SAND_SIZE

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

    def update(self, delta_time: float, level, sand):
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

        gx = int(self.x / SAND_SIZE)
        gy = int(self.y / SAND_SIZE)
        if (gx, gy) in sand.occupied:
            self.active = False
            self.toggle_sand_clump_active(sand, gx, gy)
           
           
    def toggle_sand_clump_active(self, sand, gx, gy):
        colided_grain = [g for g in sand.grains if g.gx == gx and g.gy == gy][0]
        colided_grain.active = True                    
        while True:
            found_new = False
            for other in sand.grains:
                if other.active:
                    continue
                if abs(other.gx - colided_grain.gx) <= 1 and abs(other.gy - colided_grain.gy) <= 1:
                    other.active = True
                    colided_grain = other
                    found_new = True
                    break
            if not found_new:
                break

    def draw(self):
        if self.active:
            DrawCircle(int(self.x), int(self.y), STONE_RADIUS, DARKGRAY)
            DrawCircleLines(int(self.x), int(self.y), STONE_RADIUS, BLACK)
