from pico2d import *
from math import *
import game_framework, game_world

import effects
import arrow
import bullet
import server
import server

deg = 0
mouseX, mouseY = 0, 0

# 활 프레임
LB_TIME_PER_ACTION    = 2.0
LB_ACTION_PER_TIME    = 1.0 / LB_TIME_PER_ACTION
LB_FRAMES_PER_ACTION  = 6

# 캐릭터 상태, 방향
state      = {'IDLE'  : 0,  'RUN' : 1, 'JUMP' : 2, 'DASH' : 3, 'DIE' : 4}
direction  = {'RIGHT' : 1, 'LEFT' : 0}

class ShortSword:
    image = None
    
    def __init__(self):
        if ShortSword.image == None:
            ShortSword.image = load_image('resources/images/weapon/MeleeWeapon/ShortSword.png')
        self.x = 0
        self.y = 0
        self.backrender = True
        self.isAttack = False
        self.attackCount = 0
    
    def update(self, player):
        global deg, mouseX, mouseY
        
        deg = atan2(((900 - mouseY) - player.y), (mouseX - player.x)) * 180 / pi + 100
        if player.direction == direction['LEFT']:
            if self.backrender:
                self.x = player.x - 15
                self.y = player.y - 10
            else:
                self.x = player.x
                self.y = player.y - 10
            
        elif player.direction == direction['RIGHT']:
            if self.backrender:
                self.x = player.x + 15
                self.y = player.y - 10
            else:
                self.x = player.x
                self.y = player.y - 10
            
        if self.isAttack:
            self.attackCount += 1
            if self.attackCount == 8:
                self.attackCount = 0
                self.isAttack = False
                
    def draw(self, player):
        global deg
        
        if player.direction == direction['LEFT']:
            if self.backrender:
                self.image.clip_composite_draw(0, 0, 38, 14, radians(deg), 'h', self.x, self.y, 155, 70)
            else:
                self.image.clip_composite_draw(0, 0, 38, 14, radians(deg + 30), 'n', self.x, self.y, 155, 70)
                
        elif player.direction == direction['RIGHT']:
            if self.backrender:
                self.image.clip_composite_draw(0, 0, 38, 14, radians(deg), 'n', self.x, self.y, 155, 70)
            else:
                self.image.clip_composite_draw(0, 0, 38, 14, radians(deg - 30), 'h', self.x, self.y, 155, 70)
                
    def append_Effect(self, player):
        global deg
        shortSwordEffect = effects.ShortSwordSwing(deg, player)
        game_world.add_object(shortSwordEffect, 2)
        # for monster in monsters:
        # game_world.add_collision_pairs(shortSwordEffect, test_state.monster, 'shortSwordEffect:monster')
        game_world.add_collision_pairs(shortSwordEffect, server.monster, 'shortSwordEffect:monster')

class PickaxeRed:
    image = None
    
    def __init__(self):
        if PickaxeRed.image == None:
            PickaxeRed.image = load_image('resources/images/weapon/MeleeWeapon/PickaxeRed.png')
        
        self.x = 0
        self.y = 0
        self.backrender = False
        self.isAttack = False
        self.attackCount = 0
    
    def update(self, player):
        global deg, mouseX, mouseY
        
        if self.isAttack:
            if self.attackCount < 4:
                if player.direction == direction['LEFT']:
                    deg += 45
                    self.attackCount += 1
                elif player.direction == direction['RIGHT']:
                    deg -= 45
                    self.attackCount += 1
            elif self.attackCount >= 4 and self.attackCount < 8:
                if player.direction == direction['LEFT']:
                    deg -= 45
                    self.attackCount += 1
                elif player.direction == direction['RIGHT']:
                    deg += 45
                    self.attackCount += 1
            elif self.attackCount == 8:
                self.attackCount = 0
                self.isAttack = False
        else:
            if player.direction == direction['LEFT']:
                    deg = atan2(((900 - mouseY) - player.y), (mouseX - player.x)) * 180 / pi
            elif player.direction == direction['RIGHT']:
                    deg = atan2(((900 - mouseY) - player.y), (mouseX - player.x)) * 180 / pi + 180
        
        if player.direction == direction['LEFT']:
            self.x = player.x - 25
            self.y = player.y - 20
                
        elif player.direction == direction['RIGHT']:
            self.x = player.x + 25
            self.y = player.y - 20
    
    def draw(self, player):
        global deg
        
        if player.direction == direction['LEFT']:
            self.image.clip_composite_draw(0, 0, 70, 66, radians(deg), 'h', self.x, self.y, 350, 330)
                
        elif player.direction == direction['RIGHT']:
            self.image.clip_composite_draw(0, 0, 70, 66, radians(deg), 'n', self.x, self.y, 350, 330)
        
    def append_Effect(self, player):
        global deg
        pickaxeRedEffect = effects.RedPickaxeSwing(deg, player)
        game_world.add_object(pickaxeRedEffect, 2)
        game_world.add_collision_pairs(pickaxeRedEffect, server.monster, 'pickaxeRedEffect:monster')
        

