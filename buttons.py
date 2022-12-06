from pico2d import *
import server
import game_framework
import villiage_state

class TitlePlayButton:
    offImage = None
    onImage = None
    
    def __init__(self):
        if TitlePlayButton.offImage == None:
            TitlePlayButton.offImage = load_image("resources/images/MainScene/PlayOff_Kor.png")
        if TitlePlayButton.onImage == None:
            TitlePlayButton.onImage = load_image("resources/images/MainScene/PlayOn_Kor.png")
        
        self.x    = 700
        self.y    = 260
        self.isOn = False
        self.doOn = False
            
    def get_bb(self):
        return self.x, self.y, self.x + 36 * 5, self.y + 12*5
    
    def handle_collision(self, other, group):
        if group == 'cursor:button':
            self.isOn = True
            
    def update(self):
        self.isOn = False
            
    def draw(self):
        if self.isOn == False:
            self.offImage.clip_draw_to_origin(0, 0, 36, 12, self.x, self.y, 36 * 5, 12 * 5)
        else:
            self.onImage.clip_draw_to_origin(0, 0, 36, 12, self.x, self.y, 36 * 5, 12 * 5)
    
    def handle_event(self, event):
        pass 
    
    def do(self):
        game_framework.change_state(villiage_state)
        
    
class TitleExitButton:
    offImage = None
    onImage = None
    
    def __init__(self):
        if TitleExitButton.offImage == None:
            TitleExitButton.offImage = load_image("resources/images/MainScene/ExitOff_Kor.png")
        if TitleExitButton.onImage == None:
            TitleExitButton.onImage = load_image("resources/images/MainScene/ExitOn_Kor.png")
        
        self.x    = 740
        self.y    = 175
        self.isOn = False
            
    def get_bb(self):
        return self.x, self.y, self.x + 21 * 5, self.y + 12 * 5
    
    def handle_collision(self, other, group):
        if group == 'cursor:button':
            self.isOn = True
            
    def update(self):
        self.isOn = False
        pass
            
    def draw(self):
        if self.isOn == False:
            self.offImage.clip_draw_to_origin(0, 0, 21, 12, self.x, self.y, 21 * 5, 12 * 5)
        else:
            self.onImage.clip_draw_to_origin(0, 0, 21, 12, self.x, self.y, 21 * 5, 12 * 5)
    
    def handle_event(self, event):
        pass 
    
    def do(self):
        game_framework.quit()