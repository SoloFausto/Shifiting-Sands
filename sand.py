import random
from raylib import *
from settings import *

SAND_SIZE = 4  # pixels per grain

_SAND_COLORS = [
    Color(194, 178, 128, 255),
    Color(210, 194, 140, 255),
    Color(180, 164, 115, 255),
    Color(220, 200, 150, 255),
    Color(200, 185, 135, 255),
]

_WORLD_GW = (TILE_COLS * TILE_SIZE) // SAND_SIZE
_WORLD_GH = (TILE_ROWS * TILE_SIZE) // SAND_SIZE


class SandGrain:

    def __init__(self, gx, gy):
        self.gx = gx
        self.gy = gy
        self.color = random.choice(_SAND_COLORS)


class SandSimulation:
    def __init__(self):
        self.grains: list[SandGrain] = []
        self.occupied: set[tuple[int, int]] = set()

    def spawn_block(self, tile_col: int, tile_row: int):
        grains_per_row = TILE_SIZE // SAND_SIZE
        for i in range(grains_per_row):
            for j in range(grains_per_row):
                gx = (tile_col * TILE_SIZE + i * SAND_SIZE) // SAND_SIZE
                gy = (tile_row * TILE_SIZE + j * SAND_SIZE) // SAND_SIZE
                grain = SandGrain(gx, gy)
                self.grains.append(grain)
                self.occupied.add((gx, gy))

    def _is_blocked(self, gx: int, gy: int, level) -> bool:
        if gx < 0 or gx >= _WORLD_GW or gy >= _WORLD_GH:
            return True
        if (gx, gy) in self.occupied:
            return True
        col = (gx * SAND_SIZE) // TILE_SIZE
        row = (gy * SAND_SIZE) // TILE_SIZE
        if 0 <= row < TILE_ROWS and 0 <= col < TILE_COLS:
            return level[row][col] == TILE_SOLID
        return True

    def update(self, level):
        # It is important to start at the end https://jason.today/falling-sand
        # accessing the set as a sorted list through a lambda
        for grain in sorted(self.grains, key=lambda g: -1 * g.gy):
            gx, gy = grain.gx, grain.gy

            if not self._is_blocked(gx, gy + 1, level):
                self.occupied.discard((gx, gy))
                grain.gy += 1
                self.occupied.add((grain.gx, grain.gy))
            else:
                dirs = [-1, 1]
                # random.shuffle(dirs)
                for dx in dirs:
                    if not self._is_blocked(gx + dx, gy + 1, level):
                        self.occupied.discard((gx, gy))
                        grain.gx += dx
                        grain.gy += 1
                        self.occupied.add((grain.gx, grain.gy))
                        break

    def draw(self):
        for grain in self.grains:
            DrawRectangle(
                grain.gx * SAND_SIZE,
                grain.gy * SAND_SIZE,
                SAND_SIZE,
                SAND_SIZE,
                grain.color,
            )
