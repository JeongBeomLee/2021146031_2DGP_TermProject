from pico2d import *
import math
import game_framework
import game_world
import weapons
import player_hand
import player_feet
import ui
import effects
import server

# Player Run Speed
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH  = 30.0
RUN_SPEED_MPM   = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS   = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS   = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Player Action Speed
RUN_TIME_PER_ACTION     = 0.5
RUN_ACTION_PER_TIME     = 1.0 / RUN_TIME_PER_ACTION
RUN_FRAMES_PER_ACTION   = 8

IDLE_TIME_PER_ACTION    = 0.5
IDLE_ACTION_PER_TIME    = 1.0 / IDLE_TIME_PER_ACTION
IDLE_FRAMES_PER_ACTION  = 5

# 캐릭터 상태, 방향
state      = {'IDLE'  : 0,  'RUN' : 1, 'JUMP' : 2, 'DASH' : 3, 'DIE' : 4}
direction  = {'RIGHT' : 1, 'LEFT' : 0}

# 무기
weaponSort = {'sword' : 0, 'sickle' : 1, 'pistol' : 2, 'lightbringer' : 3}

# 맵
mapSort = {'VILLIAGE' : 0, 'MOVE' : 1, 'JUMP' : 2, 'DASH' : 3, 'BATTLE' : 4, 'BOSS' : 5}

mouseX, mouseY = 0, 0
deg = 0
        
