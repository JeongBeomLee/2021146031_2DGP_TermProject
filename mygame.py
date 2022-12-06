import game_framework
from pico2d import*
import title_state
import villiage_state
import move_state
import boss_state
open_canvas(1600, 900, sync = True)
hide_cursor()
game_framework.run(title_state)
close_canvas() 