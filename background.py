from pico2d import*
import game_framework

class TitleBackground:
    image = None
    
    def __init__(self):
        if TitleBackground.image == None:
            TitleBackground.image = load_image("resources/images/MainScene/background.png")
        
        self.x = 0
        self.y = 0
        self.canvas_width  = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.bgm = load_music("resources/sounds/stage/bgm/0.Town.wav")
        self.bgm.set_volume(32)
        self.bgm.repeat_play()
            
    def get_bb(self):
        pass
    
    def handle_collision(self, other, group):
        pass
    
    def update(self):
        pass
            
    def draw(self):
        self.image.clip_draw_to_origin(0, 0, self.canvas_width + 1, self.canvas_height, self.x, self.y, self.canvas_width + 1, self.canvas_height)
    
    def handle_event(self, event):
        pass  

PIXEL_PER_METER = (10.0 / 0.3)
CLOUD_SPEED_KMPH  = 1.0
CLOUD_SPEED_MPM   = (CLOUD_SPEED_KMPH * 1000.0 / 60.0)
CLOUD_SPEED_MPS   = (CLOUD_SPEED_MPM / 60.0)
CLOUD_SPEED_PPS   = (CLOUD_SPEED_MPS * PIXEL_PER_METER)

class TitleBackCloud:
    image = None
    
    def __init__(self):
        if TitleBackCloud.image == None:
            TitleBackCloud.image = load_image("resources/images/MainScene/BackCloud2.png")
        
        self.x = 0
        self.y = 0
        self.canvas_width  = get_canvas_width()
        self.canvas_height = get_canvas_height()
            
    def get_bb(self):
        pass
    
    def handle_collision(self, other, group):
        pass
    
    def update(self):
        self.x += CLOUD_SPEED_PPS * game_framework.frame_time
        
        if self.x >= 640:
            self.x = 0
        pass
            
    def draw(self):
        self.image.clip_draw_to_origin(int(self.x), 0, 320, 180, 0, 0, 1600, 900)
        
    
    def handle_event(self, event):
        pass  
    
class TitleFrontCloud:
    image = None
    
    def __init__(self):
        if TitleFrontCloud.image == None:
            TitleFrontCloud.image = load_image("resources/images/MainScene/FrontCloud2.png")
        
        self.x = 0
        self.y = 0
        self.canvas_width  = get_canvas_width()
        self.canvas_height = get_canvas_height()
            
    def get_bb(self):
        pass
    
    def handle_collision(self, other, group):
        pass
    
    def update(self):
        self.x += CLOUD_SPEED_PPS * game_framework.frame_time * 2.5
        
        if self.x >= 574:
            self.x = 0
        pass
            
    def draw(self):
        self.image.clip_draw_to_origin(int(self.x), 0, 574 // 2, 180, 0, 0, 1600, 900)
        
    
    def handle_event(self, event):
        pass  
    
class TitleLogo:
    image = None
    
    def __init__(self):
        if TitleLogo.image == None:
            TitleLogo.image = load_image("resources/images/MainScene/MainLogo.png")
        
        self.x = 400
        self.y = 370
            
    def get_bb(self):
        pass
    
    def handle_collision(self, other, group):
        pass
    
    def update(self):
        pass
            
    def draw(self):
        self.image.clip_draw_to_origin(0, 0, 156, 75, self.x, self.y, 156 * 5, 75 * 5)
    
    def handle_event(self, event):
        pass  
    
class VilliageSky:
    image = None
    
    def __init__(self):
        if VilliageSky.image == None:
            VilliageSky.image = load_image("resources/images/Villiage/Sky_Day.png")
        
        self.x = 0
        self.y = 0
        self.canvas_width  = get_canvas_width()
        self.canvas_height = get_canvas_height()
            
    def get_bb(self):
        pass
    
    def handle_collision(self, other, group):
        pass
    
    def update(self):
        pass
            
    def draw(self):
        self.image.clip_draw_to_origin(0, 0, 320, 180, self.x, self.y, self.canvas_width + 1, self.canvas_height)
    
    def handle_event(self, event):
        pass 
    
class VilliageBackTrees:
    image = None
    
    def __init__(self):
        if VilliageBackTrees.image == None:
            VilliageBackTrees.image = load_image("resources/images/Villiage/TownBG_Day.png")
        
        self.x = 0
        self.y = 0
        self.canvas_width  = get_canvas_width()
        self.canvas_height = get_canvas_height()
            
    def get_bb(self):
        pass
    
    def handle_collision(self, other, group):
        pass
    
    def update(self):
        pass
            
    def draw(self):
        self.image.clip_draw_to_origin(0, 0, 320, 142, self.x, self.y, self.canvas_width + 1, 142 * 5)
    
    def handle_event(self, event):
        pass  
    
class VilliageFrontTrees:
    image = None
    
    def __init__(self):
        if VilliageFrontTrees.image == None:
            VilliageFrontTrees.image = load_image("resources/images/Villiage/TownLayer_Day.png")
        
        self.x = 0
        self.y = 0
        self.canvas_width  = get_canvas_width()
        self.canvas_height = get_canvas_height()
            
    def get_bb(self):
        pass
    
    def handle_collision(self, other, group):
        pass
    
    def update(self):
        pass
            
    def draw(self):
        self.image.clip_draw_to_origin(0, 0, 320, 95, self.x, self.y, self.canvas_width + 1, 95 * 5)
    
    def handle_event(self, event):
        pass  