class Player:
    idleImage  = None
    runImage   = None
    jumpImage  = None
    dashImage  = None
    dustImage  = None
    dieImage   = None
    
    def __init__(player):
        #### 이미지 초기화 ####
        if Player.idleImage == None:
            Player.idleImage = load_image('resources/images/Characters/Player/Costume/common/player_idle.png')
        if Player.runImage  == None:
            Player.runImage  = load_image('resources/images/Characters/Player/Costume/common/player_run.png')
        if Player.jumpImage == None:
            Player.jumpImage = load_image('resources/images/Characters/Player/Costume/common/player_jump.png')
        if Player.dashImage == None:
            Player.dashImage = load_image('resources/images/Characters/Player/Costume/common/player_jump.png')
        if Player.dieImage == None:
            Player.dieImage = load_image('resources/images/Characters/Player/Costume/common/player_die.png')
        if Player.dustImage == None:
            Player.dustImage = load_image('resources/images/Effect/Dash/DustEffect.png')
        
        #### 위치 관련 변수 ####
        player.x             = 500
        player.y             = 200
        player.sx            = 500 - server.map.window_left
        player.sy            = 200 - server.map.window_bottom
        player.frame         = 0
        player.speedLR       = 0
        player.jumpHeight    = 0
        player.jumpCount     = 0
        player.dx            = 0
        player.dy            = 0
        player.dashTimer     = 0
        player.dashCount     = 2
        player.dashPlusTimer = 0
        player.isAttacked    = False
        player.opacifyF      = 1.0
        player.unheatTimer   = 0
        player.isOnStepstone = False
        player.isOnGround    = True
        player.sDown         = False
        player.canMoveX       = True
        player.canMoveY       = True
        player.isOn = True
        
        player.hpMax = 100
        player.hp    = 100
        player.power = 5
        
        #### 상태 관련 변수 ####
        player.state      = state['IDLE']
        player.direction  = direction['RIGHT']
        
        player.hand       = player_hand.Hand(player)
        player.weaponSort = weaponSort['sword']
        player.weapon     = weapons.ShortSword()
        
        feet = player_feet.Feet(player.x, player.y)
        game_world.add_object(feet, 1)
        game_world.add_collision_pairs(feet, server.stepstone, 'feet:stepstone')
        #### UI ####
        player.lifeBar           = ui.PlayerLifeBar(player)
        player.dashBar           = ui.PlayerDashBar(player)
        player.equippedWeaponBar = ui.EquippedWeaponBar(player)
        

    #### 바운딩 박스 받기 ####
    def get_bb(player):
        return player.sx - 32.5, player.sy - 50, player.sx + 32.5, player.sy + 50
    
    #### 객체별 충돌처리 ####
    def handle_collision(player, other, group):
        if group == 'player:ground':
            server.player.y = other.sy + other.h + 50 + 1   ### 땅의 바운딩박스 top + 플레이어 피봇 기준 발위치 + 1 pixel
            if server.player.state == state['JUMP']:
                server.player.state = state['IDLE']
            server.player.jumpHeight    = 0
            server.player.jumpCount     = 0
            server.player.isOnGround    = True
            server.player.isOnStepstone = False
            
        
        if group == 'player:ball':
            if player.unheatTimer == 0:
                player.isAttacked = True
                player.hp -= other.power
                warningEffect = effects.RedWarningOnHit()
                game_world.add_object(warningEffect, 1)
    
    def update(player):
        global mouseX, mouseY
        player.sx, player.sy = player.x - server.map.window_left, player.y - server.map.window_bottom
        
        if not player.isOnGround and not player.isOnStepstone:
            player.jumpHeight -= 1 # h 감소
        
        if player.hp <= 0:
            if player.state != state['DIE']:
                player.state = state['DIE']
                player.canMoveX = False;
                player.canMoveY = False;
                dieEffect = effects.DestroyEffect(player.sx, player.sy)
                game_world.add_object(dieEffect, 1)
        
        #### 피격 이미지, 무적 시간 처리 ####
        if player.isAttacked:
            player.opacifyF = 0.5
            player.unheatTimer += game_framework.frame_time
            if player.unheatTimer >= 1.0:
                player.opacifyF    = 1.0
                player.unheatTimer = 0
                player.isAttacked  = False
        
        if player.sx > mouseX:
                player.direction = direction['LEFT']
        elif player.sx <= mouseX:
                player.direction = direction['RIGHT']
        
        if player.state == state['IDLE']: # idle상태 일 때
            if player.speedLR != 0: # 점프 완료 후 idle 이미지를 띄울지 run 이미지를 띄울지 결정해줌
                player.state = state['RUN']
            player.frame = (player.frame + IDLE_FRAMES_PER_ACTION * IDLE_ACTION_PER_TIME * game_framework.frame_time) % 5

        if player.state == state['RUN']:
            player.frame = (player.frame + RUN_FRAMES_PER_ACTION * RUN_ACTION_PER_TIME * game_framework.frame_time) % 8
            player.isOnGround    = False
            player.isOnStepstone = False
        
               
        if player.state == state['DASH']:
            if player.canMoveX:
                player.x += player.dx
                player.y += player.dy
                
                player.dashTimer += game_framework.frame_time
                
                if player.dashTimer >= 0.1:
                    player.dx = 0
                    player.dy = 0
                    player.dashTimer = 0
                    player.state = state['JUMP']
        
        if player.dashCount < 2:
            player.dashPlusTimer += game_framework.frame_time
            if player.dashPlusTimer >= 1.5:
                player.dashCount += 1
                player.dashPlusTimer = 0
                
        
        if player.state != state['DASH']:
            if player.canMoveX:
                player.x += player.speedLR * RUN_SPEED_PPS * game_framework.frame_time
            if player.canMoveY:
                player.y += 0.98 * 1 * (player.jumpHeight)
            
            if server.map.sort == mapSort['VILLIAGE']:
                player.x = clamp(0, player.x, 1600 * 4)
                player.y = clamp(0, player.y, 900 * 2)
            if server.map.sort == mapSort['MOVE']:
                player.x = clamp(275, player.x, 1400)
                player.y = clamp(0, player.y, 625)
            if server.map.sort == mapSort['BOSS']:
                player.x = clamp(200, player.x, 1400)
                player.y = clamp(0, player.y, 800)
                
        #### 무기 업데이트 ####
        if player.weaponSort == weaponSort['sword'] or player.weaponSort == weaponSort['pistol']:
            player.hand.update(player)
        player.weapon.update(player)
        
        #### UI 업데이트 ####
        player.lifeBar.update(player)
        player.dashBar.update(player)
        player.equippedWeaponBar.update(player)

    def draw(player):
        if player.isOn:
            #### 한손검은 휘두를 때 마다 앞에 그려줄지 뒤에 그려줄지 정해줌 ####
            if (player.weaponSort == weaponSort['sword'] and player.weapon.backrender == True) or player.weaponSort == weaponSort['pistol']:
                player.hand.image.opacify(player.opacifyF)
                player.hand.draw()
                player.weapon.draw(player)
            
            #### IDLE ####
            if player.state == state['IDLE']:
                player.idleImage.opacify(player.opacifyF)
                if player.direction == direction['LEFT']:
                    player.idleImage.clip_composite_draw(int(player.frame) * 15, 0, 15, 20, 0, 'h', player.sx, player.sy, 75, 100)
                if player.direction == direction['RIGHT']:
                    player.idleImage.clip_composite_draw(int(player.frame) * 15, 0, 15, 20, 0, 'n', player.sx, player.sy, 75, 100)
            
            #### RUN ####    
            if player.state == state['RUN']:
                player.runImage.opacify(player.opacifyF)
                if player.direction == direction['LEFT']:
                    player.runImage.clip_composite_draw (int(player.frame) * 17, 0, 17, 20, 0, 'h', player.sx, player.sy, 85, 100)
                    player.dustImage.clip_composite_draw(int(player.frame) * 14, 0, 14, 13, 0, 'h', player.sx + 40, player.sy - 25, 70, 65)
                if player.direction == direction['RIGHT']:
                    player.runImage.clip_composite_draw (int(player.frame) * 17, 0, 17, 20, 0, 'n', player.sx, player.sy, 85, 100)
                    player.dustImage.clip_composite_draw(int(player.frame) * 14, 0, 14, 13, 0, 'n', player.sx - 40, player.sy - 25, 70, 65)
                    
            #### JUMP ####
            if player.state == state['JUMP']:
                player.jumpImage.opacify(player.opacifyF)
                if player.direction == direction['LEFT']:
                    player.jumpImage.clip_composite_draw(0, 0, 17, 20, 0, 'h', player.sx, player.sy, 85, 100)
                if player.direction == direction['RIGHT']:
                    player.jumpImage.clip_composite_draw(0, 0, 17, 20, 0, 'n', player.sx, player.sy, 85, 100)
            
            #### DASH ####
            if player.state == state['DASH']:
                player.dashImage.opacify(player.opacifyF)
                if player.direction == direction['LEFT']:
                    player.dashImage.clip_composite_draw(0, 0, 17, 20, 0, 'h', player.sx, player.sy, 85, 100)
                if player.direction == direction['RIGHT']:
                    player.dashImage.clip_composite_draw(0, 0, 17, 20, 0, 'n', player.sx, player.sy, 85, 100)
            
            #### DIE ####
            if player.state == state['DIE']:
                player.dieImage.opacify(player.opacifyF)
                if player.direction == direction['LEFT']:
                    player.dieImage.clip_composite_draw(0, 0, 23, 14, 0, 'h', player.sx, player.sy, 115, 70)
                if player.direction == direction['RIGHT']:
                    player.dieImage.clip_composite_draw(0, 0, 23, 14, 0, 'n', player.sx, player.sy, 115, 70)

            
            #### 무기 그리기 ####
            if player.weaponSort == weaponSort['sword'] and player.weapon.backrender == False:
                player.hand.image.opacify(player.opacifyF)
                player.hand.draw()
                player.weapon.draw(player)
            elif player.weaponSort == weaponSort['sickle'] or player.weaponSort == weaponSort['lightbringer']:
                player.weapon.draw(player)
            
            draw_rectangle(*player.get_bb())
            
        #### UI ####
        player.lifeBar.draw(player)
        player.dashBar.draw()
        player.equippedWeaponBar.draw()
        
                
    def handle_event(player, event):
        global mouseX, mouseY
        if event.type == SDL_KEYDOWN:
            #### 무기 바꿔주기 ####
            if event.key == SDLK_1:
                player.weaponSort = weaponSort['sword']
                player.weapon = weapons.ShortSword()
            if event.key == SDLK_2:
                player.weaponSort = weaponSort['sickle']
                player.weapon = weapons.PickaxeRed()
            if event.key == SDLK_3:
                player.weaponSort = weaponSort['lightbringer']
                player.weapon = weapons.LightBringer()
            if event.key == SDLK_4:
                player.weaponSort = weaponSort['pistol']
                player.weapon = weapons.Pistol()
                
            ##### W 눌림 #####
            if event.key == SDLK_w:
                if player.jumpCount != 2:
                    if player.state != state['DASH']:
                        player.state = state['JUMP']
                        player.jumpHeight = 25
                        player.frame = 0
                        player.jumpCount += 1
                        player.isOnGround    = False
                        player.isOnStepstone = False
            ##### A 눌림 #####  
            if event.key == SDLK_a:
                player.speedLR  -= 1
                if player.state != state['JUMP'] and player.state != state['DASH']:
                    if player.state == state['RUN']:
                        player.state = state['IDLE']
                        return
                    player.state = state['RUN'] # 상태 변경
                    player.frame = 0 # 프레임 초기화
            ##### S 눌림 #####    
            if event.key == SDLK_s:
                player.sDown = True
            ##### D 눌림 #####
            if event.key == SDLK_d:
                player.speedLR += 1
                if player.state != state['JUMP'] and player.state != state['DASH']:
                    if player.state == state['RUN']:
                        player.state = state['IDLE']
                        return
                    player.state = state['RUN'] # 상태 변경
                    player.frame = 0 # 프레임 초기화
            if event.key == SDLK_r:
                if weapons.Pistol.isReload == False and weapons.Pistol.bulletCount != 10:
                    weapons.Pistol.isReload = True
                    reloadEffect = effects.ReloadEffect(player)
                    game_world.add_object(reloadEffect, 0)
            if event.key == SDLK_SPACE:
                if player.sDown and player.isOnStepstone:
                    player.state = state['JUMP']
                    player.y -= 30
                    player.isOnGround    = False
                    player.isOnStepstone = False
                else:
                    if player.jumpCount != 2:
                        if player.state != state['DASH']:
                            player.state = state['JUMP']
                            player.jumpHeight = 25
                            player.frame = 0
                            player.jumpCount += 1
                            player.isOnGround    = False
                            player.isOnStepstone = False
            
        elif event.type == SDL_KEYUP:
            ##### W 올림 #####
            if event.key == SDLK_w:
                pass
            ##### A 올림 #####
            if event.key == SDLK_a:
                player.speedLR += 1
                if player.state != state['JUMP'] and player.state != state['DASH']:
                    player.state = state['IDLE']
                    player.frame = 0 
            ##### S 올림 #####
            if event.key == SDLK_s:
                player.sDown = False
            ##### D 올림 #####
            if event.key == SDLK_d:
                player.speedLR -= 1
                if player.state != state['JUMP'] and player.state != state['DASH']:
                    player.state = state['IDLE']
                    player.frame = 0
            
        
        elif event.type == SDL_MOUSEMOTION:
            mouseX = event.x
            mouseY = event.y
            weapons.get_Mouse(event.x, event.y)
            
        #### 캐릭터 공격 ####
        #### 마우스 왼쪽 눌림 ####
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                if player.weaponSort == weaponSort['sword']: 
                    player.weapon.isAttack = True
                    player.weapon.backrender = not player.weapon.backrender
                    player.weapon.append_Effect(player)
                elif player.weaponSort == weaponSort['sickle']: # 곡괭이
                    player.weapon.isAttack = True 
                    player.weapon.append_Effect(player)
                elif player.weaponSort == weaponSort['lightbringer']: # 활
                    player.weapon.isAttack = True
                elif player.weaponSort == weaponSort['pistol']:
                    if not player.weapon.isReload:
                        player.weapon.isAttack = True
                        player.weapon.append_Effect(player)
                        dx, dy = ((mouseX - player.weapon.x) / math.sqrt((mouseX - player.weapon.x)**2 + (900 - mouseY - player.weapon.y) ** 2) * 45,
                            (900 - mouseY - player.weapon.y) / math.sqrt((mouseX - player.weapon.x)**2 + (900 - mouseY - player.weapon.y)**2) * 45)
                        player.weapon.shoot_Bullet(dx, dy, player)
                    
            #### 캐릭터 대쉬 ####
            #### 마우스 오른쪽 눌림 ####
            if event.button == SDL_BUTTON_RIGHT:
                if player.state != state['DASH'] and player.dashCount != 0:
                    player.state = state['DASH']
                    player.dashTimer = 0
                    player.dashCount -= 1
                    player.dx, player.dy = ((mouseX - player.sx) / math.sqrt((mouseX - player.sx)**2 + (900 - mouseY - player.sy) ** 2) * 45,
                           (900 - mouseY - player.sy) / math.sqrt((mouseX - player.sx)**2 + (900 - mouseY - player.sy)**2) * 45)
                    player.isOnGround    = False
                    player.isOnStepstone = False
                        
        #### 마우스 왼쪽 버튼 올림 ####
        elif event.type == SDL_MOUSEBUTTONUP:
            if event.button == SDL_BUTTON_LEFT:
                if player.weaponSort == weaponSort['lightbringer']: # 활
                    dx, dy = ((mouseX - player.weapon.x) / math.sqrt((mouseX - player.weapon.x)**2 + (900 - mouseY - player.weapon.y) ** 2) * 45,
                           (900 - mouseY - player.weapon.y) / math.sqrt((mouseX - player.weapon.x)**2 + (900 - mouseY - player.weapon.y)**2) * 45)
                    if player.weapon.frame > 2:
                        player.weapon.shoot_Arrow(dx, dy, player)
                    player.weapon.isAttack = False
                    player.weapon.frame = 0
                if player.weaponSort == weaponSort['pistol']:
                    player.weapon.isAttack = False
            
