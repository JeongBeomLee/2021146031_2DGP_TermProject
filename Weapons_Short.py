from pico2d import *
from math import *
from Characters_Player import direction
import Effects_ShortWeapon

deg = 0
mouse_x, mouse_y = 0, 0
weaponSort = {'sword' : 0, 'sickle' : 1}

class shortSword:
    def __init__(self, player):
        self.x = player.x
        self.y = player.y
        self.image = load_image('resources/images/weapon/MeleeWeapon/ShortSword.png')
        self.backrender = True
        self.sort = weaponSort['sword']
        self.isAttack = False
        pass
    
    def update(self, player):
        global direction, deg, mouse_x, mouse_y
        
        deg = atan2(((900 - mouse_y) - player.y), (mouse_x - player.x)) * 180 / pi + 100
        if player.direction == direction['left']:
            if self.backrender:
                self.x = player.x - 15
                self.y = player.y - 10
            else:
                self.x = player.x - 10
                self.y = player.y - 40
            
        elif player.direction == direction['right']:
            if self.backrender:
                self.x = player.x + 15
                self.y = player.y - 10
            else:
                self.x = player.x + 10
                self.y = player.y - 40
            
        #print(deg)
        pass
    
    def draw(self, player):
        global deg
        
        if player.direction == direction['left']:
            if self.backrender:
                self.image.clip_composite_draw(0, 0, 38, 14, radians(deg), 'h', self.x, self.y, 155, 70)
            else:
                self.image.clip_composite_draw(0, 0, 38, 14, radians(deg), 'n', self.x, self.y, 155, 70)
                
        elif player.direction == direction['right']:
            if self.backrender:
                self.image.clip_composite_draw(0, 0, 38, 14, radians(deg), 'n', self.x, self.y, 155, 70)
            else:
                self.image.clip_composite_draw(0, 0, 38, 14, radians(deg), 'h', self.x, self.y, 155, 70)
        #print(deg)
        pass


pickaxeRedEffects = []
class pickaxeRed:
    def __init__(self, player):
        self.x = player.x
        self.y = player.y
        self.image = load_image('resources/images/weapon/MeleeWeapon/PickaxeRed.png')
        self.backrender = False
        self.sort = weaponSort['sickle']
        self.isAttack = False
        self.attackCount = 0
        
    
    def update(self, player):
        global direction, deg, mouse_x, mouse_y
        global pickaxeRedEffects
        
        if self.isAttack:
            if self.attackCount < 2:
                if player.direction == direction['left']:
                    deg += 90
                    self.attackCount += 1
                elif player.direction == direction['right']:
                    deg -= 90
                    self.attackCount += 1
            elif self.attackCount >= 2 and self.attackCount < 4:
                if player.direction == direction['left']:
                    deg -= 90
                    self.attackCount += 1
                elif player.direction == direction['right']:
                    deg += 90
                    self.attackCount += 1
            elif self.attackCount == 4:
                self.attackCount = 0
                self.isAttack = False
        else:
            if player.direction == direction['left']:
                    deg = atan2(((900 - mouse_y) - player.y), (mouse_x - player.x)) * 180 / pi
            elif player.direction == direction['right']:
                    deg = atan2(((900 - mouse_y) - player.y), (mouse_x - player.x)) * 180 / pi + 180
        
        if player.direction == direction['left']:
            self.x = player.x - 25
            self.y = player.y - 20
                
        elif player.direction == direction['right']:
            self.x = player.x + 25
            self.y = player.y - 20
        
        # 이펙트 업데이트
        if not len(pickaxeRedEffects) == 0:
            for effect in pickaxeRedEffects:
                effect.update(self)
    
    def draw(self, player):
        global deg, pickaxeRedEffects
        
        if player.direction == direction['left']:
            self.image.clip_composite_draw(0, 0, 70, 66, radians(deg), 'h', self.x, self.y, 350, 330)
                
        elif player.direction == direction['right']:
            self.image.clip_composite_draw(0, 0, 70, 66, radians(deg), 'n', self.x, self.y, 350, 330)
            
        # 이펙트 드로우
        if not len(pickaxeRedEffects) == 0:
            for effect in pickaxeRedEffects:
                effect.draw(player)
        
    def appendEffect(self, player):
        global deg, pickaxeRedEffects
        pickaxeRedEffects.append(Effects_ShortWeapon.RedPickaxeSwing(self, deg, player))
        
    def removeEffect(self, effect):
        global pickaxeRedEffects
        pickaxeRedEffects.remove(effect)
        
        
            
    
def getMouse(x, y):
    global mouse_x, mouse_y
    
    mouse_x = x
    mouse_y = y