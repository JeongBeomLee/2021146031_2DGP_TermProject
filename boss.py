from pico2d import *
import game_framework
import game_world

from math import*
import random

import server
import ui
import effects
import bullet

mapSort = {'VILLIAGE' : 0, 'MOVE' : 1, 'JUMP' : 2, 'DASH' : 3, 'BATTLE' : 4, 'BOSS' : 5}

ghost_state = {'attack' : 0}
ghost_direction = {'left' : 0, 'right' : 1}

BHead_IDLE_TIME_PER_ACTION    = 0.5
BHead_IDLE_ACTION_PER_TIME    = 1.0 / BHead_IDLE_TIME_PER_ACTION
BHead_IDLE_FRAMES_PER_ACTION  = 10

BHead_ATTACK_TIME_PER_ACTION    = 0.5
BHead_ATTACK_ACTION_PER_TIME    = 1.0 / BHead_ATTACK_TIME_PER_ACTION
BHead_ATTACK_FRAMES_PER_ACTION  = 10

bullet_deg = 0
bullet_timer = 0

class Boss_Head:
    idleImage       = None
    idleShotImage   = None
    attackImage     = None
    attackShotImage = None
    
    def __init__(monster):
        if Boss_Head.idleImage == None:
            Boss_Head.idleImage = load_image("resources/images/boss/Belial/Head/idle.png")
        if Boss_Head.idleShotImage == None:
            Boss_Head.idleShotImage = load_image("resources/images/boss/Belial/Head/idle_shot.png")
            
        if Boss_Head.attackImage == None:
            Boss_Head.attackImage = load_image("resources/images/boss/Belial/Head/attack.png")
        if Boss_Head.attackShotImage == None:
            Boss_Head.attackShotImage = load_image("resources/images/boss/Belial/Head/attack_shot.png")
            
        monster.x           = 835
        monster.y           = 450
        monster.sx          = 0
        monster.sy          = 0
        monster.frame       = 0
        monster.isAttack    = False
        monster.isAttacked  = False
        monster.unheatCount = 0
        monster.pattern     = 0
        monster.finish_shoot = True
        monster.h = 180
        
        monster.hpMax = 10000
        monster.hp = 10000
        monster.power = 10
        monster.patternTimer = 0
        
        monster.LHand = Boss_LHand()
        monster.RHand = Boss_RHand()
        game_world.add_object(monster.LHand, 1)
        game_world.add_object(monster.RHand, 1)
        monster.lifeBar = ui.EnemyLifeBar(monster)
        
    def get_bb(monster):
        return monster.sx - 35 * 5, monster.sy - 48 * 5, monster.sx + 35 * 3 - 5, monster.sy + 48 * 3
    
    #### 객체별 충돌처리 ####
    def handle_collision(monster, other, group):
        if group == 'Bullet:monster' or group == 'Arrow:monster':
            if monster.unheatCount == 0:
                monster.isAttacked = True
                monster.hp -= other.power
                damageEffect = effects.Damage(monster, other.power)
                game_world.add_object(damageEffect, 1)
                
        elif group == 'pickaxeRedEffect:monster' and server.player.weapon.isAttack:
            if monster.unheatCount == 0:
                monster.isAttacked = True
                monster.hp -= other.power
                damageEffect = effects.Damage(monster, other.power)
                game_world.add_object(damageEffect, 1)
                
        elif group == 'shortSwordEffect:monster' and server.player.weapon.isAttack:
            if monster.unheatCount == 0:
                monster.isAttacked = True
                monster.hp -= other.power
                damageEffect = effects.Damage(monster, other.power)
                game_world.add_object(damageEffect, 1)
    
    def update(monster):
        global bullet_deg, bullet_timer
        monster.sx, monster.sy = monster.x - server.map.window_left, monster.y - server.map.window_bottom
        if monster.pattern == 0:
            monster.patternTimer += game_framework.frame_time
        if monster.patternTimer >= 2 and monster.pattern == 0:
            # monster.pattern = random.randint(1,3)
            monster.pattern = 1
            # monster.pattern = 2
        
        if monster.pattern == 1:
            bullet_timer += game_framework.frame_time
            if not monster.isAttack:
                monster.isAttack = True
                monster.frame    = 0
                monster.finish_shoot = False
            if monster.frame >= 4 and monster.finish_shoot == False:
                if bullet_deg != 180:
                    if bullet_timer >= 0.05:
                        monster.shoot_bullet(bullet_deg)
                        bullet_timer = 0.0
                    bullet_deg += 1
                    monster.frame = 4
                    
                if bullet_deg >= 180:
                    monster.finish_shoot = True
                    monster.isAttack = False
                    monster.frame    = 0
                    bullet_deg = 0
                    bullet_timer = 0
                    monster.pattern = 0
                    monster.patternTimer = 0
        
        
        if monster.hp <= 0:
            game_world.remove_collision_object(monster)
            game_world.remove_object(monster)
            destroyEffect = effects.DestroyEffect(monster.sx, monster.sy)
            game_world.add_object(destroyEffect, 0)
            
            #### remove_collision_object가 객체의 충돌영역을 지워주지 못해서 객체를 다른데로 보냄
            monster.x = - 99999
            monster.y = - 99999
            monster.sx, monster.sy = monster.x - server.map.window_left, monster.y - server.map.window_bottom
            
        if monster.isAttacked:
            monster.unheatCount += game_framework.frame_time
            if monster.unheatCount >= 0.1:
                monster.unheatCount = 0
                monster.isAttacked  = False
                
        if monster.isAttack:
            monster.frame = (monster.frame + BHead_ATTACK_FRAMES_PER_ACTION * BHead_ATTACK_ACTION_PER_TIME * game_framework.frame_time) % 10
            if monster.frame >= 10:
                pass
        elif not monster.isAttack:
            monster.frame = (monster.frame + BHead_IDLE_FRAMES_PER_ACTION * BHead_IDLE_ACTION_PER_TIME * game_framework.frame_time) % 10
        # monster.LHand.update()
        # monster.RHand.update()
        monster.lifeBar.update(monster)
        # monster.y -= 50

    def draw(monster):
        if monster.isAttacked and not monster.isAttack:
            monster.idleShotImage.clip_composite_draw(int(monster.frame) * 70, 0, 70, 96, 0, 'h', monster.sx, monster.sy, 70 * 5, 96 * 5)
        elif not monster.isAttacked and not monster.isAttack:
            monster.idleImage.clip_composite_draw(int(monster.frame) * 70, 0, 70, 96, 0, 'h', monster.sx, monster.sy, 70 * 5, 96 * 5)
            
        if monster.isAttacked and monster.isAttack:
            monster.attackShotImage.clip_composite_draw(int(monster.frame) * 70, 0, 70, 128, 0, 'h', monster.sx, monster.sy, 70 * 5, 128 * 5)
        elif not monster.isAttacked and monster.isAttack:
            monster.attackImage.clip_composite_draw(int(monster.frame) * 70, 0, 70, 128, 0, 'h', monster.sx, monster.sy, 70 * 5, 128 * 5)
        monster.lifeBar.draw(monster)
        draw_rectangle(*monster.get_bb())
        
    def shoot_bullet(monster, deg):
        ball = bullet.Boss_Bullet(monster.x - 20 + 50 * cos(radians(deg)), monster.y - 100 + 50 * sin(radians(deg)), 20 * cos(radians(deg)), 20 * sin(radians(deg)))
        game_world.add_object(ball, 1)
        game_world.add_collision_pairs(server.player, ball, 'player:ball')
        ball = bullet.Boss_Bullet(monster.x - 20 + 50 * cos(radians(deg + 90)), monster.y - 100 + 50 * sin(radians(deg + 90)), 20 * cos(radians(deg + 90)), 20 * sin(radians(deg + 90)))
        game_world.add_object(ball, 1)
        game_world.add_collision_pairs(server.player, ball, 'player:ball')
        ball = bullet.Boss_Bullet(monster.x - 20 + 50 * cos(radians(deg + 180)), monster.y - 100 + 50 * sin(radians(deg + 180)), 20 * cos(radians(deg + 180)), 20 * sin(radians(deg + 180)))
        game_world.add_object(ball, 1)
        game_world.add_collision_pairs(server.player, ball, 'player:ball')
        ball = bullet.Boss_Bullet(monster.x - 20 + 50 * cos(radians(deg + 270)), monster.y - 100 + 50 * sin(radians(deg + 270)), 20 * cos(radians(deg + 270)), 20 * sin(radians(deg + 270)))
        game_world.add_object(ball, 1)
        game_world.add_collision_pairs(server.player, ball, 'player:ball')
        

