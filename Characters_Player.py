from pico2d import *

state = {'idle' : 0, 'run' : 1, 'jump' : 2}
direction = {'left' : 0, 'right' : 1}

class Player:
    def __init__(self): # 생성자
        self.x, self.y = 800, 450 # 캐릭터 초기 위치
        self.idleFrame = 0
        self.runFrame = 0
        self.state = state['idle']
        self.direction = direction['right']
        self.speedLR = 0
        self.image = load_image('resources/images/Characters/Player/Costume/common/player_idle_right.png') # 캐릭터 이미지

    def update(self): # 업데이트 함수
        if self.state == state['idle']: # idle상태 일 때
            if self.direction == direction['left']: # 방향 체크후 방향에 맞는 이미지 출력과 Frame증가
                self.image = load_image('resources/images/Characters/Player/Costume/common/player_idle_left.png')
            elif self.direction == direction['right']:
                self.image = load_image('resources/images/Characters/Player/Costume/common/player_idle_right.png')
            self.idleFrame = (self.idleFrame + 1) % 5

        if self.state == state['run']:
            if self.direction == direction['left']:
                self.image = load_image('resources/images/Characters/Player/Costume/common/player_run_left.png')
            elif self.direction == direction['right']:
                self.image = load_image('resources/images/Characters/Player/Costume/common/player_run_right.png')
            self.runFrame = (self.runFrame + 1) % 8
        self.x += self.speedLR * 18

        # fill more
    def draw(self): # 그리기 함수
        # 프레임 위치부터 w 25, h 20만큼 x, y에 그린다
        if self.state == state['idle']:
            self.image.clip_draw(self.idleFrame * 15, 0, 15, 20, self.x, self.y, 75, 100)

        if self.state == state['run']:
            self.image.clip_draw(self.runFrame * 17, 0, 17, 20, self.x, self.y, 85, 100)
        