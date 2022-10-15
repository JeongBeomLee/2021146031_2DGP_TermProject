from turtle import window_height
from pico2d import *
from math import *
from Characters_Player import direction

deg = 0
mouse_x, mouse_y = 0, 0

class shortSword:
    def __init__(self, player):
        self.x = player.x
        self.y = player.y
        #self.image = load_image('resources/images/weapon/MeleeWeapon/testsword.png')
        self.image = load_image('resources/images/weapon/MeleeWeapon/ShortSword.png')
        self.backrender = True
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
    
def getMouse(x, y):
    global mouse_x, mouse_y
    
    mouse_x = x
    mouse_y = y