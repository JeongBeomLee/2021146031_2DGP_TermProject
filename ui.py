from pico2d import*
import game_framework
import weapons

PLB_TIME_PER_ACTION    = 0.5
PLB_ACTION_PER_TIME    = 1.0 / PLB_TIME_PER_ACTION
PLB_FRAMES_PER_ACTION  = 7

weaponSort = {'sword' : 0, 'sickle' : 1, 'pistol' : 2, 'lightbringer' : 3}

class EnemyLifeBar:
    image = None
    backImage = None
    
    def __init__(ui, object):
        if EnemyLifeBar.image == None:
            EnemyLifeBar.image = load_image("resources/images/gameScene/ui/LifeBar.png")
        if EnemyLifeBar.backImage == None:
            EnemyLifeBar.backImage = load_image("resources/images/gameScene/ui/LifeBarBack.png")
            
        ui.x    = 0
        ui.y    = 0
        ui.hp   = object.hp
        ui.isOn = True    
            
    def update(ui, object):
        ui.x  = object.sx - 200
        ui.y  = object.sy - (object.h // 2) - 50 - 150
        ui.hp = object.hp
    
    def draw(ui, object):
        ui.backImage.clip_draw_to_origin(0, 0, 1, 10, ui.x - 5, ui.y - 5,  350, 20)
        ui.image.clip_draw_to_origin(0, 0, 1, 10, ui.x, ui.y,  ui.hp / object.hpMax * 340, 10)
        
class PlayerLifeBar:
    image         = None
    waveImage     = None
    baseImage     = None
    backImage     = None
    portraitImage = None
    font          = None
    
    def __init__(ui, object):
        if PlayerLifeBar.image == None:
            PlayerLifeBar.image = load_image("resources/images/gameScene/ui/LifeBar.png")
        if PlayerLifeBar.waveImage == None:
            PlayerLifeBar.waveImage = load_image("resources/images/gameScene/ui/LifeWave.png")
        if PlayerLifeBar.baseImage == None:
            PlayerLifeBar.baseImage = load_image("resources/images/gameScene/ui/PlayerLifeBase 1.png")
        if PlayerLifeBar.backImage == None:
            PlayerLifeBar.backImage = load_image("resources/images/gameScene/ui/PlayerLifeBack.png")
        if PlayerLifeBar.portraitImage == None:
            PlayerLifeBar.portraitImage = load_image('resources/images/Characters/Player/Costume/common/player_idle.png')
        if PlayerLifeBar.font == None:
           PlayerLifeBar.font = load_font("resources/images/Font/DungGeunMo.ttf", 16)
        
        ui.canvas_width  = get_canvas_width()
        ui.canvas_height = get_canvas_height()
        
        ui.frame = 0
        ui.x     = 5
        ui.y     = ui.canvas_height - (ui.baseImage.h * 3) - 5
        ui.hp    = object.hp
        
    def update(ui, object):
        ui.frame = (ui.frame + PLB_FRAMES_PER_ACTION * PLB_ACTION_PER_TIME * game_framework.frame_time) % 7
        ui.hp    = object.hp
    
    def draw(ui, object):
        ui.backImage.clip_draw_to_origin(0, 0, 74, 16, ui.x, ui.y,  ui.backImage.w * 3, ui.backImage.h * 3)
        ui.image.clip_draw_to_origin(0, 0, 1, 10, ui.x + 66, ui.y,  (ui.hp / object.hpMax * 100) * 1.5, 48)
        if ui.hp <= 90 and ui.hp >= 0:
            ui.waveImage.clip_draw_to_origin(int(ui.frame) * 4, 0, 4, 10, ui.x + (ui.hp / object.hpMax * 100) * 1.5 + 66, ui.y,  12, 48)
        ui.portraitImage.clip_draw_to_origin(0, 0, 15, 21, ui.x + 21, ui.y,  30, 42)
        ui.baseImage.clip_draw_to_origin(0, 0, 74, 16, ui.x, ui.y, ui.baseImage.w * 3, ui.baseImage.h * 3)
        ui.font.draw(ui.x + 40, ui.y + 5, 130, 40, f'{ui.hp} / {object.hpMax}', (0, 0, 0))
        # ui.font.draw(ui.x + 105, ui.y + 25, 90, 30, f'{ui.hp} / {object.hpMax}', (255, 255, 255))
        
        
class PlayerDashBar:
    leftEndImage  = None
    baseImage     = None
    rightEndImage = None
    countImage    = None
    
    def __init__(ui, object):
        if PlayerDashBar.leftEndImage == None:
            PlayerDashBar.leftEndImage = load_image("resources/images/gameScene/ui/DashBaseLeftEnd.png")
        if PlayerDashBar.baseImage == None:
            PlayerDashBar.baseImage = load_image("resources/images/gameScene/ui/DashCountBase.png")
        if PlayerDashBar.rightEndImage == None:
            PlayerDashBar.rightEndImage = load_image("resources/images/gameScene/ui/DashBaseRightEnd.png")
        if PlayerDashBar.countImage == None:
            PlayerDashBar.countImage = load_image("resources/images/gameScene/ui/DashCount.png")
        
        ui.canvas_width  = get_canvas_width()
        ui.canvas_height = get_canvas_height()
        
        ui.x     = 5
        ui.y     = ui.canvas_height - (ui.baseImage.h * 3) - 50
        ui.count = object.dashCount
        
    def update(ui, object):
        ui.count = object.dashCount

    def draw(ui):
        ui.leftEndImage.clip_draw_to_origin(0, 0, 2, 8, ui.x, ui.y, 6, 24)
        ui.baseImage.clip_draw_to_origin(0, 0, 18, 8, ui.x + 6, ui.y, 54, 24)
        ui.rightEndImage.clip_draw_to_origin(0, 0, 2, 8, ui.x + 60, ui.y, 6, 24)
        
        for i in range(0, ui.count):
            ui.countImage.clip_draw_to_origin(0, 0, 9, 4, ui.x + 6 + (i * 27), ui.y + 6, 27, 12)
            
class EquippedWeaponBar:
    shortSwordImage      = None
    pickaxeRedImage      = None
    lightBringerImage    = None
    pistolImage          = None
    font                 = None
    
    def __init__(ui, object):
        if EquippedWeaponBar.shortSwordImage == None:
           EquippedWeaponBar.shortSwordImage = load_image("resources/images/gameScene/ui/EquippedWeaponBase1.png")
        if EquippedWeaponBar.pickaxeRedImage == None:
           EquippedWeaponBar.pickaxeRedImage = load_image("resources/images/gameScene/ui/EquippedWeaponBase2.png")
        if EquippedWeaponBar.lightBringerImage == None:
           EquippedWeaponBar.lightBringerImage = load_image("resources/images/gameScene/ui/EquippedWeaponBase3.png")
        if EquippedWeaponBar.pistolImage == None:
           EquippedWeaponBar.pistolImage = load_image("resources/images/gameScene/ui/EquippedWeaponBase4.png")
        if EquippedWeaponBar.font == None:
           EquippedWeaponBar.font = load_font("resources/images/Font/AaCassiopeia.ttf", 16)
        
        ui.x = 1530
        ui.y = 100
        
        if object.weaponSort == weaponSort['sword']:
            ui.sort = 1
        elif object.weaponSort == weaponSort['sickle']:
            ui.sort = 2
        elif object.weaponSort == weaponSort["lightbringer"]:
            ui.sort = 3
        elif object.weaponSort == weaponSort["pistol"]:
            ui.sort = 4
        
    def update(ui, object):
        if object.weaponSort == weaponSort['sword']:
            ui.sort = 1
        elif object.weaponSort == weaponSort["sickle"]:
            ui.sort = 2
        elif object.weaponSort == weaponSort["lightbringer"]:
            ui.sort = 3
        elif object.weaponSort == weaponSort["pistol"]:
            ui.sort = 4
        

    def draw(ui):
        if ui.sort == 1:
            ui.pistolImage.clip_draw(0, 0, 34, 24, ui.x, ui.y, 136, 96)
            ui.lightBringerImage.clip_draw(0, 0, 34, 24, ui.x - 10, ui.y - 10, 136, 96)
            ui.pickaxeRedImage.clip_draw(0, 0, 34, 24, ui.x - 20, ui.y - 20, 136, 96)
            ui.shortSwordImage.clip_draw(0, 0, 34, 24, ui.x - 30, ui.y - 30, 136, 96)
        if ui.sort == 2:
            ui.shortSwordImage.clip_draw(0, 0, 34, 24, ui.x, ui.y, 136, 96)
            ui.pistolImage.clip_draw(0, 0, 34, 24, ui.x - 10, ui.y - 10, 136, 96)
            ui.lightBringerImage.clip_draw(0, 0, 34, 24, ui.x - 20, ui.y - 20, 136, 96)
            ui.pickaxeRedImage.clip_draw(0, 0, 34, 24, ui.x - 30, ui.y - 30, 136, 96)
        if ui.sort == 3:
            ui.pickaxeRedImage.clip_draw(0, 0, 34, 24, ui.x, ui.y, 136, 96)
            ui.shortSwordImage.clip_draw(0, 0, 34, 24, ui.x - 10, ui.y - 10, 136, 96)
            ui.pistolImage.clip_draw(0, 0, 34, 24, ui.x - 20, ui.y - 20, 136, 96)
            ui.lightBringerImage.clip_draw(0, 0, 34, 24, ui.x - 30, ui.y - 30, 136, 96)
        if ui.sort == 4:
            ui.lightBringerImage.clip_draw(0, 0, 34, 24, ui.x, ui.y, 136, 96)
            ui.pickaxeRedImage.clip_draw(0, 0, 34, 24, ui.x - 10, ui.y - 10, 136, 96)
            ui.shortSwordImage.clip_draw(0, 0, 34, 24, ui.x - 20, ui.y - 20, 136, 96)
            ui.pistolImage.clip_draw(0, 0, 34, 24, ui.x - 30, ui.y - 30, 136, 96)
            ui.font.draw(ui.x - 102, ui.y - 62, 60, 20, f'{weapons.Pistol.bulletCount} / 10', (255, 255, 255))
            

                