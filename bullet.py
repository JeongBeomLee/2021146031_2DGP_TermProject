from pico2d import *
from math import *
import effects
import game_world

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
        
    def update(bullet):
        bullet.x += bullet.dx
        bullet.y += bullet.dy
        
        if bullet.x < 0 or bullet.x > 1600:
            game_world.remove_object(bullet)
            
            
    def draw(bullet):
        if bullet.direction == direction['LEFT']:
            bullet.image.clip_composite_draw(0, 0, 9, 5, radians(bullet.deg), 'n', bullet.x, bullet.y, 45, 25)
        elif bullet.direction == direction['RIGHT']:
            bullet.image.clip_composite_draw(0, 0, 9, 5, radians(bullet.deg), 'h', bullet.x, bullet.y, 45, 25)