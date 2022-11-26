from pico2d import *
from math import *
import game_framework
import game_world

# 한손검 이펙트 프레임
SSS_TIME_PER_ACTION    = 0.3
SSS_ACTION_PER_TIME    = 1.0 / SSS_TIME_PER_ACTION
SSS_FRAMES_PER_ACTION  = 3

# 곡괭이 이펙트 프레임
RPS_TIME_PER_ACTION    = 0.3
RPS_ACTION_PER_TIME    = 1.0 / RPS_TIME_PER_ACTION
RPS_FRAMES_PER_ACTION  = 5

# 자동권총 이펙트 프레임
SE_TIME_PER_ACTION    = 0.09
SE_ACTION_PER_TIME    = 1.0 / SE_TIME_PER_ACTION
SE_FRAMES_PER_ACTION  = 3

# 캐릭터 상태, 방향
state      = {'IDLE'  : 0,  'RUN' : 1, 'JUMP' : 2, 'DASH' : 3}
direction  = {'RIGHT' : 1, 'LEFT' : 0}

class ShortSwordSwing:
    image = None
    def __init__(effect, weaponDeg, player):
        if ShortSwordSwing.image == None:
            ShortSwordSwing.image = load_image('resources/images/weapon/MeleeWeapon/SwingFX.png')
        
        if player.direction == direction['LEFT']:
            effect.x = player.x - 100 * cos(radians(weaponDeg + 90))
            effect.y = player.y - 100 * sin(radians(weaponDeg + 90))
        if player.direction == direction['RIGHT']:
            effect.x = player.x + 100 * cos(radians(weaponDeg - 90))
            effect.y = player.y - 100 * sin(radians(weaponDeg + 90))
            
        if player.direction == direction['LEFT']:
            effect.direction = 0
            effect.deg = weaponDeg + 90
        if player.direction == direction['RIGHT']:
            effect.direction = 1
            effect.deg = weaponDeg - 90

        effect.frame = 0.0
        effect.isOn = True    
            
    def update(effect):
        if effect.isOn:
            if effect.frame >= 3.0:
                effect.frame = 0.0
                effect.isOn = False
                game_world.remove_object(effect)
            effect.frame = effect.frame = (effect.frame + SSS_FRAMES_PER_ACTION * SSS_ACTION_PER_TIME * game_framework.frame_time) % 4
    
    def draw(effect):
        if effect.isOn:
            if effect.direction == 0:
                effect.image.clip_composite_draw(int(effect.frame) * 28, 0, 28, 40, radians(effect.deg), 'h', effect.x, effect.y, 140, 200)
            elif effect.direction == 1:
                effect.image.clip_composite_draw(int(effect.frame) * 28, 0, 28, 40, radians(effect.deg), 'n', effect.x, effect.y, 140, 200)

class RedPickaxeSwing:
    image = None
    rectImage = None
    def __init__(effect, weaponDeg, player):
        global direction
        if RedPickaxeSwing.image == None:
            RedPickaxeSwing.image = load_image('resources/images/weapon/MeleeWeapon/RedPickaxeSwing.png')
        if RedPickaxeSwing.rectImage == None:
            RedPickaxeSwing.rectImage = load_image('resources/images/weapon/MeleeWeapon/RedPickaxeSwingRect.png')
            
        if player.direction == direction['LEFT']:
            effect.x = player.x + 165 * cos(radians(weaponDeg))
            effect.y = player.y + 165 * sin(radians(weaponDeg))
        if player.direction == direction['RIGHT']:
            effect.x = player.x - 165 * cos(radians(weaponDeg))
            effect.y = player.y - 165 * sin(radians(weaponDeg))
        
        if player.direction == direction['LEFT']:
            effect.direction = 0
        if player.direction == direction['RIGHT']:
            effect.direction = 1
            
        effect.deg = weaponDeg
        effect.frame = 0
        effect.isOn = True
        
    
    def update(effect):
        if effect.isOn:
            if effect.frame >= 13.0:
                effect.frame = 0
                effect.isOn = False
                game_world.remove_object(effect)
            effect.frame = (effect.frame + RPS_FRAMES_PER_ACTION * RPS_ACTION_PER_TIME * game_framework.frame_time) % 14
    
    def draw(effect):
        if effect.isOn:
            if effect.direction == 0:
                effect.image.clip_composite_draw(int(effect.frame) * 22, 0, 22, 56, radians(effect.deg), 'n', effect.x, effect.y, 110, 280)
                # self.rectImage.clip_composite_draw(0, 0, 110, 280, radians(self.deg), 'n', self.x, self.y, 110, 280)
            elif effect.direction == 1:
                effect.image.clip_composite_draw(int(effect.frame) * 22, 0, 22, 56, radians(effect.deg), 'h', effect.x, effect.y, 110, 280)
                # self.rectImage.clip_composite_draw(0, 0, 110, 280, radians(self.deg), 'h', self.x, self.y, 110, 280)
    
class LightBringerEffect:
    image = None
        
    def __init__(effect, x, y) :
        if LightBringerEffect.image == None:
            LightBringerEffect.image = load_image("resources/images/weapon/longDistanceWeapon/light.png")
        
        effect.x = x
        effect.y = y
        effect.f_opacify = 1.0
        
    def update(effect):
        effect.f_opacify -= 0.05
        if effect.f_opacify <= 0:
                game_world.remove_object(effect)
            
    def draw(effect):
        effect.image.opacify(effect.f_opacify)
        effect.image.clip_composite_draw(0, 0, 151, 153, 0, 'n', effect.x, effect.y, 453, 459)

class ShootEffect:
    image = None
    
    def __init__(effect, weapon, weapon_deg, player):
        if ShootEffect.image == None:
            ShootEffect.image = load_image("resources/images/weapon/longDistanceWeapon/effect/ShootEffect.png")
        
        if player.direction == direction['LEFT']:
            effect.x = weapon.x - 50 * cos(radians(weapon_deg + 90))
            effect.y = weapon.y - 50 * sin(radians(weapon_deg + 80))
        if player.direction == direction['RIGHT']:
            effect.x = weapon.x + 50 * cos(radians(weapon_deg - 90))
            effect.y = weapon.y - 50 * sin(radians(weapon_deg + 90))
            
        if player.direction == direction['LEFT']:
            effect.direction = 0
            effect.deg = weapon_deg + 90
            
        if player.direction == direction['RIGHT']:
            effect.direction = 1
            effect.deg = weapon_deg - 90

        effect.frame = 0.0
        effect.isOn = True    
            
    def update(effect):
        if effect.isOn:
            if effect.frame >= 3.0:
                effect.frame = 0.0
                effect.isOn = False
                game_world.remove_object(effect)
            effect.frame = effect.frame = (effect.frame + SE_FRAMES_PER_ACTION * SE_ACTION_PER_TIME * game_framework.frame_time) % 4
    
    def draw(effect):
        if effect.isOn:
            if effect.direction == 0:
                effect.image.clip_composite_draw(int(effect.frame) * 14, 0, 14, 15, radians(effect.deg), 'h', effect.x, effect.y, 70, 75)
            elif effect.direction == 1:
                effect.image.clip_composite_draw(int(effect.frame) * 14, 0, 14, 15, radians(effect.deg), 'n', effect.x, effect.y, 70, 75)
