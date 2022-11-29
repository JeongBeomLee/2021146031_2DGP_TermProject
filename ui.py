from pico2d import*

class EnemyLifeBar:
    image = None
    
    def __init__(effect, object):
        if EnemyLifeBar.image == None:
            EnemyLifeBar.image = load_image("resources/images/gameScene/ui/LifeBar.png")
            
        effect.x    = object.x - 50
        effect.y    = object.y - (object.h // 2) - 50
        effect.hp   = object.hp
        effect.isOn = True    
            
    def update(effect, object):
        effect.x  = object.x - 50
        effect.y  = object.y - (object.h // 2) - 50
        effect.hp = object.hp
    
    def draw(effect, object):
        # effect.image.clip_composite_draw(0, 0, 1, 10, 0, 'n', effect.x, effect.y, effect.hp / object.hpMax * 100, 10)
        effect.image.clip_draw_to_origin(0, 0, 1, 10, effect.x, effect.y,  effect.hp / object.hpMax * 100, 10)
        
class PlayerUI:
    lifeBarImage   = None
    dashCountImage = None
    
    def __init__(effect, object):
        if PlayerUI.lifeBarImage == None:
            PlayerUI.lifeBarImage = load_image("resources/images/gameScene/ui/LifeBar.png")
            
        effect.x    = object.x - 50
        effect.y    = object.y - (object.h // 2) - 50
        effect.hp   = object.hp
        effect.isOn = True    
            
    def update(effect, object):
        effect.x  = object.x - 50
        effect.y  = object.y - (object.h // 2) - 50
        effect.hp = object.hp
    
    def draw(effect, object):
        # effect.image.clip_composite_draw(0, 0, 1, 10, 0, 'n', effect.x, effect.y, effect.hp / object.hpMax * 100, 10)
        effect.image.clip_draw_to_origin(0, 0, 1, 10, effect.x, effect.y,  effect.hp / object.hpMax * 100, 10)
        
        
                