from pico2d import *

# 캐릭터 행위 변경은 여기서

state = {'idle' : 0, 'run' : 1, 'jump' : 2}
direction = {'left' : 0, 'right' : 1}

class Player:
    def __init__(self): # 생성자
        self.x, self.y = 800, 50 # 캐릭터 초기 위치
        self.idleFrame = 0
        self.runFrame = 0
        self.state = state['idle']
        self.direction = direction['right']
        self.speedLR = 0
        self.jumpSpeed = 0
        self.image = load_image('resources/images/Characters/Player/Costume/common/player_idle.png') # 캐릭터 이미지

    def update(self): # 업데이트 함수
        if self.state == state['idle']: # idle상태 일 때
            if self.speedLR != 0: # 점프 완료 후 idle 이미지를 띄울지 run 이미지를 띄울지 결정해줌
                self.state = state['run']
                pass
            
            self.image = load_image('resources/images/Characters/Player/Costume/common/player_idle.png')
            self.idleFrame = (self.idleFrame + 1) % 5

        if self.state == state['run']:
            self.image = load_image('resources/images/Characters/Player/Costume/common/player_run.png')
            self.runFrame = (self.runFrame + 1) % 8
            
        if self.state == state['jump']:
            self.image = load_image('resources/images/Characters/Player/Costume/common/player_jump.png')
            
            if self.jumpSpeed > 0:
                F = (0.5 * 1 * (self.jumpSpeed ** 2))
            else:
                F = - (0.5 * 1 * (self.jumpSpeed ** 2))
                
            self.y += round(F)
            self.jumpSpeed -= 1
            
            if self.y < 50:
                self.y = 50
                self.state = state['idle']
                self.jumpSpeed = 10
        self.x += self.speedLR * 18

        # fill more
    def draw(self): # 그리기 함수
        # 프레임 위치부터 w 25, h 20만큼 x, y에 그린다
        if self.state == state['idle']:
            if self.direction == direction['left']:
                self.image.clip_composite_draw(self.idleFrame * 15, 0, 15, 20, 0, 'h', self.x, self.y, 75, 100)
            if self.direction == direction['right']:
                self.image.clip_composite_draw(self.idleFrame * 15, 0, 15, 20, 0, 'n', self.x, self.y, 75, 100)
            
        if self.state == state['run']:
            if self.direction == direction['left']:
                self.image.clip_composite_draw(self.runFrame * 17, 0, 17, 20, 0, 'h', self.x, self.y, 85, 100)
            if self.direction == direction['right']:
                self.image.clip_composite_draw(self.runFrame * 17, 0, 17, 20, 0, 'n', self.x, self.y, 85, 100)
            
        if self.state == state['jump']:
            if self.direction == direction['left']:
                self.image.clip_composite_draw(0, 0, 17, 20, 0, 'h', self.x, self.y, 85, 100)
            if self.direction == direction['right']:
                self.image.clip_composite_draw(0, 0, 17, 20, 0, 'n', self.x, self.y, 85, 100)
            

        