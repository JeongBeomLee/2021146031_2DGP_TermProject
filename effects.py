from pico2d import *
from math import *
import server
import game_framework
import game_world
import weapons

# 한손검 이펙트 프레임
SSS_TIME_PER_ACTION    = 0.3
SSS_ACTION_PER_TIME    = 1.0 / SSS_TIME_PER_ACTION
SSS_FRAMES_PER_ACTION  = 3

# 곡괭이 이펙트 프레임
RPS_TIME_PER_ACTION    = 0.3
RPS_ACTION_PER_TIME    = 1.0 / RPS_TIME_PER_ACTION
RPS_FRAMES_PER_ACTION  = 5

# 자동권총 이펙트 프레임
SE_TIME_PER_ACTION    = 0.1
SE_ACTION_PER_TIME    = 1.0 / SE_TIME_PER_ACTION
SE_FRAMES_PER_ACTION  = 3

# 재장전 바 속도
PIXEL_PER_METER = (10.0 / 0.3)
RB_SPEED_KMPH   = 11.5
RB_SPEED_MPM    = (RB_SPEED_KMPH * 1000.0 / 60.0)
RB_SPEED_MPS    = (RB_SPEED_MPM / 60.0)
RB_SPEED_PPS    = (RB_SPEED_MPS * PIXEL_PER_METER)

# 재장전 이펙트 프레임
RELOAD_TIME_PER_ACTION    = 0.2
RELOAD_ACTION_PER_TIME    = 1.0 / RELOAD_TIME_PER_ACTION
RELOAD_FRAMES_PER_ACTION  = 4

# 총알 폭발 이펙트 프레임
BE_TIME_PER_ACTION    = 0.5
BE_ACTION_PER_TIME    = 1.0 / BE_TIME_PER_ACTION
BE_FRAMES_PER_ACTION  = 6

# 몬스터 사망 이펙트 프레임
DE_TIME_PER_ACTION    = 0.3
DE_ACTION_PER_TIME    = 1.0 / DE_TIME_PER_ACTION
DE_FRAMES_PER_ACTION  = 11

# 먼지 이펙트 프레임
DUST_TIME_PER_ACTION    = 0.5
DUST_ACTION_PER_TIME    = 1.0 / DUST_TIME_PER_ACTION
DUST_FRAMES_PER_ACTION  = 6

# 캐릭터 상태, 방향
state      = {'IDLE'  : 0,  'RUN' : 1, 'JUMP' : 2, 'DASH' : 3, 'DIE' : 4}
direction  = {'RIGHT' : 1, 'LEFT' : 0}

