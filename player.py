from pico2d import *
import math
import game_framework
import weapons
import player_hand


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
state      = {'IDLE'  : 0,  'RUN' : 1, 'JUMP' : 2, 'DASH' : 3}
direction  = {'RIGHT' : 1, 'LEFT' : 0}

# 무기
weaponSort = {'sword' : 0, 'sickle' : 1, 'pistol' : 2, 'lightbringer' : 3}

mouseX, mouseY = 0, 0
deg = 0
        
class Player:
    idleImage = None
    runImage  = None
    jumpImage = None
    dashImage = None
    afterImage = []
    dustImage = None
    
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
        if len(Player.afterImage) == 0:
            for i in range(9):
                Player.afterImage.append(load_image('resources/images/Effect/Dash/Shadow/base_player_jump_shadow.png'))
        if Player.dustImage == None:
            Player.dustImage = load_image('resources/images/Effect/Dash/DustEffect.png')
        
        #### 위치 관련 변수 ####
        player.x             = 800
        player.y             = 200
        player.afterX        = [0, 0, 0, 0, 0, 0, 0, 0]
        player.afterY        = [0, 0, 0, 0, 0, 0, 0, 0]
        player.afterOpacifyF = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        player.afterIsOn     = [0, 0, 0, 0, 0, 0, 0, 0]
        player.frame         = 0
        player.speedLR       = 0
        player.jumpHeight    = 0
        player.jumpCount     = 0
        player.dx            = 0
        player.dy            = 0
        player.dashCount     = 0
        player.isAttacked    = False
        player.opacifyF      = 1.0
        player.unheatCount   = 0
        
        #### 상태 관련 변수 ####
        player.state      = state['IDLE']
        player.direction  = direction['RIGHT']
        
        player.hand       = player_hand.Hand(player)
        player.weaponSort = weaponSort['sword']
        player.weapon     = weapons.ShortSword()

    #### 바운딩 박스 받기 ####
    def get_bb(player):
        return player.x - 32.5, player.y - 50, player.x + 32.5, player.y + 50
    
    #### 객체별 충돌처리 ####
    def handle_collision(player, other, group):
        #### 바닥 충돌처리 ####
        if group == 'player:ground':
            player.y = other.y + other.groundImage.h * 5 + 50 + 1   ### 땅의 바운딩박스 top + 플레이어 피봇 기준 발위치 + 1 pixel
            if player.state == state['JUMP']:
                player.state = state['IDLE']
            player.jumpHeight = 0
            player.jumpCount = 0
            
        if group == 'player:stepstone' and player.jumpHeight < 0:
            player.y = other.y + other.stepstoneImage.h * 5 / 2 + 50 + 1
            if player.state == state['JUMP']:
                player.state = state['IDLE']
            player.jumpHeight = 0
            player.jumpCount = 0
            
        if group == 'player:monster':
            if player.unheatCount == 0:
                player.isAttacked = True
    
    def update(player):
        # print('player.x : %d' %player.x)
        # print('player.y : %d' %player.y)
        # print('player.frame : %d' %player.frame)
        # print('player.dx : %d' %player.dx)
        # print('player.dy : %d' %player.dy)
        # print('player.speedLR : %d' %player.speedLR)
        # print('player.jumpHeight : %d' %player.jumpHeight)
        # print('player.jumpCount : %d' %player.jumpCount)
        # print('player.dashCount : %d' %player.dashCount)
        # print('player.state : %d' %player.state)
        # print('player.direction : %d' %player.direction)
        global mouseX, mouseY
        
        #### 피격 이미지, 무적 시간 처리 ####
        if player.isAttacked:
            player.opacifyF = 0.5
            player.unheatCount += game_framework.frame_time
            if player.unheatCount >= 1.0:
                player.opacifyF    = 1.0
                player.unheatCount = 0
                player.isAttacked  = False
        
        if player.x > mouseX:
                player.direction = direction['LEFT']
        elif player.x <= mouseX:
                player.direction = direction['RIGHT']
        
        if player.state == state['IDLE']: # idle상태 일 때
            if player.speedLR != 0: # 점프 완료 후 idle 이미지를 띄울지 run 이미지를 띄울지 결정해줌
                player.state = state['RUN']
            player.frame = (player.frame + IDLE_FRAMES_PER_ACTION * IDLE_ACTION_PER_TIME * game_framework.frame_time) % 5

        if player.state == state['RUN']:
            player.frame = (player.frame + RUN_FRAMES_PER_ACTION * RUN_ACTION_PER_TIME * game_framework.frame_time) % 8
            
        player.jumpHeight -= 1 # h 감소
                
        if player.state == state['DASH']:
            player.x += player.dx
            player.y += player.dy
            
            #### 잔상 업데이트 ####
            player.afterX[player.dashCount] = player.x
            player.afterY[player.dashCount] = player.y
            player.afterIsOn[player.dashCount] = 1
            
            player.dashCount += 1
            
            if player.dashCount == 8:
                player.dx = 0
                player.dy = 0
                player.dashCount = 0
                player.state = state['JUMP']
                
        if player.state != state['DASH']:
            player.x += player.speedLR * RUN_SPEED_PPS * game_framework.frame_time
            player.y += 0.98 * 1 * (player.jumpHeight)
                
        
        #### 잔상 업데이트 ####
        for i in range(player.dashCount, 8):
            player.afterOpacifyF[i] -= 0.1
            if player.afterOpacifyF[i] <= 0.0:
                player.afterIsOn[i] = 0
                player.afterX[i] = 0
                player.afterY[i] = 0
                
        
        #### 무기 업데이트 ####
        if player.weaponSort == weaponSort['sword'] or player.weaponSort == weaponSort['pistol']:
            player.hand.update(player)
        player.weapon.update(player)

    def draw(player):
        #### 잔상 이미지 ####
        if player.direction == direction['LEFT']:
                for i in range(player.dashCount, 8):
                    if player.afterIsOn[i]:
                        player.afterImage[i].clip_composite_draw(0, 0, 17, 20, 0, 'h', \
                            player.afterX[i], player.afterY[i], 85, 100)
                        player.afterImage[i].opacify(player.afterOpacifyF[i])
                    
        if player.direction == direction['RIGHT']:
                for i in range(player.dashCount, 8):
                    if player.afterIsOn[i]:
                        player.afterImage[i].clip_composite_draw(0, 0, 17, 20, 0, 'h', \
                            player.afterX[i], player.afterY[i], 85, 100)
                        player.afterImage[i].opacify(player.afterOpacifyF[i])
                        
        #### 한손검은 휘두를 때 마다 앞에 그려줄지 뒤에 그려줄지 정해줌 ####
        if (player.weaponSort == weaponSort['sword'] and player.weapon.backrender == True) or player.weaponSort == weaponSort['pistol']:
            player.hand.image.opacify(player.opacifyF)
            player.hand.draw()
            player.weapon.draw(player)
        
        #### IDLE ####
        if player.state == state['IDLE']:
            player.idleImage.opacify(player.opacifyF)
            if player.direction == direction['LEFT']:
                player.idleImage.clip_composite_draw(int(player.frame) * 15, 0, 15, 20, 0, 'h', player.x, player.y, 75, 100)
            if player.direction == direction['RIGHT']:
                player.idleImage.clip_composite_draw(int(player.frame) * 15, 0, 15, 20, 0, 'n', player.x, player.y, 75, 100)
        
        #### RUN ####    
        if player.state == state['RUN']:
            player.runImage.opacify(player.opacifyF)
            if player.direction == direction['LEFT']:
                player.runImage.clip_composite_draw (int(player.frame) * 17, 0, 17, 20, 0, 'h', player.x, player.y, 85, 100)
                player.dustImage.clip_composite_draw(int(player.frame) * 14, 0, 14, 13, 0, 'h', player.x + 40, player.y - 25, 70, 65)
            if player.direction == direction['RIGHT']:
                player.runImage.clip_composite_draw (int(player.frame) * 17, 0, 17, 20, 0, 'n', player.x, player.y, 85, 100)
                player.dustImage.clip_composite_draw(int(player.frame) * 14, 0, 14, 13, 0, 'n', player.x - 40, player.y - 25, 70, 65)
                
        #### JUMP ####
        if player.state == state['JUMP']:
            player.jumpImage.opacify(player.opacifyF)
            if player.direction == direction['LEFT']:
                player.jumpImage.clip_composite_draw(0, 0, 17, 20, 0, 'h', player.x, player.y, 85, 100)
            if player.direction == direction['RIGHT']:
                player.jumpImage.clip_composite_draw(0, 0, 17, 20, 0, 'n', player.x, player.y, 85, 100)
        
        #### DASH ####
        if player.state == state['DASH']:
            player.dashImage.opacify(player.opacifyF)
            if player.direction == direction['LEFT']:
                player.dashImage.clip_composite_draw(0, 0, 17, 20, 0, 'h', player.x, player.y, 85, 100)
            if player.direction == direction['RIGHT']:
                player.dashImage.clip_composite_draw(0, 0, 17, 20, 0, 'n', player.x, player.y, 85, 100)
        
        #### 무기 그리기 ####
        if player.weaponSort == weaponSort['sword'] and player.weapon.backrender == False:
            player.hand.image.opacify(player.opacifyF)
            player.hand.draw()
            player.weapon.draw(player)
        elif player.weaponSort == weaponSort['sickle'] or player.weaponSort == weaponSort['lightbringer']:
            player.weapon.draw(player)
            
        draw_rectangle(*player.get_bb())
            
        
                
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
                player.weaponSort = weaponSort['pistol']
                player.weapon = weapons.Pistol()
            if event.key == SDLK_4:
                player.weaponSort = weaponSort['lightbringer']
                player.weapon = weapons.LightBringer()
                
            ##### W 눌림 #####
            if event.key == SDLK_w:
                if player.jumpCount != 2:
                    if player.state != state['DASH']:
                        player.state = state['JUMP']
                        player.jumpHeight = 25
                        player.frame = 0
                        player.jumpCount += 1
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
                pass
            ##### D 눌림 #####
            if event.key == SDLK_d:
                player.speedLR  += 1
                if player.state != state['JUMP'] and player.state != state['DASH']:
                    if player.state == state['RUN']:
                        player.state = state['IDLE']
                        return
                    player.state = state['RUN'] # 상태 변경
                    player.frame = 0 # 프레임 초기화
            
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
                pass
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
            if event.button == SDL_BUTTON_RIGHT:
                if player.state != state['DASH']:
                    player.state = state['DASH']
                    player.dashCount = 0
                    player.dx, player.dy = ((mouseX - player.x) / math.sqrt((mouseX - player.x)**2 + (900 - mouseY - player.y) ** 2) * 45,
                           (900 - mouseY - player.y) / math.sqrt((mouseX - player.x)**2 + (900 - mouseY - player.y)**2) * 45)
                    for i in range(8): # 잔상 초기화
                        player.afterOpacifyF[i] = 1.0
                        
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
            
