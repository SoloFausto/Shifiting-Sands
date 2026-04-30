import random
from raylib import *
from settings import *


_STONE_COLORS = [
    Color(117, 117, 117, 255),
    Color(27, 23, 37, 255),
    Color(41, 40, 0 , 255),
    Color(24, 29, 39, 255),
    Color(9, 3, 2, 255),
]

_WORLD_GW = (TILE_COLS * TILE_SIZE) // STONE_SIZE
_WORLD_GH = (TILE_ROWS * TILE_SIZE) // STONE_SIZE


class StoneGrain:

    def __init__(self, gx, gy):
        self.gx = gx
        self.gy = gy
        self.active = False
        self.color = [random.choice(_STONE_COLORS) for _ in range(4)]


class MineableSimulation:
    def __init__(self):
        self.grains: list[StoneGrain] = []
        self.occupied: set[tuple[int, int]] = set()

    def spawn_block(self, tile_col: int, tile_row: int):
        grains_per_row = TILE_SIZE // STONE_SIZE
        for i in range(grains_per_row):
            for j in range(grains_per_row):
                gx = (tile_col * TILE_SIZE + i * STONE_SIZE) // STONE_SIZE
                gy = (tile_row * TILE_SIZE + j * STONE_SIZE) // STONE_SIZE
                grain = StoneGrain(gx, gy)
                self.grains.append(grain)
                self.occupied.add((gx, gy))

    def _is_blocked(self, gx: int, gy: int, level) -> bool:
        if gx < 0 or gx >= _WORLD_GW or gy >= _WORLD_GH:
            return True
        if (gx, gy) in self.occupied:
            return True
        col = (gx * STONE_SIZE) // TILE_SIZE
        row = (gy * STONE_SIZE) // TILE_SIZE
        if 0 <= row < TILE_ROWS and 0 <= col < TILE_COLS:
            return level[row][col] == TILE_SOLID
        return True
    def toggle_mineable_clump_active(self, gx, gy):
        colided_grain = [g for g in self.grains if g.gx == gx and g.gy == gy][0]
        
        colided_grain.active = True       
                        
        to_visit = [colided_grain]

        while to_visit:
            current = to_visit.pop()
            for other in self.grains:
                if other.active:
                    continue
                if abs(other.gx - current.gx) <= 2 and abs(other.gy - current.gy) <= 2:
                    other.active = True

    def update(self, level):
        # It is important to start at the end https://jason.today/falling-sand
        # accessing the set as a sorted list through a lambda
        ordered_grains = sorted(self.grains, key=lambda g: (g.gy, g.gx), reverse=True)
        for grain in ordered_grains:
            gx, gy = grain.gx, grain.gy

            if grain.active:
                self.occupied.discard((gx, gy))

    def draw(self):
        for grain in self.grains:
            if(grain.active):
                continue
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
