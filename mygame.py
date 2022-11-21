import game_framework
from pico2d import*
import stage1_state

open_canvas(1600, 900, sync = True)
game_framework.run(stage1_state)
close_canvas()