from pico2d import*
import server

state      = {'IDLE'  : 0,  'RUN' : 1, 'JUMP' : 2, 'DASH' : 3, 'DIE' : 4}

class Feet:
    
    def __init__(self, x, y):
        self.x  = x
        self.y  = y
        self.sx = self.x - server.map.window_left
        self.sy = self.y - server.map.window_bottom
    
    def update(self):
        self.x  = server.player.x
        self.y  = server.player.y
        self.sx = self.x - server.map.window_left
        self.sy = self.y - server.map.window_bottom
    
    def draw(self):
        draw_rectangle(*self.get_bb())
        
    def get_bb(self):
        return self.sx - 10, self.sy - 50, self.sx + 10, self.sy - 30
    
    #### 객체별 충돌처리 ####
    def handle_collision(self, other, group):
        if group == 'feet:stepstone'and server.player.jumpHeight < 0:
            server.player.y = other.sy  + 50 + 1
            if server.player.state == state['JUMP']:
                server.player.state = state['IDLE']
            server.player.jumpHeight    = 0
            server.player.jumpCount     = 0
            server.player.isOnStepstone = True
            server.player.isOnGround    = False