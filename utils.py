from enemy import Enemy
from settings import *

def parse_level(path):
    """
    Parses the level map, extracts all dynamic entities (coins, enemies, sand blocks),
    replaces their spawn points with air, and returns the modified collision map and entity lists.
    """
    with open(path, 'r') as file:
        level = [[int(char) for char in line.strip()] for line in file.readlines()]

    coins = []
    enemies = []
    sand_spawns = []  # list of (tile_col, tile_row)
    new_level = [row[:] for row in level]

    for r in range(TILE_ROWS):
        for c in range(TILE_COLS):
            x = c * TILE_SIZE
            y = r * TILE_SIZE

            if new_level[r][c] == TILE_ENEMY:
                enemies.append(Enemy(x, y))
                new_level[r][c] = TILE_AIR

            elif new_level[r][c] == TILE_SAND_BLOCK:
                sand_spawns.append((c, r))
                new_level[r][c] = TILE_AIR

    return new_level, coins, enemies, sand_spawns
