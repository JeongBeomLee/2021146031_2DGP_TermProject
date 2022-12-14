from pico2d import *
import game_framework
import game_world

import math
import random

import server
import ui
import effects

mapSort = {'VILLIAGE' : 0, 'MOVE' : 1, 'JUMP' : 2, 'DASH' : 3, 'BATTLE' : 4, 'BOSS' : 5}

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
        monster.sx          = 800
        monster.sy          = 200
        monster.w           = Big_Skel_Sword.idleImage.w * 5
        monster.h           = Big_Skel_Sword.idleImage.h * 5
        monster.frame       = 0
        monster.isAttack    = False
        monster.isAttacked  = False
        monster.unheatCount = 0
        
        monster.hpMax = 500
        monster.hp = 500
        monster.power = 10
        monster.lifeBar = ui.EnemyLifeBar(monster)
        
    def get_bb(monster):
        return monster.sx - 16.5 * 5, monster.sy - 75, monster.sx + 16.5 * 5, monster.sy + 75
    
    #### ????????? ???????????? ####
    def handle_collision(monster, other, group):
        #### ?????? ???????????? ####
        if group == 'monster:ground':
            monster.y = other.y + other.groundImage.h * 5 + 75 + 1   ### ?????? ??????????????? top + ???????????? ?????? ?????? ????????? + 1 pixel
            
        if group == 'monster:stepstone' and monster.jumpHeight < 0:
            monster.y = other.y + other.stepstoneImage.h * 5 / 2 + 75 + 1
        
        if group == 'Bullet:monster' or group == 'Arrow:monster':
            if monster.unheatCount == 0:
                monster.isAttacked = True
                monster.hp -= other.power
                damageEffect = effects.Damage(monster, other.power)
                game_world.add_object(damageEffect, 0)
                
        elif group == 'pickaxeRedEffect:monster' and server.player.weapon.isAttack:
            if monster.unheatCount == 0:
                monster.isAttacked = True
                monster.hp -= other.power
                damageEffect = effects.Damage(monster, other.power)
                game_world.add_object(damageEffect, 0)
                
        elif group == 'shortSwordEffect:monster' and server.player.weapon.isAttack:
            if monster.unheatCount == 0:
                monster.isAttacked = True
                monster.hp -= other.power
                damageEffect = effects.Damage(monster, other.power)
                game_world.add_object(damageEffect, 0)
    
    def update(monster):
        monster.sx, monster.sy = monster.x - server.map.window_left, monster.y - server.map.window_bottom
        
        if monster.hp <= 0:
            game_world.remove_collision_object(monster)
            game_world.remove_object(monster)
            destroyEffect = effects.DestroyEffect(monster.sx, monster.sy)
            game_world.add_object(destroyEffect, 0)
            
            #### remove_collision_object??? ????????? ??????????????? ???????????? ????????? ????????? ???????????? ??????
            monster.x = - 99999
            monster.y = - 99999
            monster.sx, monster.sy = monster.x - server.map.window_left, monster.y - server.map.window_bottom
            
        
        if monster.isAttacked:
            monster.unheatCount += game_framework.frame_time
            if monster.unheatCount >= 0.1:
                monster.unheatCount = 0
                monster.isAttacked  = False
        
        monster.frame = (monster.frame + BSS_IDLE_FRAMES_PER_ACTION * BSS_IDLE_ACTION_PER_TIME * game_framework.frame_time) % 5
        monster.lifeBar.update(monster)
        # monster.y -= 50

    def draw(monster):
        if monster.isAttacked:
            monster.idleShotImage.clip_composite_draw(int(monster.frame) * 33, 0, 33, 30, 0, 'h', monster.sx, monster.sy, 33 * 5, 30 * 5)
        else:
            monster.idleImage.clip_composite_draw(int(monster.frame) * 33, 0, 33, 30, 0, 'h', monster.sx, monster.sy, 33 * 5, 30 * 5)
        monster.lifeBar.draw(monster)
        draw_rectangle(*monster.get_bb())
