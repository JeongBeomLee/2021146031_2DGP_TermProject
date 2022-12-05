from pico2d import *
import server
import game_framework
import game_world

from player   import Player
from monster  import Big_Skel_Sword
from cursor   import ShootingCursor
from map      import VilliageTileMap
from objects  import Ground



def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        else:
            server.player.handle_event(event)
            server.cursor.handle_event(event)

# 초기화
def enter():
    server.map       = VilliageTileMap()
    game_world.add_object(server.map, 0)
    
    ground = Ground(0, 0, 1600 * 4, 32 * 5 - 5)
    server.ground.append(ground)
    game_world.add_objects(server.ground, 0)
    
    server.cursor    = ShootingCursor()
    game_world.add_object(server.cursor, 1)
    server.player    = Player()
    game_world.add_object(server.player, 1)
    
    server.monster   = Big_Skel_Sword()
    game_world.add_object(server.monster, 1)
    
    
    # game_world.add_collision_pairs(server.player,  server.ground,    'player:ground')
    # game_world.add_collision_pairs(server.player,  server.stepstone, 'player:stepstone')
    
    # game_world.add_collision_pairs(server.player,  server.monster,   'player:monster')

# 종료
def exit():
    game_world.clear()

def update():
    game_world.update()
    for a, b, group in game_world.all_collision_pairs():
        if collide(a, b):
            print('COLLISION ', group)
            a.handle_collision(b, group)
            b.handle_collision(a, group)

def draw_world():
    for game_object in game_world.all_objects():
        game_object.draw()

def draw():
    clear_canvas()
    draw_world()
    update_canvas()

def pause():
    pass

def resume():
    pass

def test_self():
    import server

    pico2d.open_canvas()
    game_framework.run(server)
    pico2d.clear_canvas()

if __name__ == '__main__':
    test_self()
    
def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    
    if left_a   > right_b:  return False
    if right_a  < left_b:   return False
    if top_a    < bottom_b: return False
    if bottom_a > top_b:    return False
    
    return True
