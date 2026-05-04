from enemy import Enemy
from gem import Gems
from settings import *
from sand import SAND_SIZE
from pyray import *
from egg import Egg

def parse_level(path):
    """
    Parses the level map, extracts all dynamic entities (coins, enemies, sand blocks),
    replaces their spawn points with air, and returns the modified collision map and entity lists.
    """
    tile_rows = len(open(path).readlines())
    tile_cols = len(open(path).readline().strip())
    world_width = tile_cols * TILE_SIZE
    world_height = tile_rows * TILE_SIZE

    with open(path, 'r') as file:
        level = [[int(char) for char in line.strip()] for line in file.readlines()]

    coins = []
    enemies = []
    sand_spawns = []  # list of (tile_col, tile_row)
    mineable_spawns = []  # list of (tile_col, tile_row)
    dynamite_spawns = []  # list of (tile_col, tile_row)
    eggs = []  # list of (tile_col, tile_row)
    new_level = [row[:] for row in level]

    for r in range(tile_rows):
        for c in range(tile_cols):
            x = c * TILE_SIZE
            y = r * TILE_SIZE

            if new_level[r][c] == TILE_ENEMY:
                enemies.append((c,r))
                new_level[r][c] = TILE_AIR

            elif new_level[r][c] == TILE_SAND_BLOCK:
                sand_spawns.append((c, r))
                new_level[r][c] = TILE_AIR
            elif new_level[r][c] == TILE_MINEABLE:
                mineable_spawns.append((c, r))
                new_level[r][c] = TILE_AIR
            elif new_level[r][c] == TILE_COIN:
                coins.append(Gems(x + TILE_SIZE / 2, y + TILE_SIZE / 2))
                new_level[r][c] = TILE_AIR
            elif new_level[r][c] == TILE_DYNAMITE:
                dynamite_spawns.append((c, r))
                new_level[r][c] = TILE_AIR
            elif new_level[r][c] == TILE_EGG:
                eggs.append((c, r))
                new_level[r][c] = TILE_AIR

    return new_level, coins, enemies, sand_spawns, mineable_spawns, dynamite_spawns, eggs, tile_rows, tile_cols, world_width, world_height

    
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