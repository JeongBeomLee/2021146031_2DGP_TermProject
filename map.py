from pico2d import*
import server

mapSort = {'VILLIAGE' : 0, 'MOVE' : 1, 'JUMP' : 2, 'DASH' : 3, 'BATTLE' : 4, 'BOSS' : 5}

class VilliageTileMap:
    images = [[]]
    
    def __init__(self):
        self.canvas_width  = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.w = 1600 * 4
        self.h = 900 * 2
        self.sort = mapSort['VILLIAGE']
        self.window_left   = 0
        self.window_bottom = 0
        
        VilliageTileMap.images = [ [ load_image("resources/images/Map/villiage_state_map/villiage_%d%d.png" % (y, x)) for x in range(4) ] for y in range(2) ]
    
    def update(self):
        pass
    
    def draw(self):
        self.window_left = clamp(0, int(server.player.x) - self.canvas_width // 2, self.w - self.canvas_width - 1)
        self.window_bottom = clamp(0, int(server.player.y) - self.canvas_height // 2, self.h - self.canvas_height - 1)

        tile_left     = self.window_left // self.canvas_width
        tile_right    = (self.window_left + self.canvas_width) // self.canvas_width
        left_offset   = self.window_left % self.canvas_width
        tile_bottom   = self.window_bottom // self.canvas_height
        tile_top      = (self.window_bottom + self.canvas_height) // self.canvas_height
        bottom_offset = self.window_bottom % self.canvas_height
        
        for ty in range(tile_bottom, tile_top + 1):
            for tx in range(tile_left, tile_right + 1):
                self.images[ty][tx].draw_to_origin(-left_offset + (tx - tile_left) * self.canvas_width, 
                                                   -bottom_offset + (ty - tile_bottom) * self.canvas_height, self.canvas_width, self.canvas_height)
