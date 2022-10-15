from pico2d import *
import Manager_Events
import Characters_Player_hand
import Weapons_Short

open_canvas(1600, 900)

player = Manager_Events.Characters_Player.Player()
hand = Characters_Player_hand.Hand(player)
weapon = Weapons_Short.shortSword(player)

def update():
    global player, hand
    player.update()
    hand.update(player)
    weapon.update(player)

def draw():
    global player, hand, weapon
    
    if weapon.backrender:
        weapon.draw(player)
        
    player.draw()
    
    if not weapon.backrender:
        weapon.draw(player)
    hand.draw(player)
    

while(not Manager_Events.quitMassage):
    update()
    clear_canvas()
    draw()
    update_canvas()
    delay(0.07)
    Manager_Events.events(player, weapon) # 이벤트 처리
    
close_canvas()