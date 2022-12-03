from pico2d import *
import server

# 캐릭터 상태, 방향
state      = {'IDLE'  : 0,  'RUN' : 1, 'JUMP' : 2, 'DASH' : 3, 'DIE' : 4}
direction  = {'RIGHT' : 1, 'LEFT' : 0}

class Feet:
    
    def __init__(feet, player):
        feet.x = player.x
        feet.y = player.y - 50
    
     #### 바운딩 박스 받기 ####
    def get_bb(feet):
        return feet.x - 20, feet.y, feet.x + 20, feet.y + 20
    
    #### 객체별 충돌처리 ####
    def handle_collision(feet, other, group):
        #### 바닥 충돌처리 ####
        if group == 'feet:ground':
            server.player.y = other.y + other.groundImage.h * 5 + 50 + 1   ### 땅의 바운딩박스 top + 플레이어 피봇 기준 발위치 + 1 pixel
            if server.player.state == state['JUMP']:
                server.player.state = state['IDLE']
            server.player.jumpHeight    = 0
            server.player.jumpCount     = 0
            server.player.isOnGround    = True
            
        else:
            server.player.isOnGround    = False
            
        if group == 'feet:stepstone'and server.player.jumpHeight < 0:
            server.player.y = other.y + other.stepstoneImage.h * 5 / 2 + 50 + 1
            if server.player.state == state['JUMP']:
                server.player.state = state['IDLE']
            server.player.jumpHeight    = 0
            server.player.jumpCount     = 0
            server.player.isOnStepstone = True
            # server.player.isOnGround    = False
        else:
            server.player.isOnStepstone = False
            
        feet.update(server.player)

    def update(feet, player):
        feet.x = player.x
        feet.y = player.y - 50
        
    def draw(feet):
        draw_rectangle(*feet.get_bb())
        