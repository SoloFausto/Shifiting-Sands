from enemy import Enemy
from settings import *
from sand import SAND_SIZE

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
    mineable_spawns = []  # list of (tile_col, tile_row)
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
            elif new_level[r][c] == TILE_MINEABLE:
                mineable_spawns.append((c, r))
                new_level[r][c] = TILE_AIR
            elif new_level[r][c] == TILE_COIN:
                coins.append((x + TILE_SIZE / 2, y + TILE_SIZE / 2))
                new_level[r][c] = TILE_AIR

    return new_level, coins, enemies, sand_spawns, mineable_spawns

def check_sand_crush(sand,rect):

    rect_x, rect_y, rect_w, rect_h = rect
    for grain in sand.grains:
        if not grain.active:
            continue

        grain_px = grain.gx * SAND_SIZE
        grain_py = grain.gy * SAND_SIZE
        grain_rect = (grain_px, grain_py, SAND_SIZE, SAND_SIZE)

        player_killable_zone = grain_py < (rect_y + rect_h * 0.35)
        if CheckCollisionRecs(rect, grain_rect):
            if player_killable_zone:
                return True
    return False