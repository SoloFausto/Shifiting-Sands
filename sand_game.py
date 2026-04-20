import raylib
import pyray
from settings import *
from utils import parse_level
from enemy import Enemy
from player import Player
from sand import SandSimulation

class Game():
    def __init__(self):
        self.isGameOver = True
        self.game_level, self.collectibles, self.enemies, sand_spawns = parse_level(LEVEL_PATH)
        self.sand = SandSimulation()
        for col, row in sand_spawns:
            self.sand.spawn_block(col, row)
        TEXTURES["block"] = load_texture("assets/block.png")
        TEXTURES["bg"] = load_texture("assets/bg.png")
        # Game State Variables
        # Player starts at TILE_SIZE * 2, TILE_SIZE * 2
        self.player = Player(TILE_SIZE * 2, TILE_SIZE * 2) 
        self.score = 0
        self.game_state = "PLAYING" 
        
        # --- Camera Initialization ---
        self.camera = Camera2D()
        self.camera.target = Vector2(self.player.x, self.player.y) 
        self.camera.offset = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) 
        self.camera.rotation = 0.0
        self.camera.zoom = 1.0
        
    def update(self):
        delta_time = GetFrameTime()
        
        # --- Update ---
        if self.game_state == "PLAYING":
            self.player.update(delta_time, self.game_level, self.sand)
            
            # Update Enemies
            for enemy in self.enemies:
                enemy.update(delta_time, self.game_level, self.player, self.enemies)

            self.sand.update(self.game_level)
            self.update_camera(WORLD_WIDTH, WORLD_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT)

            # Check for coin collection
            collected_indices = self.player.check_collection(self.collectibles)
            if collected_indices:
                for index in sorted(collected_indices, reverse=True):
                    self.collectibles.pop(index)
                    self.score += 10
            
            # Check for enemy collision (Stomp/Death/Reset)
            hit_type, enemy_index = self.player.check_enemy_collision(self.enemies)

            if hit_type == "STOMP":
                # Stomp mechanic: Remove enemy, score, and bounce
                self.enemies.pop(enemy_index)
                self.score += 100 
                self.player.vy = STOMP_BOUNCE # Player bounces up
                
            elif hit_type == "LETHAL":
                # Death/Reset mechanic: Penalty and restart
                self.player.reset()
                self.score -= 50 
                if self.score < 0: self.score = 0
            
        
    def draw(self):
        ClearBackground(SKYBLUE)
        # Start the 2D camera mode
        BeginMode2D(self.camera)
        draw_texture_pro(TEXTURES["bg"], 
                    Rectangle(0, 0, TEXTURES["bg"].width, TEXTURES["bg"].height),
                    Rectangle(0, 0, WORLD_WIDTH, WORLD_HEIGHT),
                    Vector2(0, 0), 0.0, WHITE)

        # 1. Draw the Level
        self.draw_level(self.game_level)

        # 2. Draw Sand
        self.sand.draw()

        # 4. Draw Collectibles
        self.draw_coins(self.collectibles)

        # 5. Draw Enemies
        for enemy in self.enemies:
            enemy.draw()

        # 6. Draw Player
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
        self.camera.target.y = self.player.y + self.player.height / 2

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

