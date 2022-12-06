from pico2d import *
from math import *
import effects
import game_world
import server

direction  = {'RIGHT' : 1, 'LEFT' : 0}

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
        arrow.power   = player.power + (100 * speed)
        
        if player.direction == direction['LEFT']:
            arrow.direction = direction['LEFT']
        if player.direction == direction['RIGHT']:
            arrow.direction = direction['RIGHT']
    
    #### 바운딩 박스 받기 ####
    def get_bb(arrow):
        return arrow.x - 130, arrow.y - 20, arrow.x + 130, arrow.y + 20
    
    #### 객체별 충돌처리 ####
    def handle_collision(arrow, other, group):
        pass
    
    def update(arrow):
        if arrow.isOn:
            arrow.x += arrow.dx * (arrow.speed + 1)
            arrow.y += arrow.dy * (arrow.speed + 1)
            effect = effects.LightBringerEffect(arrow.x, arrow.y)
            game_world.add_object(effect, 0)
        
        if arrow.x < 0 or arrow.x > 1600 or arrow.y < 0 or arrow.y > 900:
            arrow.isOn = False;
            game_world.remove_object(arrow)
            game_world.remove_collision_pairs(arrow, server.monster, 'Arrow:monster')
            
            #### remove_collision_object가 객체의 충돌영역을 지워주지 못해서 객체를 다른데로 보냄
            arrow.x = 99999
            arrow.y = 99999
            
            
    
    def draw(arrow):
        if arrow.isOn:
            if arrow.direction == direction['LEFT']:
                arrow.image.clip_composite_draw(0, 0, 5, 26, radians(arrow.deg), 'n', arrow.x, arrow.y, 50, 260)
            elif arrow.direction == direction['RIGHT']:
                arrow.image.clip_composite_draw(0, 0, 5, 26, radians(arrow.deg), 'h', arrow.x, arrow.y, 50, 260)
            draw_rectangle(*arrow.get_bb())