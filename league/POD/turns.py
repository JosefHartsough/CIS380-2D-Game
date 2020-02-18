from league import *
import pygame
import league
from enums import *
import pprint
from handle_animations import Handle_Animations
from change_scene import Change_Scene
import time
import sys
from player import Player


class Turns():

    def __init__(self, player, enemy, engine):
        self.player = player
        self.enemy = enemy
        self.engine = engine
        self.has_not_hit_left = True
        self.has_not_hit_right = True
        self.has_not_hit_up = True
        self.has_not_hit_down = True
        self.enemy.turn = False
        self.last_move = pygame.time.get_ticks()


    ###########################################################################
    # Movement stuff
    ###########################################################################

    def move_left(self, time):
        if self.player.turn:
            if self.has_not_hit_left:
                self.player_before_x = self.player.x
                self.player_before_y = self.player.y
            if abs(self.player_before_x - self.player.x) <= self.player.tile_size:
                if abs(self.player_before_x - self.player.x) > self.player.tile_size // 2:
                    self.turn_off_inputs_except(pygame.K_a)
                self.player.move_left(time)
            else:
                self.player.turn = False
            self.has_not_hit_left = False
        else:
            self.engine.key_events[pygame.K_a] = self.ghetto_stop
            self.move_enemies(time)

    def move_right(self, time):
        if self.player.turn:
            if self.has_not_hit_right:
                self.player_before_x = self.player.x
                self.player_before_y = self.player.y
            self.last_move = pygame.time.get_ticks()
            if abs(self.player_before_x - self.player.x) <= self.player.tile_size:
                if abs(self.player_before_x - self.player.x) > self.player.tile_size // 2:
                    self.turn_off_inputs_except(pygame.K_d)
                self.player.move_right(time)
            else:
                self.player.turn = False
            self.has_not_hit_right = False
        else:
            self.engine.key_events[pygame.K_d] = self.ghetto_stop
            self.move_enemies(time)

    def move_up(self, time):
        if self.player.turn:
            if self.has_not_hit_up:
                self.player_before_x = self.player.x
                self.player_before_y = self.player.y
            if abs(self.player_before_y - self.player.y) <= self.player.tile_size:
                if abs(self.player_before_y - self.player.y) > self.player.tile_size // 2:
                    self.turn_off_inputs_except(pygame.K_w)
                self.player.move_up(time)
            else:
                self.player.turn = False
            self.has_not_hit_up = False
        else:
            self.engine.key_events[pygame.K_w] = self.ghetto_stop
            self.move_enemies(time)

    def move_down(self, time):
        if self.player.turn:
            if self.has_not_hit_down:
                self.player_before_x = self.player.x
                self.player_before_y = self.player.y
            if abs(self.player_before_y - self.player.y) <= self.player.tile_size:
                if abs(self.player_before_y - self.player.y) > self.player.tile_size // 2:
                    self.turn_off_inputs_except(pygame.K_s)
                self.player.move_down(time)
            else:
                self.player.turn = False
            self.has_not_hit_down = False
        else:
            self.engine.key_events[pygame.K_s] = self.ghetto_stop
            self.move_enemies(time)

    def move_enemies(self, time):
        """
        This is a pretty big and nasty method that basically acts as the AI for
        the enemies. Whichever direction, x or y, that I am further away from
        the player, I will move in that direction. Then just figure out where
        the player is in comparison to me and move that way. I want to keep
        pressing the move command until I, the enemy, has moved 64 pixels.
        """
        before_x = self.enemy.x
        before_y = self.enemy.y
        dist_from_x = abs(self.enemy.x - self.player.x)
        dist_from_y = abs(self.enemy.y - self.player.y)
        for x in range(0, 50):
            if dist_from_x >= dist_from_y:
                if self.enemy.x >= self.player.x:
                    if abs(before_x - self.enemy.x) <= self.player.tile_size:
                        self.enemy.move_left(time)
                    else:
                        break
                else:
                    if abs(before_x - self.enemy.x) <= self.player.tile_size:
                        self.enemy.move_right(time)
                    else:
                        break
            else:
                if self.enemy.y >= self.player.y:
                    if abs(before_y - self.enemy.y) <= self.player.tile_size:
                        self.enemy.move_up(time)
                    else:
                        break
                else:
                    if abs(before_y - self.enemy.y) <= self.player.tile_size:
                        self.enemy.move_down(time)
                    else:
                        break
        self.reset_variables()


    def ghetto_stop(self, time):
        pass

    def reset_variables(self):
        self.enemy.turn = False
        self.player.turn = True
        self.has_not_hit_left = True
        self.has_not_hit_right = True
        self.has_not_hit_up= True
        self.has_not_hit_down = True
        self.engine.key_events[pygame.K_a] = self.move_left
        self.engine.key_events[pygame.K_d] = self.move_right
        self.engine.key_events[pygame.K_w] = self.move_up
        self.engine.key_events[pygame.K_s] = self.move_down
        self.engine.key_events[pygame.K_1] = self.attack_1
        self.engine.key_events[pygame.K_2] = self.attack_2
        self.engine.key_events[pygame.K_3] = self.attack_3
        self.engine.key_events[pygame.K_4] = self.attack_4
        self.engine.key_events[pygame.K_5] = self.attack_5

    def turn_off_inputs_except(self, keep_input):
        for event in list(self.engine.key_events):
            if event != keep_input:
                self.engine.key_events.pop(event)

    ###########################################################################
    # Attacking stuff
    ###########################################################################

    def attack_1(self, time):
        if self.player.turn:
            if self.player.attack_1_finished:
                if self.check_damage_small_weapon():
                    self.enemy.health -= Attack_Damage.FIRST_ATTACK
                self.player.turn = False
            else:
                self.player.attack_1(time)
                self.turn_off_inputs_except(pygame.K_1)
            if self.enemy in self.engine.objects:
                self.remove_enemy()
        else:
            self.engine.key_events[pygame.K_1] = self.ghetto_stop
            self.move_enemies(time)

    def attack_2(self, time):
        if self.player.turn:
            self.turn_off_inputs_except(pygame.K_2)
            self.player.attack_2(time)
            if self.player.attack_2_finished:
                if self.check_damage_small_weapon():
                    self.enemy.health -= Attack_Damage.SECOND_ATTACK
                self.player.turn = False
            if self.enemy in self.engine.objects:
                self.remove_enemy()
        else:
            self.engine.key_events[pygame.K_2] = self.ghetto_stop
            self.move_enemies(time)


    def attack_3(self, time):
        if self.player.turn:
            self.turn_off_inputs_except(pygame.K_3)
            self.player.attack_3(time)
            if self.player.attack_3_finished:
                if self.check_damage_small_weapon():
                    self.enemy.health -= Attack_Damage.THIRD_ATTACK
                self.player.turn = False
            if self.enemy in self.engine.objects:
                self.remove_enemy()
        else:
            self.engine.key_events[pygame.K_3] = self.ghetto_stop
            self.move_enemies(time)


    def attack_4(self, time):
        if self.player.turn:
            self.turn_off_inputs_except(pygame.K_4)
            self.player.attack_4(time)
            if self.player.attack_4_finished:
                if self.check_damage_small_weapon():
                    self.enemy.health -= Attack_Damage.FOURTH_ATTACK
                self.player.turn = False
            if self.enemy in self.engine.objects:
                self.remove_enemy()
        else:
            self.engine.key_events[pygame.K_4] = self.ghetto_stop
            self.move_enemies(time)


    def attack_5(self, time):
        if self.player.turn:
            self.turn_off_inputs_except(pygame.K_5)
            self.player.attack_5(time)
            if self.player.attack_5_finished:
                if self.check_damage_big_weapon():
                    self.enemy.health -= Attack_Damage.FIFTH_ATTACK
                self.player.turn = False
            if self.enemy in self.engine.objects:
                self.remove_enemy()
        else:
            self.engine.key_events[pygame.K_5] = self.ghetto_stop
            self.move_enemies(time)

    def check_damage_small_weapon(self):
        if abs(self.player.x - self.enemy.x) < 64 and abs(self.player.y - self.enemy.y) < 64:
            return True
        else:
            return False

    def check_damage_big_weapon(self):
        if abs(self.player.x - self.enemy.x) - 85 < 64 and abs(self.player.y - self.enemy.y) - 65 < 64:
            return True
        else:
            return False

    def remove_enemy(self):
        if self.enemy.health <= 0:
            self.engine.objects.remove(self.enemy)
            self.engine.drawables.remove(self.enemy)
