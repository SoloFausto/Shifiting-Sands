import raylib
import pyray
class Game():
    def __init__(self):
        self.isGameOver = True
        game_level, collectibles, enemies = parse_level(LEVEL_PATH)
        self.block_texture = load_texture("assets/block.png")
        self.background_texture = load_texture("assets/bg.png")
        
    def update(self):
        pass
        
    def draw(self):
        pass