BHand_IDLE_TIME_PER_ACTION    = 0.5
BHand_IDLE_ACTION_PER_TIME    = 1.0 / BHand_IDLE_TIME_PER_ACTION
BHand_IDLE_FRAMES_PER_ACTION  = 10

BHand_ATTACK_TIME_PER_ACTION    = 2.0
BHand_ATTACK_ACTION_PER_TIME    = 1.0 / BHand_ATTACK_TIME_PER_ACTION
BHand_ATTACK_FRAMES_PER_ACTION  = 18

class Boss_LHand:
    idleImage       = None
    attackImage     = None
    
    def __init__(self):
        if Boss_LHand.idleImage == None:
            Boss_LHand.idleImage = load_image("resources/images/boss/Belial/Hand/idle.png")
            
        if Boss_LHand.attackImage == None:
            Boss_LHand.attackImage = load_image("resources/images/boss/Belial/Hand/attack.png")
            
        self.x           = 100
        self.y           = 600
        self.sx          = 0
        self.sy          = 0
        self.frame       = 0
        self.isAttack    = False
        
    def get_bb(self):
        pass
    
    #### 객체별 충돌처리 ####
    def handle_collision(self, other, group):
        pass
    
    def update(self):
        self.sx, self.sy = self.x - server.map.window_left, self.y - server.map.window_bottom
        
        if server.monster.hp <= 0:
            game_world.remove_collision_object(self)
            game_world.remove_object(self)
            destroyEffect = effects.DestroyEffect(self.sx, self.sy)
            game_world.add_object(destroyEffect, 0)
            
            #### remove_collision_object가 객체의 충돌영역을 지워주지 못해서 객체를 다른데로 보냄
            self.x = - 99999
            self.y = - 99999
            self.sx, self.sy = self.x - server.map.window_left, self.y - server.map.window_bottom
        
        self.frame = (self.frame + BHand_IDLE_FRAMES_PER_ACTION * BHand_IDLE_ACTION_PER_TIME * game_framework.frame_time) % 10
        # monster.y -= 50

    def draw(self):
        self.idleImage.clip_composite_draw(int(self.frame) * 57, 0, 57, 67, 0, 'n', self.sx, self.sy, 57 * 5, 67 * 5)
        
