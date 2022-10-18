from pico2d import *
from Characters_Player import direction, state

class Hand:
    def __init__(self, player):
        self.x = player.x - 35
        self.y = player.y - 25
        self.image = load_image('resources/images/Characters/Player/Costume/common/player_hand.png')
        
    def update(self, player):
        global direction
        global state
        if player.state == state['idle']:
            if player.direction == direction['left']:
                self.x = player.x + 35
            elif player.direction == direction['right']:
                self.x = player.x - 35
        if player.state == state['run']:
            if player.direction == direction['left']:
                self.x = player.x + 35
            elif player.direction == direction['right']:
                self.x = player.x - 35
        if player.state == state['jump']:
            if player.direction == direction['left']:
                self.x = player.x + 30
            elif player.direction == direction['right']:
                self.x = player.x - 30
        if player.state == state['dash']:
            if player.direction == direction['left']:
                self.x = player.x + 30
            elif player.direction == direction['right']:
                self.x = player.x - 30
        self.y = player.y - 25
        pass
    
    def draw(self, player):
        self.image.clip_draw(0, 0, 3, 3, self.x, self.y, 15, 15)
        pass