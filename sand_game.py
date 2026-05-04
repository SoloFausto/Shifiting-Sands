import raylib
import pyray
from dynamite import Dynamite
from settings import *
from utils import *

from enemy import Enemy
from player import Player
from sand import SandSimulation
from stone import Stone
from mineable import MineableSimulation

class Game():
    def __init__(self,level_idx,spawn_x, spawn_y,points):
        self.isGameOver = True
        self.game_level, collectibles, enemies, sand_spawns,mineable_spawns, dynamite_spawns, eggs, tile_rows,tile_cols,world_width,world_height = parse_level(LEVEL_PATH[level_idx])
        self.sand = SandSimulation(tile_rows,tile_cols,world_width,world_height)
        self.mineable = MineableSimulation(tile_rows,tile_cols,world_width,world_height)
        self.dynamites: list[Dynamite] = []
        self.enemies: list[Enemy] = []
        self.eggs: list[Egg] = []
        self.collectibles: list[Gems] = []

        for col, row in sand_spawns:
            self.sand.spawn_block(col, row)
        for col, row in mineable_spawns:
            self.mineable.spawn_block(col, row)
        for col, row in dynamite_spawns:
            self.dynamites.append(Dynamite(col * TILE_SIZE + TILE_SIZE / 2, row * TILE_SIZE + TILE_SIZE / 2))
        for col, row in eggs:
            self.eggs.append(Egg(col * TILE_SIZE + TILE_SIZE / 2, row * TILE_SIZE + TILE_SIZE / 2))
        for col, row in enemies:
            self.enemies.append(Enemy(col * TILE_SIZE, row * TILE_SIZE, tile_rows, tile_cols, world_width, world_height))
        for gem in collectibles:
            self.collectibles.append(gem)
        TEXTURES["block"] = load_texture("assets/sand.png")
        TEXTURES["underground"] = load_texture("assets/sand.png")  # Reusing sand or replace with appropriate texture
        TEXTURES["bg"] = load_texture("assets/bg.png")
        TEXTURES["player_idle"] = load_texture("assets/idle.png")
        TEXTURES["player_walk"] = load_texture("assets/walking.png")
        TEXTURES["player_jump"] = load_texture("assets/jumping.png")
        TEXTURES["player_mine"] = load_texture("assets/mine.png")
        TEXTURES["player_throw"] = load_texture("assets/rock_throw.png")
        TEXTURES["enemy"] = load_texture("assets/enemy.png")
        TEXTURES["gems"] = load_texture("assets/gems.png")
        TEXTURES["dynamite"] = load_texture("assets/dynamite.png")
        TEXTURES["dynamite_explosion"] = load_texture("assets/dynamite-explosion.png")
        TEXTURES['tent'] = load_texture("assets/tent.png")
        TEXTURES['egg'] = load_texture("assets/egg.png")
        # Game State Variables
        # Player starts at TILE_SIZE * 2, TILE_SIZE * 2
        self.player = Player(spawn_x, spawn_y, tile_rows, tile_cols, world_width, world_height)
        self.player.points = points 
        self.stones: list[Stone] = []
        self.score = points
        self.game_state = "PLAYING"
        self.tile_rows = tile_rows
        self.tile_cols = tile_cols
        self.world_width = world_width
        self.world_height = world_height
        if level_idx == 0:
            self.ground_level_y = self.world_height - 1600
        else:
            self.ground_level_y = 0

        # --- Camera Initialization ---
        self.camera = Camera2D()
        self.camera.target = Vector2(self.player.x, self.player.y + self.player.height / 2) 
        self.camera.offset = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) 
        self.camera.rotation = 0.0
        self.camera.zoom = 1.0
        print("WORLD SIZE:", world_width, world_height)
        
    def update(self):
        delta_time = GetFrameTime()
        
        # --- Update ---
        if self.game_state == "PLAYING":
            self.player.update(delta_time, self.game_level, self.sand,self.mineable)
            
            # Update Enemies
            for enemy in self.enemies:
                enemy.update(delta_time, self.game_level, self.player, self.enemies,self.sand,self.mineable)

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
                stone.update(delta_time, self.game_level, self.sand,self.mineable, self.dynamites,self.player,self.enemies)
            self.stones = [s for s in self.stones if s.active]

            for dynamite in self.dynamites:
                dynamite.update(delta_time)
            # Remove dynamites that finished explosion animation
            self.dynamites = [d for d in self.dynamites if not d.exploded]

            self.update_camera(self.world_width, self.world_height, SCREEN_WIDTH, SCREEN_HEIGHT)

            for gem in self.collectibles:
                if self.player.check_gem_collection(gem):
                    self.collectibles.remove(gem)
                    self.score += 10

            for egg in self.eggs:
                if self.player.check_gem_collection(egg):
                    self.eggs.remove(egg)
                    if not self.eggs:
                        self.game_state = "WON"
                        self.isGameOver = True

            # Check for enemy collisions
            if self.player.check_enemy_collision(self.enemies):
                # Death/Reset mechanic: Penalty and restart
                self.player.reset()
                self.player.lives -= 1
                self.score -= 50 
                if self.score < 0: self.score = 0
            if check_sand_crush(self.sand,self.player.get_rect()):
                self.player.reset()
                self.player.lives -= 1
                self.score -= 20 
                if self.score < 0: self.score = 0 
            
            if self.player.lives <= 0:
                self.isGameOver = True
                self.game_state = "LOST"   
            for enemy in self.enemies:
                if check_sand_crush(self.sand,enemy.get_rect()):
                    self.enemies.pop(self.enemies.index(enemy))
                    self.score += 20
                    break



    
    def spawn_stone(self, rock_lifetime, is_mining):
        mouse_screen = GetMousePosition()
        mouse_world = GetScreenToWorld2D(mouse_screen, self.camera)
        cx = self.player.x + self.player.width / 2
        cy = self.player.y + self.player.height / 2
        self.stones.append(
            Stone(
                cx,
                cy,
                mouse_world.x,
                mouse_world.y,
                rock_lifetime,
                is_mining,
                self.tile_rows,
                self.tile_cols,
                self.world_width,
                self.world_height,
            )
        )
        
    def draw(self):
        ClearBackground(Color(208,176,128,255))
        # Start the 2D camera mode
        BeginMode2D(self.camera)
        
        # Draw sky/ground background above ground level
        bg_tex = TEXTURES["bg"]
        draw_texture_pro(bg_tex, 
                    Rectangle(0, 0, bg_tex.width, bg_tex.height),
                    Rectangle(0, 0, self.world_width, self.ground_level_y),
                    Vector2(0, 0), 0.0, WHITE)

        if self.ground_level_y > 0:
            tent_tex = TEXTURES["tent"]
            size_x = tent_tex.width * 2
            size_y = tent_tex.height * 2
            draw_texture_pro(tent_tex,
                            Rectangle(0, 0, tent_tex.width, tent_tex.height),
                            Rectangle(25*TILE_SIZE-size_x/2, 20*TILE_SIZE-size_y/2, size_x, size_y),
                            Vector2(0, 0), 0.0, WHITE)
            
        ug_tex = TEXTURES["underground"]
        tint = Color(150, 150, 150, 255)
        for y in range(int(self.ground_level_y), int(self.world_height), ug_tex.height):
            for x in range(0, int(self.world_width), ug_tex.width):
                draw_texture(ug_tex, x, y, tint)

        # 1. Draw the Level
        self.draw_level(self.game_level)

        # 2. Draw Sand
        self.sand.draw()

        # 3. Draw Mineable
        self.mineable.draw()
        
        # 4. Draw Collectibles
        for gem in self.collectibles:
            gem.draw()
        # 5. Draw Enemies
        for enemy in self.enemies:
            enemy.draw()

        # 6. Draw Stones
        for stone in self.stones:
            stone.draw()
            
        for dynamite in self.dynamites:
            dynamite.draw()

        for egg in self.eggs:
            egg.draw()
        # 7. Draw Player
        self.player.draw()
        
        # End the 2D camera mode
        EndMode2D()
        
        # 5. Draw HUD (Drawn on screen, outside of BeginMode2D)
        score_text = f"Score: {self.score}".encode('utf-8')
        DrawText(score_text, SCREEN_WIDTH - MeasureText(score_text, 40) - 10, 10, 40, BLACK)
        
        lives_text = f"Lives: {self.player.lives}".encode('utf-8')
        DrawText(lives_text, 10, 10, 40, BLACK)
        

    
    def draw_level(self, level):
        """Draws the solid tiles of the level map."""
        for row in range(self.tile_rows):
            for col in range(self.tile_cols):
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

