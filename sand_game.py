import raylib
import pyray
from settings import *
from utils import *

from enemy import Enemy
from player import Player
from sand import SandSimulation
from stone import Stone
from mineable import MineableSimulation

class Game():
    def __init__(self):
        self.isGameOver = True
        self.game_level, self.collectibles, self.enemies, sand_spawns,mineable_spawns = parse_level(LEVEL_PATH)
        self.sand = SandSimulation()
        self.mineable = MineableSimulation()
        for col, row in sand_spawns:
            self.sand.spawn_block(col, row)
        for col, row in mineable_spawns:
            self.mineable.spawn_block(col, row)
        TEXTURES["block"] = load_texture("assets/sand.png")
        TEXTURES["bg"] = load_texture("assets/bg.png")
        TEXTURES["player_idle"] = load_texture("assets/idle.png")
        TEXTURES["player_walk"] = load_texture("assets/walking.png")
        TEXTURES["player_jump"] = load_texture("assets/jumping.png")
        TEXTURES["player_mine"] = load_texture("assets/mine.png")
        TEXTURES["player_throw"] = load_texture("assets/rock_throw.png")
        TEXTURES["enemy"] = load_texture("assets/enemy.png")
        # Game State Variables
        # Player starts at TILE_SIZE * 2, TILE_SIZE * 2
        self.player = Player(TILE_SIZE * 2, TILE_SIZE * 2) 
        self.stones: list[Stone] = []
        self.score = 0
        self.game_state = "PLAYING"
        
        # --- Camera Initialization ---
        self.camera = Camera2D()
        self.camera.target = Vector2(self.player.x, self.player.y + self.player.height / 2) 
        self.camera.offset = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) 
        self.camera.rotation = 0.0
        self.camera.zoom = 1.0
        
    def update(self):
        delta_time = GetFrameTime()
        
        # --- Update ---
        if self.game_state == "PLAYING":
            self.player.update(delta_time, self.game_level, self.sand,self.mineable)
            
            # Update Enemies
            for enemy in self.enemies:
                enemy.update(delta_time, self.game_level, self.player, self.enemies)

            self.sand.update(self.game_level,self.mineable)
            self.mineable.update(self.game_level)

            # Throw stone toward world-space mouse on left click
            if IsMouseButtonPressed(MOUSE_BUTTON_LEFT):
                self.player.is_throwing = True
                self.player.is_mining = False
                self.player.action_timer = 0.0
                rock_lifetime = 5.0
                is_mining = False

                self.spawn_stone(rock_lifetime,is_mining)
            
            if IsKeyDown(KEY_E):
                self.player.is_throwing = False
                self.player.is_mining = True
                self.player.action_timer = 0.0
                rock_lifetime = 0.1
                is_mining = True
                self.spawn_stone(rock_lifetime,is_mining)
            
            


            for stone in self.stones:
                stone.update(delta_time, self.game_level, self.sand,self.mineable)
            self.stones = [s for s in self.stones if s.active]

            self.update_camera(WORLD_WIDTH, WORLD_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT)

            # Check for coin collection
            collected_indices = self.player.check_collection(self.collectibles)
            if collected_indices:
                for index in sorted(collected_indices, reverse=True):
                    self.collectibles.pop(index)
                    self.score += 10
            
            # Check for enemy collisions
            if self.player.check_enemy_collision(self.enemies):
                # Death/Reset mechanic: Penalty and restart
                self.player.reset()
                self.score -= 50 
                if self.score < 0: self.score = 0
                
            for enemy in self.enemies:
                if check_sand_crush(self.sand,enemy.get_rect()):
                    self.enemies.pop(self.enemies.index(enemy))
                    self.score += 20
                    break


            if check_sand_crush(self.sand,self.player.get_rect()):
                self.player.reset()
                self.score -= 20 
                if self.score < 0: self.score = 0
    
    def spawn_stone(self, rock_lifetime, is_mining):
        mouse_screen = GetMousePosition()
        mouse_world = GetScreenToWorld2D(mouse_screen, self.camera)
        cx = self.player.x + self.player.width / 2
        cy = self.player.y + self.player.height / 2
        self.stones.append(Stone(cx, cy, mouse_world.x, mouse_world.y, rock_lifetime, is_mining))
        
    def draw(self):
        ClearBackground(Color(208,176,128,255))
        # Start the 2D camera mode
        BeginMode2D(self.camera)
        draw_texture_pro(TEXTURES["bg"], 
                    Rectangle(0, 0, TEXTURES["bg"].width, TEXTURES["bg"].height),
                    Rectangle(0, 0, WORLD_WIDTH, WORLD_HEIGHT/2 + 1200),
                    Vector2(0, 0), 0.0, WHITE)

        # 1. Draw the Level
        self.draw_level(self.game_level)

        # 2. Draw Sand
        self.sand.draw()

        # 3. Draw Mineable
        self.mineable.draw()
        
        # 4. Draw Collectibles
        self.draw_coins(self.collectibles)

        # 5. Draw Enemies
        for enemy in self.enemies:
            enemy.draw()

        # 6. Draw Stones
        for stone in self.stones:
            stone.draw()

        # 7. Draw Player
        self.player.draw()
        
        # End the 2D camera mode
        EndMode2D()
        
        # 5. Draw HUD (Drawn on screen, outside of BeginMode2D)
        score_text = f"Score: {self.score}".encode('utf-8')
        DrawText(score_text, SCREEN_WIDTH - MeasureText(score_text, 20) - 10, 10, 20, BLACK)
        
        debug_text = f"Grounded: {self.player.is_grounded} | Enemies: {len(self.enemies)}".encode('utf-8')
        DrawText(debug_text, 10, 10, 20, BLACK) 

    
    def draw_level(self, level):
        """Draws the solid tiles of the level map."""
        for row in range(TILE_ROWS):
            for col in range(TILE_COLS):
                tile_value = level[row][col]
                if tile_value == TILE_SOLID:
                    x = col * TILE_SIZE
                    y = row * TILE_SIZE
                    
                    if "block" in TEXTURES:
                        draw_texture_pro(TEXTURES["block"], 
                                        Rectangle(0, 0, TEXTURES["block"].width, TEXTURES["block"].height),
                                        Rectangle(x, y, TILE_SIZE, TILE_SIZE),
                                        Vector2(0, 0), 0.0, WHITE)
                    else:
                        DrawRectangle(x, y, TILE_SIZE, TILE_SIZE, BROWN)
                        DrawRectangleLines(x, y, TILE_SIZE, TILE_SIZE, BLACK)
                    
    def draw_coins(self, coins):
        """Draws the active coins as small yellow diamonds (polygons)."""
        radius = TILE_SIZE * 0.3 / 2 
        
        for cx, cy in coins:
            v1 = Vector2(cx, cy - radius * 2)
            v2 = Vector2(cx + radius * 1.5, cy)
            v3 = Vector2(cx, cy + radius * 2)
            v4 = Vector2(cx - radius * 1.5, cy)
            
            DrawTriangle(v1, v2, v4, YELLOW)
            DrawTriangle(v2, v3, v4, GOLD)
            
            DrawLineV(v1, v3, BLACK)
            DrawLineV(v2, v4, BLACK)


    def update_camera(self, world_width, world_height, screen_width, screen_height):
        """Centers the camera on the player and clamps the camera's target to the world bounds."""
        
        self.camera.target.x = self.player.x + self.player.width / 2
        self.camera.target.y = self.player.y - self.player.height * 2

        min_x = screen_width / 2
        max_x = world_width - screen_width / 2
        
        if self.camera.target.x < min_x:
            self.camera.target.x = min_x
        if self.camera.target.x > max_x:
            self.camera.target.x = max_x

        min_y = screen_height / 2
        max_y = world_height - screen_height / 2
        
        if self.camera.target.y < min_y:
            self.camera.target.y = min_y
        if self.camera.target.y > max_y:
            self.camera.target.y = max_y
        
        self.camera.offset.x = screen_width / 2
        self.camera.offset.y = screen_height / 2

