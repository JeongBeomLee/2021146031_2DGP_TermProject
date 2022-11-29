from pico2d import *
import game_framework
import game_world

import math
import random

import test_state

ghost_state = {'attack' : 0}
ghost_direction = {'left' : 0, 'right' : 1}

BSS_IDLE_TIME_PER_ACTION    = 0.5
BSS_IDLE_ACTION_PER_TIME    = 1.0 / BSS_IDLE_TIME_PER_ACTION
BSS_IDLE_FRAMES_PER_ACTION  = 5

class Big_Skel_Sword:
    idleImage       = None
    idleShotImage   = None
    runImage        = None
    runShotImage    = None
    attackImage     = None
    attackShotImage = None
    
    def __init__(monster):
        if Big_Skel_Sword.idleImage == None:
            Big_Skel_Sword.idleImage = load_image("resources/images/Enemy/Skel/Big_Normal/idle.png")
        if Big_Skel_Sword.idleShotImage == None:
            Big_Skel_Sword.idleShotImage = load_image("resources/images/Enemy/Skel/Big_Normal/idle_shot.png")
            
        if Big_Skel_Sword.runImage == None:
            Big_Skel_Sword.runImage = load_image("resources/images/Enemy/Skel/Big_Normal/move.png")
        if Big_Skel_Sword.runShotImage == None:
            Big_Skel_Sword.runShotImage = load_image("resources/images/Enemy/Skel/Big_Normal/move_shot.png")
            
        if Big_Skel_Sword.attackImage == None:
            Big_Skel_Sword.attackImage = load_image("resources/images/Enemy/Skel/Big_Normal/attack.png")
        if Big_Skel_Sword.attackShotImage == None:
            Big_Skel_Sword.attackShotImage = load_image("resources/images/Enemy/Skel/Big_Normal/attack_shot.png")
            
        monster.x           = 800
        monster.y           = 200
        monster.frame       = 0
        monster.isAttack    = False
        monster.isAttacked  = False
        monster.unheatCount = 0
        
    def get_bb(monster):
        return monster.x - 16.5 * 5, monster.y - 75, monster.x + 16.5 * 5, monster.y + 75
    
    #### 객체별 충돌처리 ####
    def handle_collision(monster, other, group):
        #### 바닥 충돌처리 ####
        if group == 'monster:ground':
            monster.y = other.y + other.groundImage.h * 5 + 75 + 1   ### 땅의 바운딩박스 top + 플레이어 피봇 기준 발위치 + 1 pixel
            
        if group == 'monster:stepstone' and monster.jumpHeight < 0:
            monster.y = other.y + other.stepstoneImage.h * 5 / 2 + 75 + 1
        
        if group == 'Bullet:monster' or group == 'Arrow:monster':
            if monster.unheatCount == 0:
                monster.isAttacked = True
        elif group == 'pickaxeRedEffect:monster' and test_state.player.weapon.isAttack:
            if monster.unheatCount == 0:
                monster.isAttacked = True
        elif group == 'shortSwordEffect:monster' and test_state.player.weapon.isAttack:
            if monster.unheatCount == 0:
                monster.isAttacked = True
            
    
    def update(monster):
        if monster.isAttacked:
            monster.opacifyF = 0.5
            monster.unheatCount += game_framework.frame_time
            if monster.unheatCount >= 0.1:
                monster.opacifyF    = 1.0
                monster.unheatCount = 0
                monster.isAttacked  = False
        
        monster.frame = (monster.frame + BSS_IDLE_FRAMES_PER_ACTION * BSS_IDLE_ACTION_PER_TIME * game_framework.frame_time) % 5
        # monster.y -= 50

    def draw(monster):
        if monster.isAttacked:
            monster.idleShotImage.clip_composite_draw(int(monster.frame) * 33, 0, 33, 30, 0, 'h', monster.x, monster.y, 33 * 5, 30 * 5)
        else:
            monster.idleImage.clip_composite_draw(int(monster.frame) * 33, 0, 33, 30, 0, 'h', monster.x, monster.y, 33 * 5, 30 * 5)
        draw_rectangle(*monster.get_bb())