class Boss_RHand:
    idleImage       = None
    attackImage     = None
    
    def __init__(self):
        if Boss_RHand.idleImage == None:
            Boss_RHand.idleImage = load_image("resources/images/boss/Belial/Hand/idle.png")
            
        if Boss_RHand.attackImage == None:
            Boss_RHand.attackImage = load_image("resources/images/boss/Belial/Hand/attack.png")
            
        self.x           = 1500
        self.y           = 300
        self.sx          = 0
        self.sy          = 0
        self.frame       = 0
        self.isAttack    = False
        
    def get_bb(self):
        pass
    
    #### 객체별 충돌처리 ####
    def handle_collision(self, other, group):
        pass
    
    def update(self):
        self.sx, self.sy = self.x - server.map.window_left, self.y - server.map.window_bottom
        
        if server.monster.hp <= 0:
            game_world.remove_collision_object(self)
            game_world.remove_object(self)
            destroyEffect = effects.DestroyEffect(self.sx, self.sy)
            game_world.add_object(destroyEffect, 0)
            
            #### remove_collision_object가 객체의 충돌영역을 지워주지 못해서 객체를 다른데로 보냄
            self.x = - 99999
            self.y = - 99999
            self.sx, self.sy = self.x - server.map.window_left, self.y - server.map.window_bottom
        
        self.frame = (self.frame + BHand_IDLE_FRAMES_PER_ACTION * BHand_IDLE_ACTION_PER_TIME * game_framework.frame_time) % 10
        # monster.y -= 50

    def draw(self):
        self.idleImage.clip_composite_draw(int(self.frame) * 57, 0, 57, 67, 0, 'h', self.sx, self.sy, 57 * 5, 67 * 5)
        