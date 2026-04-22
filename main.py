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

  game = Game()
  game.isGameOver = True
  isTitleScreen = True
  

  while not window_should_close():
    update_music_stream(music)
    if game.isGameOver:
      if isTitleScreen: 
        if IsKeyPressed(KEY_ENTER):
            game.isGameOver = False
            isTitleScreen = False
            
    else:
      game.update()
    #   update_music_stream(hum)
    
    begin_drawing()
    clear_background(BLACK)
    
    
    if not game.isGameOver:
      game.draw()
    else:
        draw_text("Shifting Sands", WINDOW_WIDTH//2 - 200, WINDOW_HEIGHT//2 - 200, FONT_SIZE*3, WHITE)
    end_drawing()

close_audio_device()
close_window()
  
