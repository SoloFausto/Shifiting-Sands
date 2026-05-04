from raylib import *
from settings import * 
from sand_game import Game


if __name__ == '__main__':  

  init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Shifting Sands")
  init_audio_device()
  set_target_fps(120)
  
  music = load_music_stream("assets/music.mp3")
  play_music_stream(music)
  set_music_volume(music, 0.15)
  level_idx = 0
  spawn_points = [(TILE_SIZE * 19, TILE_SIZE * 35),(TILE_SIZE * 40, TILE_SIZE * 1)]
  # spawn_points = [(TILE_SIZE * 2, TILE_SIZE * 2)]
  game = Game(level_idx, spawn_points[level_idx][1], spawn_points[level_idx][0], 0)
  game.isGameOver = True
  has_won = False
  isTitleScreen = True
  isIntroScreen = False
  intro_step = 0
  has_seen_intro = False
  final_score = 0
  isLevelTransition = False
  next_level_idx = 0
  transition_points = 0
  transition_timer = 0.0
  transition_duration = 1.5
  isPaused = False
  level_start_points = 0

  
  

  while not window_should_close():
    update_music_stream(music)
    
    
    if isLevelTransition:
      transition_timer += GetFrameTime()
      if IsKeyPressed(KEY_ENTER) or transition_timer >= transition_duration:
        level_idx = next_level_idx
        game = Game(level_idx, spawn_points[level_idx][1], spawn_points[level_idx][0], transition_points)
        game.isGameOver = False
        level_start_points = transition_points
        isLevelTransition = False
        isPaused = False
        transition_timer = 0.0
    elif game.isGameOver:
      if isIntroScreen:
        if IsKeyPressed(KEY_ENTER):
          if intro_step == 0:
            intro_step = 1
          else:
            game = Game(level_idx, spawn_points[level_idx][1], spawn_points[level_idx][0], 0)
            game.isGameOver = False
            level_start_points = 0
            isPaused = False
            isIntroScreen = False
            isTitleScreen = False
            has_seen_intro = True
      elif IsKeyPressed(KEY_ENTER):
        if isTitleScreen:
          if not has_seen_intro:
            isIntroScreen = True
            intro_step = 0
            isTitleScreen = False
          else:
            game = Game(level_idx, spawn_points[level_idx][1], spawn_points[level_idx][0], 0)
            game.isGameOver = False
            level_start_points = 0
            isPaused = False
            isTitleScreen = False
        else:
          if has_won:
              level_idx = 0
              has_won = False
          elif not isTitleScreen:
              level_idx = 0 # reset back to level 0 when lost
          game = Game(level_idx, spawn_points[level_idx][1], spawn_points[level_idx][0], 0)
          game.isGameOver = False
          level_start_points = 0
          isPaused = False
            
    else:
      if IsKeyPressed(KEY_P):
        isPaused = not isPaused
      if isPaused:
        if IsKeyPressed(KEY_R):
          game = Game(level_idx, spawn_points[level_idx][1], spawn_points[level_idx][0], level_start_points)
          game.isGameOver = False
          isPaused = False
      else:
        game.update()
        if game.game_state == "WON":
          level_idx += 1
          if level_idx < len(spawn_points):
            isLevelTransition = True
            next_level_idx = level_idx
            transition_points = game.score
            transition_timer = 0.0
            isPaused = False
          else:
            has_won = True
            final_score = game.score
            game.isGameOver = True
            isPaused = False
        elif game.game_state == "LOST":
            game.isGameOver = True
            isPaused = False

          
    #   update_music_stream(hum)
    
    begin_drawing()
    clear_background(BLACK)
    
    
    if isLevelTransition:
      draw_texture_ex(TEXTURES['game_over'], Vector2(0, 0), 0.0,1, WHITE)
      text_0 = "Level Complete!"
      text_1 = "Preparing Next Level..."
      text_2 = "Press Enter to Continue"
      line0_x = WINDOW_WIDTH//2 - measure_text(text_0, FONT_SIZE*3)//2
      line1_x = WINDOW_WIDTH//2 - measure_text(text_1, FONT_SIZE*2)//2
      line2_x = WINDOW_WIDTH//2 - measure_text(text_2, FONT_SIZE*2)//2

      draw_text("Level Complete!", line0_x, WINDOW_HEIGHT//2 - 200, FONT_SIZE*3, WHITE)
      draw_text("Preparing Next Level...", line1_x, WINDOW_HEIGHT//2 - 50, FONT_SIZE*2, WHITE)
      draw_text("Press Enter to Continue", line2_x, WINDOW_HEIGHT//2 + 50, FONT_SIZE*2, WHITE)

    elif isIntroScreen:
      draw_texture_ex(TEXTURES['dialogue'], Vector2(0, 0), 0.0,1, WHITE)

      text_0 = "Press Enter to continue."
      line0_x = WINDOW_WIDTH//2 - measure_text(text_0, FONT_SIZE*2)//2

      if intro_step == 0:
        text_1 = "Heya boss, would you like to help me recover these ancient gems?"
        text_2 = "You'll have to explore these unstable caves that are filled with danger."
        text_3 = "Look for the dinosaur egg at each level, and use the sand to crush your enemies!"
        line1_x = WINDOW_WIDTH//2- measure_text(text_1, FONT_SIZE-10)//2
        line2_x = WINDOW_WIDTH//2 - measure_text(text_2, FONT_SIZE-10)//2
        line3_x = WINDOW_WIDTH//2 - measure_text(text_3, FONT_SIZE-10)//2
        draw_text(text_1, line1_x, WINDOW_HEIGHT//2 - 200, FONT_SIZE-10, WHITE)
        draw_text(text_2, line2_x, WINDOW_HEIGHT//2 - 150, FONT_SIZE-10, WHITE)
        draw_text(text_3, line3_x, WINDOW_HEIGHT//2 - 100, FONT_SIZE-10, WHITE)
      elif intro_step == 1:
        text_1 = "Controls:"
        text_2 = "Use WASD to move, space to jump, and left click to throw a stone."
        text_3 = "Use E to mine sand and stone, and P to pause."
        line1_x = WINDOW_WIDTH//2- measure_text(text_1, FONT_SIZE//1)//2
        line2_x = WINDOW_WIDTH//2 - measure_text(text_2, FONT_SIZE//1)//2
        line3_x = WINDOW_WIDTH//2 - measure_text(text_3, FONT_SIZE//1)//2
        draw_text(text_1, line1_x, WINDOW_HEIGHT//2 - 200, FONT_SIZE, WHITE)
        draw_text(text_2, line2_x, WINDOW_HEIGHT//2 - 150, FONT_SIZE, WHITE)
        draw_text(text_3, line3_x, WINDOW_HEIGHT//2 - 100, FONT_SIZE, WHITE)
        
      draw_text(text_0, line0_x, WINDOW_HEIGHT//2 + 50, FONT_SIZE*2, WHITE)
      
    elif not game.isGameOver:
      game.draw()
      if isPaused:
        DrawRectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, Color(0, 0, 0, 160))
        line1_x = WINDOW_WIDTH//2- measure_text("Paused", FONT_SIZE*3)//2
        line2_x = WINDOW_WIDTH//2 - measure_text("Press P to Resume", FONT_SIZE*2)//2
        line3_x = WINDOW_WIDTH//2 - measure_text("Press R to Reset Level", FONT_SIZE*2)//2
        draw_text("Paused", line1_x, WINDOW_HEIGHT//2 - 200, FONT_SIZE*3, WHITE)
        draw_text("Press P to Resume", line2_x, WINDOW_HEIGHT//2 - 50, FONT_SIZE*2, WHITE)
        draw_text("Press R to Reset Level", line3_x, WINDOW_HEIGHT//2 + 50, FONT_SIZE*2, WHITE)
        
    else:
      if has_won:
        draw_texture_ex(TEXTURES['game_over'], Vector2(0, 0), 0.0,1, WHITE)
        line1_text = "Congratulations, you found all the eggs!"
        score_text = f"Final Score: {final_score}"
        line3_text = "Press Enter to Restart Game"
        line1_x = WINDOW_WIDTH//2 - measure_text(line1_text, FONT_SIZE*3)//2
        line2_x = WINDOW_WIDTH//2 - measure_text(score_text, FONT_SIZE*2)//2
        line3_x = WINDOW_WIDTH//2 - measure_text(line3_text, FONT_SIZE*2)//2

        draw_text(line1_text, line1_x, WINDOW_HEIGHT//2 - 200, FONT_SIZE*3, WHITE)
        draw_text(score_text, line2_x, WINDOW_HEIGHT//2 - 50, FONT_SIZE*2, WHITE)
        draw_text(line3_text, line3_x, WINDOW_HEIGHT//2 + 50, FONT_SIZE*2, WHITE)
      elif isTitleScreen:
        draw_texture_ex(TEXTURES['title_screen'], Vector2(0, 0), 0.0,1, WHITE)
        start_text = "Press Enter to Start"
        line1_x = WINDOW_WIDTH//2 - measure_text(start_text, FONT_SIZE*2)//2
        draw_text(start_text, line1_x, WINDOW_HEIGHT//2 -150, FONT_SIZE*2, BLACK)
      else:
        draw_texture_ex(TEXTURES['game_over'], Vector2(0, 0), 0.0,1, WHITE)
        line1_text = "Game Over"
        line2_text = "Press Enter to Restart Game"
        line1_x = WINDOW_WIDTH//2 - measure_text(line1_text, FONT_SIZE*3)//2
        line2_x = WINDOW_WIDTH//2 - measure_text(line2_text, FONT_SIZE*2)//2
        draw_text(line1_text, line1_x, WINDOW_HEIGHT//2 - 200, FONT_SIZE*3, WHITE)
        draw_text(line2_text, line2_x, WINDOW_HEIGHT//2, FONT_SIZE*2, WHITE)
    end_drawing()

close_audio_device()
close_window()
  
