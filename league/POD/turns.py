from league import *
import pygame
import league
from enums import *
import pprint
from handle_animations import Handle_Animations
from change_scene import Change_Scene
import time
import sys
# from player import Player
import random
# from enemy import Enemy


class Turns():

    def __init__(self, player, enemies, engine):
        self.player = player
        self.enemies = enemies
        self.engine = engine
        self.has_not_hit_left = True
        self.has_not_hit_right = True
        self.has_not_hit_up = True
        self.has_not_hit_down = True
        for enemy in self.enemies:
            enemy.turn = False

        self.last_attack_was_1 = False
        self.last_attack_was_2 = False
        self.last_attack_was_3 = False
        self.last_attack_was_4 = False
        self.last_attack_was_5 = False

        self.all_attacks = {
            1: False, # last attack was 1
            2: False, # last attack was 2
            3: False, # last attack was 3
            4: False, # last attack was 4
            5: False  # last attack was 5
        }

        self.player_movement = []

    ###########################################################################
    # Movement stuff
    ###########################################################################

    def move_left(self, time):
        if self.player.turn:
            if self.has_not_hit_left:
                self.player_before_x = self.player.x
                self.player_before_y = self.player.y
            if abs(self.player_before_x - self.player.x) <= self.player.tile_size:
                self.player_movement.append((self.player.x, self.player.y))
                if len(self.player_movement) > 3:
                    # check if the player hasn't been able to move
                    if(abs(self.player_movement[-1][0] - self.player_movement[-3][0]) < 1 and
                       abs(self.player_movement[-1][1] - self.player_movement[-3][1] < 1)):
                        self.engine.key_events[pygame.K_a] = self.move_left
                        self.engine.key_events[pygame.K_d] = self.move_right
                        self.engine.key_events[pygame.K_w] = self.move_up
                        self.engine.key_events[pygame.K_s] = self.move_down
                    else:
                        if abs(self.player_before_x - self.player.x) > self.player.tile_size // 2:
                            self.turn_off_inputs_except(pygame.K_a)
                            self.engine.key_events[pygame.K_1] = self.attack_1
                            self.engine.key_events[pygame.K_2] = self.attack_2
                            self.engine.key_events[pygame.K_3] = self.attack_3
                            self.engine.key_events[pygame.K_4] = self.attack_4
                            self.engine.key_events[pygame.K_5] = self.attack_5
                self.player.move_left(time)
            else:
                self.player.turn = False
            self.has_not_hit_left = False
        else:
            self.engine.key_events[pygame.K_a] = self.ghetto_stop
            self.enemy_decision(time)

    def move_right(self, time):
        if self.player.turn:
            if self.has_not_hit_right:
                self.player_before_x = self.player.x
                self.player_before_y = self.player.y
            if abs(self.player_before_x - self.player.x) <= self.player.tile_size:
                self.player_movement.append((self.player.x, self.player.y))
                if len(self.player_movement) > 3:
                    # check if the player hasn't been able to move
                    if(abs(self.player_movement[-1][0] - self.player_movement[-3][0]) < 1 and
                       abs(self.player_movement[-1][1] - self.player_movement[-3][1] < 1)):
                        self.engine.key_events[pygame.K_a] = self.move_left
                        self.engine.key_events[pygame.K_d] = self.move_right
                        self.engine.key_events[pygame.K_w] = self.move_up
                        self.engine.key_events[pygame.K_s] = self.move_down
                    else:
                        if abs(self.player_before_x - self.player.x) > self.player.tile_size // 2:
                            self.turn_off_inputs_except(pygame.K_d)
                            self.engine.key_events[pygame.K_1] = self.attack_1
                            self.engine.key_events[pygame.K_2] = self.attack_2
                            self.engine.key_events[pygame.K_3] = self.attack_3
                            self.engine.key_events[pygame.K_4] = self.attack_4
                            self.engine.key_events[pygame.K_5] = self.attack_5
                self.player.move_right(time)
            else:
                self.player.turn = False
            self.has_not_hit_right = False
        else:
            self.engine.key_events[pygame.K_d] = self.ghetto_stop
            self.enemy_decision(time)

    def move_up(self, time):
        if self.player.turn:
            if self.has_not_hit_up:
                self.player_before_x = self.player.x
                self.player_before_y = self.player.y
            if abs(self.player_before_y - self.player.y) <= self.player.tile_size:
                self.player_movement.append((self.player.x, self.player.y))
                if len(self.player_movement) > 3:
                    # check if the player hasn't been able to move
                    if(abs(self.player_movement[-1][0] - self.player_movement[-3][0]) < 1 and
                       abs(self.player_movement[-1][1] - self.player_movement[-3][1] < 1)):
                        self.engine.key_events[pygame.K_a] = self.move_left
                        self.engine.key_events[pygame.K_d] = self.move_right
                        self.engine.key_events[pygame.K_w] = self.move_up
                        self.engine.key_events[pygame.K_s] = self.move_down
                    else:
                        if abs(self.player_before_y - self.player.y) > self.player.tile_size // 2:
                            self.turn_off_inputs_except(pygame.K_w)
                            self.engine.key_events[pygame.K_1] = self.attack_1
                            self.engine.key_events[pygame.K_2] = self.attack_2
                            self.engine.key_events[pygame.K_3] = self.attack_3
                            self.engine.key_events[pygame.K_4] = self.attack_4
                            self.engine.key_events[pygame.K_5] = self.attack_5
                self.player.move_up(time)
            else:
                self.player.turn = False
            self.has_not_hit_up = False
        else:

            self.engine.key_events[pygame.K_w] = self.ghetto_stop
            self.enemy_decision(time)

    def move_down(self, time):
        if self.player.turn:
            if self.has_not_hit_down:
                self.player_before_x = self.player.x
                self.player_before_y = self.player.y
            if abs(self.player_before_y - self.player.y) <= self.player.tile_size:
                self.player_movement.append((self.player.x, self.player.y))
                if len(self.player_movement) > 3:
                    # check if the player hasn't been able to move
                    if(abs(self.player_movement[-1][0] - self.player_movement[-3][0]) < 1 and
                       abs(self.player_movement[-1][1] - self.player_movement[-3][1] < 1)):
                        self.engine.key_events[pygame.K_a] = self.move_left
                        self.engine.key_events[pygame.K_d] = self.move_right
                        self.engine.key_events[pygame.K_w] = self.move_up
                        self.engine.key_events[pygame.K_s] = self.move_down
                    else:
                        if abs(self.player_before_y - self.player.y) > self.player.tile_size // 2:
                            self.turn_off_inputs_except(pygame.K_s)
                            self.engine.key_events[pygame.K_1] = self.attack_1
                            self.engine.key_events[pygame.K_2] = self.attack_2
                            self.engine.key_events[pygame.K_3] = self.attack_3
                            self.engine.key_events[pygame.K_4] = self.attack_4
                            self.engine.key_events[pygame.K_5] = self.attack_5
                self.player.move_down(time)
            else:
                self.player.turn = False
            self.has_not_hit_down = False
        else:
            self.engine.key_events[pygame.K_s] = self.ghetto_stop
            self.enemy_decision(time)

    ###########################################################################
    # Attacking stuff
    ###########################################################################

    def attack_1(self, time):
        if self.player.turn:
            if not self.all_attacks[1]:
                if self.player.attack_1_finished:
                    self.check_damage_small_weapon(Attack_Damage.FIRST_ATTACK)
                    self.player.turn = False
                    loc_in_sprite_sheet = self.player.pull_sprite(self.player.direction, 0, file = self.player.sprites_to_use)
                    self.player.update_sprite(loc_in_sprite_sheet, offset_x = 0)
                    self.control_last_attack(1)
                else:
                    self.player.attack_1(time)
                    self.turn_off_inputs_except(pygame.K_1)
        else:
            self.engine.key_events[pygame.K_1] = self.ghetto_stop
            self.enemy_decision(time)

    def attack_2(self, time):
        if self.player.turn:
            if not self.all_attacks[2]:
                if self.player.attack_2_finished:
                    self.check_damage_small_weapon(Attack_Damage.SECOND_ATTACK)
                    self.player.turn = False
                    loc_in_sprite_sheet = self.player.pull_sprite(self.player.direction, 0, file = self.player.sprites_to_use)
                    self.player.update_sprite(loc_in_sprite_sheet, offset_x = 0)
                    self.control_last_attack(2)
                else:
                    self.player.attack_2(time)
                    self.turn_off_inputs_except(pygame.K_2)
        else:
            self.engine.key_events[pygame.K_2] = self.ghetto_stop
            self.enemy_decision(time)


    def attack_3(self, time):
        if self.player.turn:
            if not self.all_attacks[3]:
                if self.player.attack_3_finished:
                    self.check_damage_small_weapon(Attack_Damage.THIRD_ATTACK)
                    self.player.turn = False
                    loc_in_sprite_sheet = self.player.pull_sprite(self.player.direction, 0, file = self.player.sprites_to_use)
                    self.player.update_sprite(loc_in_sprite_sheet, offset_x = 0)
                    self.control_last_attack(3)
                else:
                    self.player.attack_3(time)
                    self.turn_off_inputs_except(pygame.K_3)
        else:
            self.engine.key_events[pygame.K_3] = self.ghetto_stop
            self.enemy_decision(time)


    def attack_4(self, time):
        if self.player.turn:
            if not self.all_attacks[4]:
                if self.player.attack_4_finished:
                    self.check_damage_small_weapon(Attack_Damage.FOURTH_ATTACK)
                    self.player.turn = False
                    loc_in_sprite_sheet = self.player.pull_sprite(self.player.direction, 0, file = self.player.sprites_to_use)
                    self.player.update_sprite(loc_in_sprite_sheet, offset_x = 0)
                    self.control_last_attack(4)
                else:
                    self.player.attack_4(time)
                    self.turn_off_inputs_except(pygame.K_4)
        else:
            self.engine.key_events[pygame.K_4] = self.ghetto_stop
            self.enemy_decision(time)


    def attack_5(self, time):
        if self.player.turn:
            if not self.all_attacks[5]:
                if self.player.attack_5_finished:
                    self.check_damage_big_weapon(Attack_Damage.FIFTH_ATTACK)
                    self.player.turn = False
                    loc_in_sprite_sheet = self.player.pull_sprite(self.player.direction, 0, file = self.player.sprites_to_use)
                    self.player.update_sprite(loc_in_sprite_sheet, offset_x = 0)
                    self.control_last_attack(5)
                else:
                    self.player.attack_5(time)
                    self.turn_off_inputs_except(pygame.K_5)
        else:
            self.engine.key_events[pygame.K_5] = self.ghetto_stop
            self.enemy_decision(time)

    def check_damage_small_weapon(self, damage):
        for enemy in self.enemies:
            if abs(self.player.x - enemy.x) < 64 and abs(self.player.y - enemy.y) < 64:
                enemy.health -= damage
                if enemy in self.engine.objects:
                    if enemy.health <= 0:
                        self.engine.objects.remove(enemy)
                        self.engine.drawables.remove(enemy)
                        self.enemies.remove(enemy)

    def check_damage_big_weapon(self, damage):
        for enemy in self.enemies:
            if abs(self.player.x - enemy.x) - 85 < 64 and abs(self.player.y - enemy.y) - 65 < 64:
                enemy.health -= damage
                if enemy in self.engine.objects:
                    if enemy.health <= 0:
                        self.engine.objects.remove(enemy)
                        self.engine.drawables.remove(enemy)
                        self.enemies.remove(enemy)

    def control_last_attack(self, last_attack):
        for attack in self.all_attacks.keys():
            if attack == last_attack:
                self.all_attacks[attack] = True
            else:
                self.all_attacks[attack] = False
        self.player.update_self_variables()

    ###########################################################################
    # Helper Functions
    ###########################################################################

    def enemy_decision(self, time):
        for enemy in self.enemies:
            dist_from_x = abs(enemy.x - self.player.x)
            dist_from_y = abs(enemy.y - self.player.y)

            if dist_from_x < 64 and dist_from_y < 64:
                self.attack_player(time, enemy, dist_from_x, dist_from_y)
            elif dist_from_x < 1000 and dist_from_y < 1000:
                self.move_enemies_to_player(time, enemy, dist_from_x, dist_from_y)
            else:
                self.move_randomly(enemy, {"any"}, time)
        self.reset_variables()

    def attack_player(self, time, enemy, dist_from_x, dist_from_y):
        for x in range(0, 20):
            enemy.choose_attack(time)
        self.player.health -= enemy.attack_damage

    def move_enemies_to_player(self, time, enemy, dist_from_x, dist_from_y):
        """
        This is a pretty big and nasty method that basically acts as the AI for
        the enemies. Whichever direction, x or y, that I am further away from
        the player, I will move in that direction. Then just figure out where
        the player is in comparison to me and move that way. I want to keep
        pressing the move command until I, the enemy, has moved 64 pixels.
        """
        before_x = enemy.x
        before_y = enemy.y
        path = []
        # I randomly chose 50 just to give it enough cycles to move 64 pixels
        for x in range(0, 50):
            # track enemy position
            path.append((enemy.x, enemy.y))
            # move in the x direction
            if dist_from_x >= dist_from_y:
                # if the player is to my left
                if enemy.x >= self.player.x:
                    if abs(before_x - enemy.x) <= self.player.tile_size:
                        if len(path) > 3:
                            # If I have not moved, go in a random direction
                            if abs(path[x][0] - path[x-2][0]) < 1 and abs(path[x][1] - path[x-2][1] < 1):
                                self.move_randomly(enemy, {"left"}, time)
                            else:
                                enemy.move_left(time)
                        else:
                            enemy.move_left(time)
                    else:
                        break
                # if the player is to my right
                else:
                    if abs(before_x - enemy.x) <= self.player.tile_size:
                        if len(path) > 3:
                            # If I have not moved, go in a random direction
                            if abs(path[x][0] - path[x-2][0]) < 1 and abs(path[x][1] - path[x-2][1] < 1):
                                self.move_randomly(enemy, {"right"}, time)
                            else:
                                enemy.move_right(time)
                        else:
                            enemy.move_right(time)
                    else:
                        break
            # move in the y direction
            else:
                # if the player is above me
                if enemy.y >= self.player.y:
                    if abs(before_y - enemy.y) <= self.player.tile_size:
                        if len(path) > 3:
                            # If I have not moved, go in a random direction
                            if abs(path[x][0] - path[x-2][0]) < 1 and abs(path[x][1] - path[x-2][1] < 1):
                                self.move_randomly(enemy, {"up"}, time)
                            else:
                                enemy.move_up(time)
                        else:
                            enemy.move_up(time)
                    else:
                        break
                # if the player is below me
                else:
                    if abs(before_y - enemy.y) <= self.player.tile_size:
                        if len(path) > 3:
                            # If I have not moved, go in a random direction
                            if abs(path[x][0] - path[x-2][0]) < 1 and abs(path[x][1] - path[x-2][1] < 1):
                                self.move_randomly(enemy, {"down"}, time)
                            else:
                                enemy.move_down(time)
                        else:
                            enemy.move_down(time)
                    else:
                        break

    def move_randomly(self, sprite_to_move, direction_to_not_move, time):
        # do set subtraction to figure out which direction to go and then
        # randomly pick from that result
        choice = random.choice(tuple({"up", "down", "left", "right"} - direction_to_not_move))
        if choice == "up":
            sprite_to_move.move_up(time)
        elif choice == "down":
            sprite_to_move.move_down(time)
        elif choice == "left":
            sprite_to_move.move_left(time)
        elif choice == "right":
            sprite_to_move.move_right(time)



    def ghetto_stop(self, time):
        pass

    def reset_variables(self):
        for enemy in self.enemies:
            enemy.turn = False
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
        self.player_movement.clear()


    def turn_off_inputs_except(self, keep_input):
        for event in list(self.engine.key_events):
            if event != keep_input:
                self.engine.key_events.pop(event)
