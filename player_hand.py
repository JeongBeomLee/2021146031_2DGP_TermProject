from pico2d import *

# 캐릭터 상태, 방향
state      = {'IDLE'  : 0,  'RUN' : 1, 'JUMP' : 2, 'DASH' : 3, 'DIE' : 4}
direction  = {'RIGHT' : 1, 'LEFT' : 0}

class Hand:
    image = None
    
    def __init__(hand, player):
        hand.x = player.sx - 35
        hand.y = player.sy - 25
        if Hand.image == None:
            Hand.image = load_image('resources/images/Characters/Player/Costume/common/player_hand.png')
        
    def update(hand, player):
        global direction
        global state
        if player.state == state['IDLE']:
            if player.direction == direction['LEFT']:
                hand.x = player.sx + 35
            elif player.direction == direction['RIGHT']:
                hand.x = player.sx - 35
        if player.state == state['RUN']:
            if player.direction == direction['LEFT']:
                hand.x = player.sx + 35
            elif player.direction == direction['RIGHT']:
                hand.x = player.sx - 35
        if player.state == state['JUMP']:
            if player.direction == direction['LEFT']:
                hand.x = player.sx + 30
            elif player.direction == direction['RIGHT']:
                hand.x = player.sx - 30
        if player.state == state['DASH']:
            if player.direction == direction['LEFT']:
                hand.x = player.sx + 30
            elif player.direction == direction['RIGHT']:
                hand.x = player.sx - 30
        hand.y = player.sy - 25
        pass
    
    def draw(hand):
        hand.image.clip_draw(0, 0, 3, 3, hand.x, hand.y, 15, 15)