import game_framework
from pico2d import*
import test_state
import villiage_state

open_canvas(1600, 900, sync = True)
hide_cursor()
game_framework.run(villiage_state)  
close_canvas()