class ShortSwordSwing:
    image = None
    def __init__(effect, weaponDeg, player):
        if ShortSwordSwing.image == None:
            ShortSwordSwing.image = load_image('resources/images/weapon/MeleeWeapon/SwingFX.png')
        
        if player.direction == direction['LEFT']:
            effect.x = player.sx - 100 * cos(radians(weaponDeg + 90))
            effect.y = player.sy - 100 * sin(radians(weaponDeg + 90))
        if player.direction == direction['RIGHT']:
            effect.x = player.sx + 100 * cos(radians(weaponDeg - 90))
            effect.y = player.sy - 100 * sin(radians(weaponDeg + 90))
            
        if player.direction == direction['LEFT']:
            effect.direction = 0
            effect.deg = weaponDeg + 90
        if player.direction == direction['RIGHT']:
            effect.direction = 1
            effect.deg = weaponDeg - 90

        effect.frame = 0.0
        effect.isOn = True    
        effect.power = player.power + 10
    
    #### 바운딩 박스 받기 ####
    def get_bb(effect):
        return effect.x - 70, effect.y - 100, effect.x + 70, effect.y + 100
    
    #### 객체별 충돌처리 ####
    def handle_collision(effect, other, group):
        pass
            
    def update(effect):
        if effect.isOn:
            if effect.frame >= 3.0:
                effect.frame = 0.0
                effect.isOn = False
                game_world.remove_object(effect)
                game_world.remove_collision_pairs(effect, server.monster, 'shortSwordEffect:monster')
            effect.frame = (effect.frame + SSS_FRAMES_PER_ACTION * SSS_ACTION_PER_TIME * game_framework.frame_time) % 4
    
    def draw(effect):
        if effect.isOn:
            if effect.direction == 0:
                effect.image.clip_composite_draw(int(effect.frame) * 28, 0, 28, 40, radians(effect.deg), 'h', effect.x, effect.y, 140, 200)
            elif effect.direction == 1:
                effect.image.clip_composite_draw(int(effect.frame) * 28, 0, 28, 40, radians(effect.deg), 'n', effect.x, effect.y, 140, 200)
        draw_rectangle(*effect.get_bb())

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
            effect.x = player.sx + 165 * cos(radians(weaponDeg))
            effect.y = player.sy + 165 * sin(radians(weaponDeg))
        if player.direction == direction['RIGHT']:
            effect.x = player.sx - 165 * cos(radians(weaponDeg))
            effect.y = player.sy - 165 * sin(radians(weaponDeg))
        
        if player.direction == direction['LEFT']:
            effect.direction = 0
        if player.direction == direction['RIGHT']:
            effect.direction = 1
            
        effect.deg = weaponDeg
        effect.frame = 0
        effect.isOn = True
        effect.power = player.power + 10
        
    #### 바운딩 박스 받기 ####
    def get_bb(effect):
        return effect.x - 55, effect.y - 140, effect.x + 55, effect.y + 140
    
    #### 객체별 충돌처리 ####
    def handle_collision(effect, other, group):
        pass
    
    def update(effect):
        if effect.isOn:
            if effect.frame >= 13.0:
                effect.frame = 0
                effect.isOn = False
                game_world.remove_object(effect)
                game_world.remove_collision_pairs(effect, server.monster, 'pickaxeRedEffect:monster')
                
            effect.frame = (effect.frame + RPS_FRAMES_PER_ACTION * RPS_ACTION_PER_TIME * game_framework.frame_time) % 14
    
    def draw(effect):
        if effect.isOn:
            if effect.direction == 0:
                effect.image.clip_composite_draw(int(effect.frame) * 22, 0, 22, 56, radians(effect.deg), 'n', effect.x, effect.y, 110, 280)
            elif effect.direction == 1:
                effect.image.clip_composite_draw(int(effect.frame) * 22, 0, 22, 56, radians(effect.deg), 'h', effect.x, effect.y, 110, 280)
        draw_rectangle(*effect.get_bb())
    
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
                
class ReloadEffect:
    reloadBarImage  = None
    reloadBaseImage = None
    reloadImage     = None
    
    
    def __init__(effect, player):
        if ReloadEffect.reloadBarImage == None:
            ReloadEffect.reloadBarImage = load_image("resources/images/weapon/longDistanceWeapon/effect/ReloadBar.png")
        if ReloadEffect.reloadBaseImage == None:
            ReloadEffect.reloadBaseImage = load_image("resources/images/weapon/longDistanceWeapon/effect/ReloadBase.png")
        if ReloadEffect.reloadImage == None:
            ReloadEffect.reloadImage = load_image("resources/images/weapon/longDistanceWeapon/effect/Reload.png")    

        effect.reloadBaseX = player.sx
        effect.reloadBaseY = player.sy + 100
        
        effect.reloadBarX  = player.sx - 35
        effect.reloadBarY  = player.sy + 100
        effect.reloadBarDX = 0.0
        
        effect.reloadX     = player.sx
        effect.reloadY     = player.sy + 100
        
        effect.isOn      = True
        effect.frame     = 0.0
        effect.afterIsOn = False
            
    def update(effect):
        effect.reloadBaseX = server.player.sx
        effect.reloadBaseY = server.player.sy + 100
        
        effect.reloadBarX  = server.player.sx - 35
        effect.reloadBarY  = server.player.sy + 100
        
        effect.reloadX     = server.player.sx
        effect.reloadY     = server.player.sy + 100
        
        if effect.isOn:
            effect.reloadBarX  += effect.reloadBarDX
            effect.reloadBarDX += RB_SPEED_PPS * game_framework.frame_time
            if effect.reloadBarDX >= 90:
                effect.isOn = False
                weapons.pistol_Reload()
        else:
            effect.frame = (effect.frame + RELOAD_FRAMES_PER_ACTION * RELOAD_ACTION_PER_TIME * game_framework.frame_time) % 4
            if int(effect.frame) >= 3:
                game_world.remove_object(effect)
    
    def draw(effect):
        if effect.isOn:
            effect.reloadBaseImage.clip_draw(0, 0, 23, 1, effect.reloadBaseX, effect.reloadBaseY, 115, 5)
            effect.reloadBarImage.clip_draw(0, 0, 2, 3, effect.reloadBarX, effect.reloadBarY, 10, 15)
        else:
            effect.reloadImage.clip_draw(int(effect.frame) * 27, 0, 27, 9, effect.reloadX, effect.reloadY, 135, 45)
        
