from pico2d import *
from math import *
import game_framework, game_world

import effects
import arrow

deg = 0
mouse_x, mouse_y = 0, 0

# 활 프레임
LB_TIME_PER_ACTION    = 2.0
LB_ACTION_PER_TIME    = 1.0 / LB_TIME_PER_ACTION
LB_FRAMES_PER_ACTION  = 6

# 캐릭터 상태, 방향
state      = {'IDLE'  : 0,  'RUN' : 1, 'JUMP' : 2, 'DASH' : 3}
direction  = {'RIGHT' : 1, 'LEFT' : 0}

shortSwordEffects = []
class shortSword:
    image = None
    
    def __init__(self):
        if shortSword.image == None:
            shortSword.image = load_image('resources/images/weapon/MeleeWeapon/ShortSword.png')
        self.x = 0
        self.y = 0
        self.backrender = True
        self.isAttack = False
    
    def update(self, player):
        global deg, mouse_x, mouse_y
        
        deg = atan2(((900 - mouse_y) - player.y), (mouse_x - player.x)) * 180 / pi + 100
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
        
        if len(shortSwordEffects) != 0:
            for effect in shortSwordEffects:
                effect.update(self)
            
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
                
        if len(shortSwordEffects) != 0:
            for effect in shortSwordEffects:
                effect.draw()
                
    def appendEffect(self, player):
        global deg, shortSwordEffects
        shortSwordEffects.append(effects.shortSwordSwing(deg, player))
        
    def removeEffect(self, effect):
        global shortSwordEffects
        shortSwordEffects.remove(effect)

pickaxeRedEffects = []
class pickaxeRed:
    image = None
    
    def __init__(self):
        if pickaxeRed.image == None:
            pickaxeRed.image = load_image('resources/images/weapon/MeleeWeapon/PickaxeRed.png')
        
        self.x = 0
        self.y = 0
        self.backrender = False
        self.isAttack = False
        self.attackCount = 0
        
    
    def update(self, player):
        global deg, mouse_x, mouse_y
        global pickaxeRedEffects
        
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
                    deg = atan2(((900 - mouse_y) - player.y), (mouse_x - player.x)) * 180 / pi
            elif player.direction == direction['RIGHT']:
                    deg = atan2(((900 - mouse_y) - player.y), (mouse_x - player.x)) * 180 / pi + 180
        
        if player.direction == direction['LEFT']:
            self.x = player.x - 25
            self.y = player.y - 20
                
        elif player.direction == direction['RIGHT']:
            self.x = player.x + 25
            self.y = player.y - 20
        
        # 이펙트 업데이트
        if len(pickaxeRedEffects) != 0:
            for effect in pickaxeRedEffects:
                effect.update(self)
    
    def draw(self, player):
        global deg, pickaxeRedEffects
        
        if player.direction == direction['LEFT']:
            self.image.clip_composite_draw(0, 0, 70, 66, radians(deg), 'h', self.x, self.y, 350, 330)
                
        elif player.direction == direction['RIGHT']:
            self.image.clip_composite_draw(0, 0, 70, 66, radians(deg), 'n', self.x, self.y, 350, 330)
            
        # 이펙트 그리기
        if len(pickaxeRedEffects) != 0:
            for effect in pickaxeRedEffects:
                effect.draw()
        
    def appendEffect(self, player):
        global deg, pickaxeRedEffects
        pickaxeRedEffects.append(effects.RedPickaxeSwing(deg, player))
        
    def removeEffect(self, effect):
        global pickaxeRedEffects
        pickaxeRedEffects.remove(effect)

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
        global deg, mouse_x, mouse_y
        
        deg = atan2(((900 - mouse_y) - player.y), (mouse_x - player.x)) * 180 / pi + 100
        if player.direction == direction['LEFT']:
            self.x = player.x - 15
            self.y = player.y - 10
            
        elif player.direction == direction['RIGHT']:
            self.x = player.x + 15
            self.y = player.y - 10
        
        if self.isAttack:
            if self.frame < 3.5:
                self.frame = (self.frame + LB_FRAMES_PER_ACTION * LB_ACTION_PER_TIME * game_framework.frame_time) % 6
        
        for effect in arrow.LightBringerEffects:
            if effect.opac <= 0:
                arrow.LightBringerEffects.remove(effect)    
            effect.update()
            
    def draw(self, player):
        global deg
        
        if player.direction == direction['LEFT']:
            self.image.clip_composite_draw(int(self.frame) * 30, 0, 30, 25, radians(deg + 100), 'h', self.x, self.y, 150, 125)
                
        elif player.direction == direction['RIGHT']:
            self.image.clip_composite_draw(int(self.frame) * 30, 0, 30, 25, radians(deg - 100), 'n', self.x, self.y, 150, 125)
            
        for effect in arrow.LightBringerEffects:
            effect.draw()
                
    def shootArrow(self, dx, dy, player):
        global deg
        Arrow = arrow.Arrow(self.x, self.y, dx, dy, int(self.frame), deg, player)
        game_world.add_object(Arrow, 1)

pistolEffects = []
class pistol:
    image = None
    
    def __init__(self):
        if pistol.image == None:
            pistol.image = load_image('resources/images/weapon/longDistanceWeapon/Pistol.png')
        self.x = 0
        self.y = 0
        self.backrender = False
        self.isAttack = False
        self.frame = 0
    
    def update(self, player):
        global deg, mouse_x, mouse_y
        
        deg = atan2(((900 - mouse_y) - player.y), (mouse_x - player.x)) * 180 / pi + 100
        if player.direction == direction['LEFT']:
            self.x = player.x - 40
            self.y = player.y - 10
            
        elif player.direction == direction['RIGHT']:
            self.x = player.x + 40
            self.y = player.y - 10
        
        if self.isAttack:
            pass
        
        if len(pistolEffects) != 0:
            for effect in pistolEffects:
                effect.update(self)
            
    def draw(self, player):
        global deg
        
        if player.direction == direction['LEFT']:
            self.image.clip_composite_draw(0, 0, 11, 7, radians(deg + 100), 'h', self.x, self.y, 55, 35)
                
        elif player.direction == direction['RIGHT']:
            self.image.clip_composite_draw(0, 0, 11, 7, radians(deg - 100), 'n', self.x, self.y, 55, 35)
            
        if len(pistolEffects) != 0:
            for effect in pistolEffects:
                effect.draw()
            
    def appendEffect(self, player):
        global deg, pistolEffects
        pistolEffects.append(effects.shootEffect(self, deg, player))
        
    def removeEffect(self, effect):
        global pistolEffects
        pistolEffects.remove(effect)
                
    # def shootArrow(self, dx, dy, player):
    #     global deg
    #     Arrow = arrow.Arrow(self.x, self.y, dx, dy, int(self.frame), deg, player)
    #     game_world.add_object(Arrow, 1)



def getMouse(x, y):
    global mouse_x, mouse_y
    
    mouse_x = x
    mouse_y = y