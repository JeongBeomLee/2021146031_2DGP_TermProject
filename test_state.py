from pico2d import *
import game_framework
import game_world

from player   import Player
from test_map import Ground
from test_map import Stepstone
from monster  import Big_Skel_Sword

import effects

player    = None
ground    = None
stepstone = None
monster   = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        else:
            player.handle_event(event)

# 초기화
def enter():
    global player, ground, stepstone, monster
    player    = Player()
    ground    = Ground()
    stepstone = Stepstone()
    monster   = Big_Skel_Sword()
    
    game_world.add_object(player, 1)
    game_world.add_object(monster, 1)
    game_world.add_object(ground, 0)
    game_world.add_object(stepstone, 0)
    
    game_world.add_collision_pairs(player, ground,    'player:ground')
    game_world.add_collision_pairs(player, stepstone, 'player:stepstone')
    
    game_world.add_collision_pairs(monster, ground,    'monster:ground')
    game_world.add_collision_pairs(monster, stepstone, 'monster:stepstone')
    


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
    import test_state

    pico2d.open_canvas()
    game_framework.run(test_state)
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
