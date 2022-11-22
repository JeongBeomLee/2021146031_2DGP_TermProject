from pico2d import *
from math import *
import effects
import game_world

direction  = {'RIGHT' : 1, 'LEFT' : 0}


LightBringerEffects = []

class Bullet:
    image = None
    
    def __init__(bullet, x, y, dx, dy, speed, deg, player):
        if Bullet.image == None:
            Bullet.image = load_image("resources/images/weapon/longDistanceWeapon/ArrowImage.png")
        bullet.x       = x
        bullet.y       = y
        bullet.dx      = dx
        bullet.dy      = dy
        bullet.speed   = speed
        bullet.deg     = deg - 10
        bullet.isOn    = True
        
        if player.direction == direction['LEFT']:
            bullet.direction = direction['LEFT']
        if player.direction == direction['RIGHT']:
            bullet.direction = direction['RIGHT']
        
    def update(bullet):
        bullet.x += bullet.dx * (bullet.speed + 1)
        bullet.y += bullet.dy * (bullet.speed + 1)
        effect = effects.LightBringerEffect(bullet.x, bullet.y)
        LightBringerEffects.append(effect)
        
        if bullet.x < 0 or bullet.x > 1600:
            game_world.remove_object(bullet)
            
            
    def draw(bullet):
        if bullet.direction == direction['LEFT']:
            bullet.image.clip_composite_draw(0, 0, 5, 26, radians(bullet.deg), 'n', bullet.x, bullet.y, 50, 260)
        elif bullet.direction == direction['RIGHT']:
            bullet.image.clip_composite_draw(0, 0, 5, 26, radians(bullet.deg), 'h', bullet.x, bullet.y, 50, 260)