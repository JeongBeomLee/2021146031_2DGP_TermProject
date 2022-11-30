from pico2d import*

class ShootingCursor:
    image = None
    
    def __init__(self):
        if ShootingCursor.image == None:
            ShootingCursor.image = load_image("resources/images/common/cursor/ShootingCursor2.png")
        
        self.x = 0
        self.y = 0
        self.canvas_width  = get_canvas_width()
        self.canvas_height = get_canvas_height()
            
    #### 바운딩 박스 받기 ####
    def get_bb(self):
        return self.x - 1, self.y - 1, self.x + 1, self.y + 1
    
    #### 객체별 충돌처리 ####
    def handle_collision(self, other, group):
        pass
    
    def update(self):
        pass
            
    def draw(self):
        self.image.clip_draw(0, 0, 21, 21, self.x, self.y, 21 * 3, 21 * 3)
    
    def handle_event(self, event):
        if event.type == SDL_MOUSEMOTION:
            self.x = event.x
            self.y = self.canvas_height - event.y
            