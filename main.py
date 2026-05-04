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
  spawn_points = [(TILE_SIZE * 20, TILE_SIZE * 35),(TILE_SIZE * 40, TILE_SIZE * 1)]
  # spawn_points = [(TILE_SIZE * 2, TILE_SIZE * 2)]
  game = Game(level_idx, spawn_points[level_idx][1], spawn_points[level_idx][0], 0)
  game.isGameOver = True
  has_won = False
  isTitleScreen = True
  final_score = 0
  isLevelTransition = False
  next_level_idx = 0
  transition_points = 0
  transition_timer = 0.0
  transition_duration = 1.5

  
  

  while not window_should_close():
    update_music_stream(music)
    
    
    if isLevelTransition:
      transition_timer += GetFrameTime()
      if IsKeyPressed(KEY_ENTER) or transition_timer >= transition_duration:
        level_idx = next_level_idx
        game = Game(level_idx, spawn_points[level_idx][1], spawn_points[level_idx][0], transition_points)
        game.isGameOver = False
        isLevelTransition = False
        transition_timer = 0.0
    elif game.isGameOver:
      
      if IsKeyPressed(KEY_ENTER):
        if has_won:
            level_idx = 0
            has_won = False
        elif not isTitleScreen:
            level_idx = 0 # reset back to level 0 when lost
        game = Game(level_idx, spawn_points[level_idx][1], spawn_points[level_idx][0], 0)
        game.isGameOver = False
        isTitleScreen = False
            
    else:
      game.update()
      if game.game_state == "WON":
        level_idx += 1
        if level_idx < len(spawn_points):
          isLevelTransition = True
          next_level_idx = level_idx
          transition_points = game.score
          transition_timer = 0.0
        else:
          has_won = True
          final_score = game.score
          game.isGameOver = True
      elif game.game_state == "LOST":
          game.isGameOver = True

          
    #   update_music_stream(hum)
    
    begin_drawing()
    clear_background(BLACK)
    
    
    if isLevelTransition:
      draw_text("Level Complete!", WINDOW_WIDTH//2 - 160, WINDOW_HEIGHT//2 - 200, FONT_SIZE*3, WHITE)
      draw_text("Preparing Next Level...", WINDOW_WIDTH//2 - 220, WINDOW_HEIGHT//2 - 50, FONT_SIZE*2, WHITE)
      draw_text("Press Enter to Continue", WINDOW_WIDTH//2 - 220, WINDOW_HEIGHT//2 + 50, FONT_SIZE*2, WHITE)
    elif not game.isGameOver:
      game.draw()
    else:
      if has_won:
        draw_text("You Won!", WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 - 200, FONT_SIZE*3, WHITE)
        score_text = f"Final Score: {final_score}"
        draw_text(score_text, WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2 - 50, FONT_SIZE*2, WHITE)
        draw_text("Press Enter to Restart Game", WINDOW_WIDTH//2 - 250, WINDOW_HEIGHT//2 + 50, FONT_SIZE*2, WHITE)
      elif isTitleScreen:
        draw_text("Shifting Sands", WINDOW_WIDTH//2 - 200, WINDOW_HEIGHT//2 - 200, FONT_SIZE*3, WHITE)
        draw_text("Press Enter to Start", WINDOW_WIDTH//2 - 180, WINDOW_HEIGHT//2, FONT_SIZE*2, WHITE)
      else:
        draw_text("Game Over", WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2 - 200, FONT_SIZE*3, WHITE)
        draw_text("Press Enter to Restart Game", WINDOW_WIDTH//2 - 220, WINDOW_HEIGHT//2, FONT_SIZE*2, WHITE)
    end_drawing()

close_audio_device()
close_window()
  
