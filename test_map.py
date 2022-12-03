from pico2d import *

class Ground:
    groundImage = None
    
    def __init__(self):
        if Ground.groundImage == None:
            Ground.groundImage = load_image('test_ground.png')
        self.x = 800
        self.y = 80
    
    def update(self):
        pass
    
    def draw(self):
        self.groundImage.clip_draw(0, 0, self.groundImage.w, self.groundImage.h, self.x, self.y, self.groundImage.w * 20, self.groundImage.h * 10)
        draw_rectangle(*self.get_bb())
        
    def get_bb(self):
        return self.x - self.groundImage.w * 10, self.y - self.groundImage.h * 5, self.x + self.groundImage.w * 10 - 1, self.y + self.groundImage.h * 5
    
    #### 객체별 충돌처리 ####
    def handle_collision(self, other, group):
        pass
    
class Stepstone:
    stepstoneImage = None
    
    def __init__(self):
        if Stepstone.stepstoneImage == None:
            Stepstone.stepstoneImage = load_image('test_stepstone.png')
        self.x = 800
        self.y = 450
    
    def update(self):
        pass
    
    def draw(self):
        self.stepstoneImage.clip_draw(0, 0, self.stepstoneImage.w, self.stepstoneImage.h, self.x, self.y, self.stepstoneImage.w * 5, self.stepstoneImage.h * 5)
        draw_rectangle(*self.get_bb())
        pass
    
    def get_bb(self):
        return self.x - self.stepstoneImage.w * 5 / 2, self.y + self.stepstoneImage.h * 5 / 2 - 5,  self.x + self.stepstoneImage.w * 5 / 2, self.y + self.stepstoneImage.h * 5 / 2
    
    #### 객체별 충돌처리 ####
    def handle_collision(self, other, group):
        pass