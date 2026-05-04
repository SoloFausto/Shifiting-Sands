import random
from raylib import *
from settings import *
from mineable import STONE_SIZE

_SAND_COLORS = [
    Color(194, 178, 128, 255),
    Color(210, 194, 140, 255),
    Color(180, 164, 115, 255),
    Color(220, 200, 150, 255),
    Color(200, 185, 135, 255),
]




class SandGrain:

    def __init__(self, gx, gy):
        self.gx = gx
        self.gy = gy
        self.active = False
        self.color = [random.choice(_SAND_COLORS) for _ in range(4)]


class SandSimulation:
    def __init__(self,tile_rows,tile_cols,world_width,world_height):
        self.grains: list[SandGrain] = []
        self.occupied: set[tuple[int, int]] = set()
        self.tile_rows = tile_rows
        self.tile_cols = tile_cols
        self.world_width = world_width
        self.world_height = world_height
        self.world_grain_width = (self.tile_cols * TILE_SIZE) // SAND_SIZE
        self.world_grain_height = (self.tile_rows * TILE_SIZE) // SAND_SIZE

    def _overlaps_mineable(self, gx: int, gy: int, mineable) -> bool:
        # got some help from ai for this function
        min_mx = (gx * SAND_SIZE) // STONE_SIZE
        max_mx = ((gx + 1) * SAND_SIZE - 1) // STONE_SIZE
        min_my = (gy * SAND_SIZE) // STONE_SIZE
        max_my = ((gy + 1) * SAND_SIZE - 1) // STONE_SIZE

        for mx in range(min_mx, max_mx + 1):
            for my in range(min_my, max_my + 1):
                if (mx, my) in mineable.occupied:
                    return True
        return False

    def spawn_block(self, tile_col: int, tile_row: int):
        grains_per_row = TILE_SIZE // SAND_SIZE
        for i in range(grains_per_row):
            for j in range(grains_per_row):
                gx = (tile_col * TILE_SIZE + i * SAND_SIZE) // SAND_SIZE
                gy = (tile_row * TILE_SIZE + j * SAND_SIZE) // SAND_SIZE
                grain = SandGrain(gx, gy)
                self.grains.append(grain)
                self.occupied.add((gx, gy))

    def _is_blocked(self, gx: int, gy: int, level,mineable) -> bool:
        if gx < 0 or gx >= self.world_grain_width or gy >= self.world_grain_height:
            return True
        if (gx, gy) in self.occupied:
            return True

        if self._overlaps_mineable(gx, gy, mineable):
            return True
        col = (gx * SAND_SIZE) // TILE_SIZE
        row = (gy * SAND_SIZE) // TILE_SIZE
        if 0 <= row < self.tile_rows and 0 <= col < self.tile_cols:
            return level[row][col] == TILE_SOLID
        return True

    def remove_sand_clump(self, gx, gy):
        chunk_radius = 1
        to_remove = set()
        self.toggle_sand_clump_active(gx, gy)  # Activate the initial grain to find the clump
        
        # Find all grains within the small radius around the impact point
        for g in self.grains:
            if abs(g.gx - gx) <= chunk_radius and abs(g.gy - gy) <= chunk_radius:
                to_remove.add(g)
                
        self.grains = [g for g in self.grains if g not in to_remove]
        for g in to_remove:
            self.occupied.discard((g.gx, g.gy))

    def toggle_sand_clump_active(self, gx, gy):
        colided_grain = [g for g in self.grains if g.gx == gx and g.gy == gy][0]
        
        colided_grain.active = True       
                     
        to_visit = [colided_grain]

        while to_visit:
            current = to_visit.pop()
            for other in self.grains:
                if other.active:
                    continue
                if abs(other.gx - current.gx) <= 1 and abs(other.gy - current.gy) <= 1:
                    other.active = True
                    to_visit.append(other)
    

    def update(self, level,mineable):
        # It is important to start at the end https://jason.today/falling-sand
        # accessing the set as a sorted list through a lambda
        ordered_grains = sorted(self.grains, key=lambda g: (g.gy, g.gx), reverse=True)
        for grain in ordered_grains:
            gx, gy = grain.gx, grain.gy

            if not grain.active:
                continue

            if not self._is_blocked(gx, gy + 1, level,mineable):
                self.occupied.discard((gx, gy))
                grain.gy += 1
                self.occupied.add((grain.gx, grain.gy))
            else:
                dirs = [-1, 1]
                for dx in dirs:
                    if not self._is_blocked(gx + dx, gy + 1, level,mineable) and not self._is_blocked(gx + dx, gy, level,mineable):
                        self.occupied.discard((gx, gy))
                        grain.gx += dx
                        grain.gy += 1
                        self.occupied.add((grain.gx, grain.gy))
                        break
    def draw(self):
        for grain in self.grains:
            half_size = SAND_SIZE // 2
            DrawRectangle(
                grain.gx * SAND_SIZE,
                grain.gy * SAND_SIZE,
                half_size,
                half_size,
                grain.color[0],
            )
            DrawRectangle(
                grain.gx * SAND_SIZE + half_size,
                grain.gy * SAND_SIZE,
                half_size,
                half_size,
                grain.color[1],
            )
            DrawRectangle(
                grain.gx * SAND_SIZE,
                grain.gy * SAND_SIZE + half_size,
                half_size,
                half_size,
                grain.color[2],
            )
            DrawRectangle(
                grain.gx * SAND_SIZE + half_size,
                grain.gy * SAND_SIZE + half_size,
                half_size,
                half_size,
                grain.color[3],
            )
