from pico2d import *
from math import *
import effects
import game_world
import server

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
        bullet.power   = player.power + 100
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
        if bullet.isOn:
            if group == 'Bullet:monster':
                bullet.isOn = False
                game_world.remove_object(bullet)
                game_world.remove_collision_pairs(bullet, server.monster, 'Bullet:monster')
                boomEffect = effects.BoomEffect(bullet)
                game_world.add_object(boomEffect, 0)
                
                #### remove_collision_object가 객체의 충돌영역을 지워주지 못해서 객체를 다른데로 보냄
                bullet.x = 99999
                bullet.y = 99999
                
            if group == 'Bullet:ground':
                bullet.isOn = False
                game_world.remove_object(bullet)
                game_world.remove_collision_pairs(bullet, server.ground, 'Bullet:ground')
                boomEffect = effects.BoomEffect(bullet)
                game_world.add_object(boomEffect, 0)
                
                #### remove_collision_object가 객체의 충돌영역을 지워주지 못해서 객체를 다른데로 보냄
                bullet.x = 99999
                bullet.y = 99999
        
    def update(bullet):
        if bullet.isOn:
            bullet.x += bullet.dx
            bullet.y += bullet.dy
        
        if bullet.x < 0 or bullet.x > 1600 or bullet.y < 0 or bullet.y > 900:
            bullet.isOn = False
            game_world.remove_object(bullet)
            game_world.remove_collision_pairs(bullet, server.monster, 'Bullet:monster')
            game_world.remove_collision_pairs(bullet, server.ground, 'Bullet:ground')
            
            #### remove_collision_object가 객체의 충돌영역을 지워주지 못해서 객체를 다른데로 보냄
            bullet.x = 99999
            bullet.y = 99999
            
            
    def draw(bullet):
        if bullet.isOn:
            if bullet.direction == direction['LEFT']:
                bullet.image.clip_composite_draw(0, 0, 9, 5, radians(bullet.deg), 'n', bullet.x, bullet.y, 45, 25)
            elif bullet.direction == direction['RIGHT']:
                bullet.image.clip_composite_draw(0, 0, 9, 5, radians(bullet.deg), 'h', bullet.x, bullet.y, 45, 25)
            draw_rectangle(*bullet.get_bb())
        
        
class Boss_Bullet:
    image = None
    
    def __init__(bullet, x, y, dx, dy):
        if Boss_Bullet.image == None:
            Boss_Bullet.image = load_image("resources/images/boss/Belial/bullet.png")
        bullet.x       = x
        bullet.y       = y
        bullet.dx      = dx
        bullet.dy      = dy
        bullet.power   = 10
        bullet.frame   = 0
        bullet.isOn    = True
            
    #### 바운딩 박스 받기 ####
    def get_bb(bullet):
        return bullet.x - 32.5, bullet.y - 32.5, bullet.x + 32.5, bullet.y + 32.5
    
    #### 객체별 충돌처리 ####
    def handle_collision(bullet, other, group):
        if bullet.isOn:
            if group == 'player:ball':
                bullet.isOn = False
                game_world.remove_object(bullet)
                game_world.remove_collision_pairs(server.player, bullet, 'player:ball')
                
                #### remove_collision_object가 객체의 충돌영역을 지워주지 못해서 객체를 다른데로 보냄
                bullet.x = 99999
                bullet.y = 99999
        
    def update(bullet):
        bullet.frame = (bullet.frame + 1) % 2
        if bullet.isOn:
            bullet.x += bullet.dx
            bullet.y += bullet.dy
        
        if bullet.x < 0 or bullet.x > 1600 or bullet.y < 0 or bullet.y > 900:
            bullet.isOn = False
            game_world.remove_object(bullet)
            
            #### remove_collision_object가 객체의 충돌영역을 지워주지 못해서 객체를 다른데로 보냄
            bullet.x = 99999
            bullet.y = 99999
            
            
    def draw(bullet):
        if bullet.isOn:
            bullet.image.clip_composite_draw(int(bullet.frame) * 13, 0, 13, 13, 0, 'n', bullet.x, bullet.y, 65, 65)
            draw_rectangle(*bullet.get_bb())
            