class BoomEffect:
    image = None
    
    def __init__(effect, bullet):
        if BoomEffect.image == None:
            BoomEffect.image = load_image("resources/images/weapon/longDistanceWeapon/effect/BoomEffect.png")
        
        if bullet.direction == direction['LEFT']:
            effect.x = bullet.x
            effect.y = bullet.y
            effect.direction = 0
            effect.deg = bullet.deg + 90
            
        if bullet.direction == direction['RIGHT']:
            effect.x = bullet.x
            effect.y = bullet.y
            effect.direction = 1
            effect.deg = bullet.deg - 90
            

        effect.frame = 0.0
        effect.isOn = True    
            
    def update(effect):
        if effect.isOn:
            if effect.frame >= 5.0:
                effect.frame = 0.0
                effect.isOn = False
                game_world.remove_object(effect)
            effect.frame = effect.frame = (effect.frame + SE_FRAMES_PER_ACTION * SE_ACTION_PER_TIME * game_framework.frame_time) % 6
    
    def draw(effect):
        if effect.isOn:
            if effect.direction == 0:
                effect.image.clip_composite_draw(int(effect.frame) * 14, 0, 14, 13, radians(effect.deg - 90), 'h', effect.x, effect.y, 70, 65)
            elif effect.direction == 1:
                effect.image.clip_composite_draw(int(effect.frame) * 14, 0, 14, 13, radians(effect.deg - 90), 'n', effect.x, effect.y, 70, 65)
            
class DestroyEffect:
    image = None
    
    def __init__(effect, x, y):
        if DestroyEffect.image == None:
            DestroyEffect.image = load_image("resources/images/Enemy/destroy.png")
        
        effect.x = x
        effect.y = y
        effect.frame = 0.0
        effect.isOn = True    
            
    def update(effect):
        if effect.isOn:
            if effect.frame >= 10.0:
                effect.frame = 0.0
                effect.isOn = False
                game_world.remove_object(effect)
            effect.frame = effect.frame = (effect.frame + DE_FRAMES_PER_ACTION * DE_ACTION_PER_TIME * game_framework.frame_time) % 11
    
    def draw(effect):
        if effect.isOn:
            effect.image.clip_composite_draw(int(effect.frame) * 40, 0, 40, 40, 0, 'n', effect.x, effect.y, 200, 200)
            
class RedWarningOnHit:
    leftImage  = None
    rightImage = None
    
    def __init__(effect):
        if RedWarningOnHit.leftImage == None:
            RedWarningOnHit.leftImage = load_image("resources/images/gameScene/ui/RedWarningOnHitLeft.png")
        if RedWarningOnHit.rightImage == None:
            RedWarningOnHit.rightImage = load_image("resources/images/gameScene/ui/RedWarningOnHitRight.png")
        
        effect.opacifyF = 1.0
        effect.isOn = True    
            
    def update(effect):
        if effect.isOn:
            if effect.opacifyF <= 0.0:
                effect.opacifyF = 0.0
                effect.isOn = False
                game_world.remove_object(effect)
            effect.opacifyF -= 0.05
    
    def draw(effect):
        if effect.isOn:
            effect.leftImage.opacify(effect.opacifyF)
            effect.rightImage.opacify(effect.opacifyF)
            effect.leftImage.draw_to_origin(0, 0, 800, 900)
            effect.rightImage.draw_to_origin(800, 0, 800, 900)
            
class Damage:
    font = None
    
    def __init__(effect, object, power):
        if Damage.font == None:
            Damage.font = load_font("resources/images/Font/DungGeunMo.ttf", 16)
            
        effect.x        = object.x
        effect.y        = object.y
        effect.dx       = 0.5
        effect.dy       = 40
        effect.opacipyF = 1.0
        effect.text     = power
        effect.isOn     = True
        
    def update(effect):
        if effect.opacipyF <= 0:
            effect.isOn = False
            game_world.remove_object(effect)
        if effect.isOn:
            effect.y += (0.98 * 1 * (effect.dy)) / 10
            effect.x += effect.dx
            effect.dy -= 1
            effect.opacipyF -= 0.02
        
    def draw(effect):
        if effect.isOn:
            effect.font.draw(effect.x, effect.y, 35, 60, f'{effect.text}', (255, 255, 255), effect.opacipyF)