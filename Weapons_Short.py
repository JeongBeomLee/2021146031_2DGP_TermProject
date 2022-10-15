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
        self.image = load_image('resources/images/weapon/MeleeWeapon/ShortSword.png')
        self.backrender = True
        pass
    
    def update(self, player):
        global direction, deg, mouse_x, mouse_y, backrender
        
        if player.direction == direction['left']:
            deg = atan2(-((player.y + 900) - mouse_y), (player.x - mouse_x)) * 180 / pi
            if self.backrender:
                self.x = player.x - 50
                self.y = player.y + 7
            else:
                self.x = player.x - 10
                self.y = player.y - 50
            
        elif player.direction == direction['right']:
            deg = atan2(-(mouse_y - (player.y + 900)), (mouse_x - player.x)) * 180 / pi
            if self.backrender:
                self.x = player.x + 50
                self.y = player.y + 7
            else:
                self.x = player.x + 10
                self.y = player.y - 50
            
        # if backrender == False:
        #     deg -= 140
            
        #print('playerX : %d, playerY : %d \nmouseX : %d, mouseY : %d\ndeg : %f', (player.x,player.y,mouse_x,mouse_y,deg))
        
        #deg = atan2(-(player.y - mouse_y), (player.x - mouse_x))
        pass
    
    def draw(self, player):
        global deg
        
        if player.direction == direction['left']:
            if self.backrender:
                self.image.clip_composite_draw(0, 0, 19, 7, radians(deg), 'h', self.x, self.y, 95, 35)
            else:
                self.image.clip_composite_draw(0, 0, 19, 7, radians(deg), 'n', self.x, self.y, 95, 35)
                
                
            
        elif player.direction == direction['right']:
            if self.backrender:
                self.image.clip_composite_draw(0, 0, 19, 7, radians(deg), 'n', self.x, self.y, 95, 35)
            else:
                self.image.clip_composite_draw(0, 0, 19, 7, radians(deg), 'h', self.x, self.y, 95, 35)
            
        pass
    
def getMouse(x, y):
    global mouse_x, mouse_y
    
    mouse_x = x
    mouse_y = y