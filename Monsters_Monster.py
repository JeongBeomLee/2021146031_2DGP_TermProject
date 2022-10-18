from pico2d import *
import math
import random

ghost_state = {'attack' : 0}
ghost_direction = {'left' : 0, 'right' : 1}
class Ghost:
    def __init__(self, player):
        global ghost_state
        self.x, self.y = random.randint(0, 1600), random.randint(0, 900)
        if self.x < player.x:
            self.direction = ghost_direction['right']
        else:
            self.direction = ghost_direction['left']
        self.dx, self.dy = ((player.x-self.x)/math.sqrt((player.x-self.x)** 2+(player.y-self.y) ** 2) * 10,
                          (player.y-self.y)/math.sqrt((player.x-self.x)** 2+(player.y-self.y) ** 2) * 10)
        self.image = load_image('resources/images/Enemy/Ghost/attack.png')
        self.state = ghost_state['attack']
        self.attackFrame = 0
        self.shotFrame = 0
        self.isAttack = False
        self.isAttacked = False
    
    def update(self, player):
        self.dx, self.dy = ((player.x-self.x)/math.sqrt((player.x-self.x)** 2+(player.y-self.y) ** 2) * 10,
                          (player.y-self.y)/math.sqrt((player.x-self.x)** 2+(player.y-self.y) ** 2) * 10)
        self.x += self.dx
        self.y += self.dy
        if self.x < player.x:
            self.direction = ghost_direction['right']
        else:
            self.direction = ghost_direction['left']
        self.attackFrame = (self.attackFrame + 1) % 3
        pass
    
    def draw(self):
        if self.state == ghost_state['attack']:
            if self.direction == ghost_direction['left']:
                self.image.clip_composite_draw(self.attackFrame * 20, 0, 20, 20, 0, 'h', self.x, self.y, 100, 100)
            if self.direction == ghost_direction['right']:
                self.image.clip_composite_draw(self.attackFrame * 20, 0, 20, 20, 0, 'n', self.x, self.y, 100, 100)
            
            #draw_rectangle(self.x - 50, self.y - 50, self.x + 50, self.y + 50)
        pass