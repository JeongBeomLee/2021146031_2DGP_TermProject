from pico2d import *
from Characters_Player import direction
from math import *

class RedPickaxeSwing:
    def __init__(self, weapon, weapon_deg, player):
        global direction
        if player.direction == direction['left']:
            self.x = player.x + 165 * cos(radians(weapon_deg))
            self.y = player.y + 165 * sin(radians(weapon_deg))
        if player.direction == direction['right']:
            self.x = player.x - 165 * cos(radians(weapon_deg))
            self.y = player.y - 165 * sin(radians(weapon_deg))
        self.deg = weapon_deg
        self.image = load_image('resources/images/weapon/MeleeWeapon/RedPickaxeSwing.png')
        self.frame = 0
        self.isOn = True
        if player.direction == direction['left']:
            self.direction = 0
        if player.direction == direction['right']:
            self.direction = 1
        pass
    
    def update(self, weapon):
        
        if self.isOn:
            if self.frame == 13:
                self.frame = 0
                self.isOn = False
                weapon.removeEffect(self)
            self.frame += 1
        pass
    
    def draw(self, player):
        if self.isOn:
            if self.direction == 0:
                self.image.clip_composite_draw(self.frame * 22, 0, 22, 56, radians(self.deg), 'n', self.x, self.y, 110, 280)
            elif self.direction == 1:
                self.image.clip_composite_draw(self.frame * 22, 0, 22, 56, radians(self.deg), 'h', self.x, self.y, 110, 280)
        pass
    