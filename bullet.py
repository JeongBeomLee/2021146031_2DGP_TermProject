from pico2d import *
from math import *
import effects
import game_world
import test_state

direction  = {'RIGHT' : 1, 'LEFT' : 0}

class Bullet:
    image = None
    
    def __init__(bullet, x, y, dx, dy, deg, player):
        if Bullet.image == None:
            Bullet.image = load_image("resources/images/weapon/longDistanceWeapon/Bullet.png")
        bullet.x       = x
        bullet.y       = y
        bullet.dx      = dx
        bullet.dy      = dy
        bullet.deg     = deg - 90
        bullet.isOn    = True
        
        if player.direction == direction['LEFT']:
            bullet.direction = direction['LEFT']
        if player.direction == direction['RIGHT']:
            bullet.direction = direction['RIGHT']
    #### 바운딩 박스 받기 ####
    def get_bb(bullet):
        return bullet.x - 22.5, bullet.y - 12.5, bullet.x + 22.5, bullet.y + 12.5
    
    #### 객체별 충돌처리 ####
    def handle_collision(bullet, other, group):
        if group == 'Bullet:monster':
            game_world.remove_object(bullet)
            game_world.remove_collision_pairs(bullet, test_state.monster, 'Bullet:monster')
        
    def update(bullet):
        bullet.x += bullet.dx
        bullet.y += bullet.dy
        
        if bullet.x < 0 or bullet.x > 1600 or bullet.y < 0 or bullet.y > 900:
            game_world.remove_object(bullet)
            game_world.remove_collision_pairs(bullet, test_state.monster, 'Bullet:monster')
            
            
    def draw(bullet):
        if bullet.direction == direction['LEFT']:
            bullet.image.clip_composite_draw(0, 0, 9, 5, radians(bullet.deg), 'n', bullet.x, bullet.y, 45, 25)
        elif bullet.direction == direction['RIGHT']:
            bullet.image.clip_composite_draw(0, 0, 9, 5, radians(bullet.deg), 'h', bullet.x, bullet.y, 45, 25)
        draw_rectangle(*bullet.get_bb())
        