class LightBringer:
    image = None
    
    def __init__(self):
        if LightBringer.image == None:
            LightBringer.image = load_image('resources/images/weapon/longDistanceWeapon/LightBringer.png')
        self.x = 0
        self.y = 0
        self.backrender = False
        self.isAttack = False
        self.frame = 0
    
    def update(self, player):
        global deg, mouseX, mouseY
        
        deg = atan2(((900 - mouseY) - player.y), (mouseX - player.x)) * 180 / pi + 100
        if player.direction == direction['LEFT']:
            self.x = player.x - 15
            self.y = player.y - 10
            
        elif player.direction == direction['RIGHT']:
            self.x = player.x + 15
            self.y = player.y - 10
        
        if self.isAttack:
            if self.frame < 3.5:
                self.frame = (self.frame + LB_FRAMES_PER_ACTION * LB_ACTION_PER_TIME * game_framework.frame_time) % 6
            
    def draw(self, player):
        global deg
        
        if player.direction == direction['LEFT']:
            self.image.clip_composite_draw(int(self.frame) * 30, 0, 30, 25, radians(deg + 100), 'h', self.x, self.y, 150, 125)
                
        elif player.direction == direction['RIGHT']:
            self.image.clip_composite_draw(int(self.frame) * 30, 0, 30, 25, radians(deg - 100), 'n', self.x, self.y, 150, 125)
                
    def shoot_Arrow(self, dx, dy, player):
        global deg
        Arrow = arrow.Arrow(self.x, self.y, dx, dy, int(self.frame), deg, player)
        game_world.add_object(Arrow, 4)
        game_world.add_collision_pairs(Arrow, server.monster, 'Arrow:monster')

class Pistol:
    image       = None
    bulletCount = 10
    isReload    = False
    
    def __init__(self):
        if Pistol.image == None:
            Pistol.image = load_image('resources/images/weapon/longDistanceWeapon/Pistol.png')
        self.x = 0
        self.y = 0
        self.backrender  = False
        self.isAttack    = False
        self.recoilDeg   = 0
        # self.isReload    = False
        # self.bulletCount = 10

    def update(self, player):
        global deg, mouseX, mouseY
        
        deg = atan2(((900 - mouseY) - player.y), (mouseX - player.x)) * 180 / pi + 100 
        if player.direction == direction['LEFT']:
            self.x = player.x - 40
            self.y = player.y - 10
            
        elif player.direction == direction['RIGHT']:
            self.x = player.x + 40
            self.y = player.y - 10
        
        if self.isAttack:
            self.recoilDeg = 30
        
        if self.recoilDeg != 0:
            self.recoilDeg -= 5
        
        if self.bulletCount == 0:
            if Pistol.isReload == False:
                Pistol.isReload = True
                reloadEffect = effects.ReloadEffect(player)
                game_world.add_object(reloadEffect, 0)
            
    def draw(self, player):
        global deg
        
        if player.direction == direction['LEFT']:
            self.image.clip_composite_draw(0, 0, 11, 7, radians(deg + 80 - self.recoilDeg), 'h', self.x, self.y, 55, 35)
                
        elif player.direction == direction['RIGHT']:
            self.image.clip_composite_draw(0, 0, 11, 7, radians(deg - 100 + self.recoilDeg), 'n', self.x, self.y, 55, 35)
            
            
    def append_Effect(self, player):
        global deg
        pistolEffect = effects.ShootEffect(self, deg, player)
        game_world.add_object(pistolEffect, 0)
        
                
    def shoot_Bullet(self, dx, dy, player):
        global deg
        Bullet = bullet.Bullet(self.x, self.y, dx, dy, deg, player)
        game_world.add_object(Bullet, 5)
        game_world.add_collision_pairs(Bullet, server.monster, 'Bullet:monster')
        game_world.add_collision_pairs(Bullet, server.ground,  'Bullet:ground')
        Pistol.bulletCount -= 1
            

def pistol_Reload():
    Pistol.bulletCount = 10
    Pistol.isReload = False
    
def get_Mouse(x, y):
    global mouseX, mouseY
    
    mouseX = x
    mouseY = y