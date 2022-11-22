from pico2d import *
from math import *
import effects
import game_world

direction  = {'RIGHT' : 1, 'LEFT' : 0}


LightBringerEffects = []

class Arrow:
    image = None
    
    def __init__(arrow, x, y, dx, dy, speed, deg, player):
        if Arrow.image == None:
            Arrow.image = load_image("resources/images/weapon/longDistanceWeapon/ArrowImage.png")
        arrow.x       = x
        arrow.y       = y
        arrow.dx      = dx
        arrow.dy      = dy
        arrow.speed   = speed
        arrow.deg     = deg - 10
        arrow.isOn    = True
        
        if player.direction == direction['LEFT']:
            arrow.direction = direction['LEFT']
        if player.direction == direction['RIGHT']:
            arrow.direction = direction['RIGHT']
        
    def update(arrow):
        arrow.x += arrow.dx * (arrow.speed + 1)
        arrow.y += arrow.dy * (arrow.speed + 1)
        effect = effects.LightBringerEffect(arrow.x, arrow.y)
        LightBringerEffects.append(effect)
        
        if arrow.x < 0 or arrow.x > 1600:
            game_world.remove_object(arrow)
            
            
    
    def draw(arrow):
        if arrow.direction == direction['LEFT']:
            arrow.image.clip_composite_draw(0, 0, 5, 26, radians(arrow.deg), 'n', arrow.x, arrow.y, 50, 260)
        elif arrow.direction == direction['RIGHT']:
            arrow.image.clip_composite_draw(0, 0, 5, 26, radians(arrow.deg), 'h', arrow.x, arrow.y, 50, 260)