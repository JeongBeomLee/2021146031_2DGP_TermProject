from pico2d import *
import server
import game_framework
import game_world

from cursor     import BasicCursor
from background import TitleBackground
from background import TitleBackCloud
from background import TitleFrontCloud
from background import TitleLogo
from buttons    import TitlePlayButton
from buttons    import TitleExitButton

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        else:
            server.cursor.handle_event(event)

# 초기화
def enter():
    
    titleBackground = TitleBackground()
    titleBackCloud  = TitleBackCloud()
    titleFrontCloud = TitleFrontCloud()
    titleLogo       = TitleLogo()
    
    server.background.append(titleBackground)
    server.background.append(titleBackCloud)
    server.background.append(titleFrontCloud)
    server.background.append(titleLogo)
    
    game_world.add_objects(server.background, 0)
    
    titlePlayButton = TitlePlayButton()
    titleExitButton = TitleExitButton()
    
    server.button.append(titlePlayButton)
    server.button.append(titleExitButton)
    
    game_world.add_objects(server.button, 0)
    
    server.cursor = BasicCursor()
    game_world.add_object(server.cursor, 1)
    
    game_world.add_collision_pairs(server.cursor, server.button, 'cursor:button')
    
    

# 종료
def exit():
    game_world.clear()

def update():
    game_world.update()
    for a, b, group in game_world.all_collision_pairs():
        if collide(a, b):
            # print('COLLISION ', group)
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
