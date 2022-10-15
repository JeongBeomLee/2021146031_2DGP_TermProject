from pico2d import *
import Characters_Player
import Weapons_Short

from Characters_Player import state, direction
from Weapons_Short import deg

# 캐릭터 속성 변경은 여기서

quitMassage = False

def events(player):
    global state, direction, deg
    global quitMassage

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT: # 종료
            quitMassage = True
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_d: # 오른쪽 키 눌림
                player.speedLR += 1
                if player.state != state['jump']:
                    player.state = state['run'] # 상태 변경
                    player.runFrame = 0 # 프레임 초기화
                
            elif event.key == SDLK_a: # 왼쪽 키 눌림
                player.speedLR -= 1
                if player.state != state['jump']:
                    player.state = state['run'] # 상태 변경
                    player.runFrame = 0 # 프레임 초기화
                
            elif event.key == SDLK_w:
                # if player.state != state['jump']:
                if player.jumpCount != 2:
                    player.state = state['jump']
                    player.jumpSpeed = 10
                    player.jumpCount += 1
                    player.idleFrame = 0
                    player.runFrame = 0
                pass
            
            elif event.key == SDLK_s:
                pass
            
            elif event.key == SDLK_ESCAPE: # ESC키
                pass
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_d:
                player.speedLR -= 1
                if player.state != state['jump']:
                    player.state = state['idle']
                    player.idleFrame = 0 
            elif event.key == SDLK_a:
                player.speedLR += 1
                if player.state != state['jump']:
                    player.state = state['idle']
                    player.idleFrame = 0 
            elif event.key == SDLK_w:
                pass
            elif event.key == SDLK_s:
                pass
        elif event.type == SDL_MOUSEMOTION:
            Characters_Player.getMouse(event.x, event.y)
            Weapons_Short.getMouse(event.x, event.y)
            pass
    pass