from pico2d import *
import Manager_Events
import Characters_Player_hand
import Weapons_Short
import Monsters_Monster
from Weapons_Short import weaponSort

open_canvas(1600, 900)

player = Manager_Events.Characters_Player.Player()
hand = Characters_Player_hand.Hand(player)
#weapon = Weapons_Short.shortSword(player)
weapon = Weapons_Short.pickaxeRed(player)
monsters = [Monsters_Monster.Ghost(player) for i in range(5)]

def update():   
    global player, hand, ghost
    player.update()
    hand.update(player)
    weapon.update(player)
    #weapon.effect.update()
    for ghost in monsters:
        ghost.update(player)

def draw():
    global player, hand, weapon, weaponSort, ghost
    
    if weapon.backrender:
            weapon.draw(player)
            
    player.draw()
    for ghost in monsters:
        ghost.draw()
    
    
    if not weapon.backrender:
        weapon.draw(player)
    if not weapon.sort == weaponSort['sickle']:
        hand.draw(player)
        
    #weapon.effect.draw(weapon, player) 

while(not Manager_Events.quitMassage):
    update()
    clear_canvas()
    draw()
    update_canvas()
    delay(0.05)
    Manager_Events.events(player, weapon) # 이벤트 처리
    
close_canvas()