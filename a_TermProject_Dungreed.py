from pico2d import *
import Manager_Events

open_canvas(1600, 900)

player = Manager_Events.Characters_Player.Player()

while(not Manager_Events.quitMassage):
    player.update()
    clear_canvas()
    player.draw()
    update_canvas()
    delay(0.07)
    Manager_Events.events(player) # 이벤트 처리
    
close_canvas()