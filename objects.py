from pico2d import *
import server
import game_world
import game_framework


# 맵
mapSort = {'VILLIAGE' : 0, 'MOVE' : 1, 'JUMP' : 2, 'DASH' : 3, 'BATTLE' : 4, 'BOSS' : 5}
    
class Ground:
    
    def __init__(self, x, y, w, h):
        self.x  = x
        self.y  = y
        self.sx = self.x - server.map.window_left
        self.sy = self.y - server.map.window_bottom
        self.w  = w
        self.h  = h
    
    def update(self):
        self.sx = self.x - server.map.window_left
        self.sy = self.y - server.map.window_bottom
    
    def draw(self):
        draw_rectangle(*self.get_bb())
        
    def get_bb(self):
        return self.sx, self.sy, self.sx + self.w + 1, self.sy + self.h
    
    #### 객체별 충돌처리 ####
    def handle_collision(self, other, group):
        pass

class Stepstone:
    
    def __init__(self, x, y, w):
        self.x  = x
        self.y  = y
        self.sx = self.x - server.map.window_left
        self.sy = self.y - server.map.window_bottom
        self.w  = w
    
    def update(self):
        self.sx = self.x - server.map.window_left
        self.sy = self.y - server.map.window_bottom
    
    def draw(self):
        draw_rectangle(*self.get_bb())
        
    def get_bb(self):
        return self.sx, self.sy - 5, self.sx + self.w + 1, self.sy
    
    #### 객체별 충돌처리 ####
    def handle_collision(self, other, group):
        pass

DGE_TIME_PER_ACTION     = 125
DGE_ACTION_PER_TIME     = 1.0 / DGE_TIME_PER_ACTION
DGE_FRAMES_PER_ACTION   = 28

class DungeonEat:
    image = None
    eat_sound = None
    def __init__(self, x, y):
        if DungeonEat.image == None:
            DungeonEat.image = load_image("resources/images/Villiage/DungeonEat.png")
        self.x     = x
        self.y     = y + 175
        self.frame = 0
        if DungeonEat.eat_sound is None:
            DungeonEat.eat_sound = load_wav("resources/sounds/DungreedSound/nyam.wav")
            DungeonEat.eat_sound.set_volume(32)
        

        
    def update(self):
        self.frame = (self.frame + DGE_FRAMES_PER_ACTION * DGE_ACTION_PER_TIME) % 29
    
    def draw(self):
        self.sx    = self.x - server.map.window_left
        self.sy    = self.y - server.map.window_bottom
        self.image.clip_draw(int(self.frame) * 120, 0, 120, 90, self.sx, self.sy, 600, 450)
        if self.frame >= 9:
            server.player.isOn = False
            DungeonEat.eat_sound.play()
        if self.frame >= 28:
            import move_state
            
            game_world.remove_object(self)
            game_framework.change_state(move_state)
        
    def get_bb(self):
        pass
    
    def handle_collision(self, other, group):
        pass

class Trigger:
    
    out_sound = None
    def __init__(self, x, y, w, h):
        self.x  = x
        self.y  = y
        self.sx = self.x - server.map.window_left
        self.sy = self.y - server.map.window_bottom
        self.w  = w
        self.h  = h
        self.isOn = False
        
        if Trigger.out_sound is None:
            Trigger.out_sound = load_wav("resources/sounds/DungreedSound/DungeonOut.wav")
            Trigger.out_sound.set_volume(32)
    
    def update(self):
        self.sx = self.x - server.map.window_left
        self.sy = self.y - server.map.window_bottom
    
    def draw(self):
        draw_rectangle(*self.get_bb())
        
    def get_bb(self):
        return self.sx, self.sy, self.sx + self.w + 1, self.sy + self.h
    
    #### 객체별 충돌처리 ####
    def handle_collision(self, other, group):
        if group == 'player:trigger':
            if server.map.sort == mapSort['VILLIAGE']:
                if not self.isOn:
                    Trigger.out_sound.play()
                    server.player.canMove = False
                    dungeonEat = DungeonEat(server.player.x, server.player.y)
                    game_world.add_object(dungeonEat, 0)
                    self.isOn = True
                

class Door:
    
    def __init__(self, x, y, w, h):
        self.x  = x
        self.y  = y
        self.sx = self.x - server.map.window_left
        self.sy = self.y - server.map.window_bottom
        self.w  = w
        self.h  = h
    
    def update(self):
        self.sx = self.x - server.map.window_left
        self.sy = self.y - server.map.window_bottom
    
    def draw(self):
        draw_rectangle(*self.get_bb())
        
    def get_bb(self):
        return self.sx, self.sy, self.sx + self.w + 1, self.sy + self.h
    
    #### 객체별 충돌처리 ####
    def handle_collision(self, other, group):
        if group == 'player:door':
            if server.map.sort == mapSort['MOVE']:
                import boss_state
                game_framework.change_state(boss_state)
        
    
