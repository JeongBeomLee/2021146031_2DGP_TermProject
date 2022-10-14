from pico2d import *
import Manager_Events
import Characters_Player_hand

open_canvas(1600, 900)

player = Manager_Events.Characters_Player.Player()
hand = Characters_Player_hand.Hand(player)

while(not Manager_Events.quitMassage):
    ## update
    player.update()
    hand.update(player)
    ## clear canvas
    clear_canvas()
    ## draw
    player.draw()
    hand.draw(player)
    ## double buffering
    update_canvas()
    delay(0.07)
    Manager_Events.events(player) # 이벤트 처리
    
close_canvas()