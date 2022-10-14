from pico2d import *
import Characters_Player
from Characters_Player import state, direction

# 캐릭터 속성 변경은 여기서

quitMassage = False

def check_bottom(player): # 바닥체크
    pass

def events(player):
    global state
    global direction
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
                if player.state != state['jump']:
                    player.state = state['jump']
                    player.jumpSpeed = 10
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
            if player.x > event.x:
                player.direction = direction['left']
                flip = 'h'
            elif player.x <= event.x:
                player.direction = direction['right']
                flip = 'n'
            pass
    pass