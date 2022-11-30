import game_framework
from pico2d import*
import test_state

open_canvas(1600, 900, sync = True)
hide_cursor()
game_framework.run(test_state)  
close_canvas()