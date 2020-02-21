from league import *
import pygame
import league
from enums import *
import pprint
from handle_animations import Handle_Animations
from change_scene import Change_Scene
import time
import sys


class Enemy(Character, Handle_Animations, Change_Scene):
    """
    This is a sample class for a player object.  A player
    is a character, is a drawable, and an updateable object.
    This class should handle everything a player does, such as
    moving, throwing/shooting, collisions, etc.  It was hastily
    written as a demo but should direction.
    """

    def __init__(self, sprites_to_use, z=0, x=0, y=0, attack_to_animate = 1, health = 100, damage = 69):
        super().__init__(z, x, y)

        # What sprites am I not allowd to cross?
        self.blocks = pygame.sprite.Group()
        # This unit's health
        self.health = health
        # Last time I was hit
        self.last_hit = pygame.time.get_ticks()
        # A unit-less value. Bigger is faster. Changes player speed
        self.delta = 100
        # Where the player is positioned
        self.x = x
        self.y = y
        self.z = 0

       
        # images to pull from
        self.sprites_to_use = sprites_to_use

        # attack to animate
        self.attack_to_animate = attack_to_animate

        # attack damage
        self.attack_damage = damage

        # these are the rows on the sprite sheet that correspond with him walking
        self.walk_up_row = 8
        self.walk_left_row = 9
        self.walk_down_row = 10
        self.walk_right_row = 11
        walking_rows = [self.walk_up_row, self.walk_left_row,
                        self.walk_down_row, self.walk_right_row]
        self.num_animations_to_walk = 8

        # these are the rows on the sprite sheet that make him use his first attack
        self.attack_1_up_row = 0
        self.attack_1_left_row = 1
        self.attack_1_down_row = 2
        self.attack_1_right_row = 3
        attacking_rows_1 = [self.attack_1_up_row, self.attack_1_left_row,
                            self.attack_1_down_row, self.attack_1_right_row]
        self.num_animations_to_attack_1 = 7
        self.attack_1_animation = 0
        self.attack_1_finished = False

        # these are the rows on the sprite sheet that make him use his second attack
        self.attack_2_up_row = 4
        self.attack_2_left_row = 5
        self.attack_2_down_row = 6
        self.attack_2_right_row = 7
        attacking_rows_2 = [self.attack_2_up_row, self.attack_2_left_row,
                            self.attack_2_down_row, self.attack_2_right_row]
        self.num_animations_to_attack_2 = 8
        self.attack_2_animation = 0
        self.attack_2_finished = False

        # these are the rows on the sprite sheet that make him use his third attack
        self.attack_3_up_row = 12
        self.attack_3_left_row = 13
        self.attack_3_down_row = 14
        self.attack_3_right_row = 15
        attacking_rows_3 = [self.attack_3_up_row, self.attack_3_left_row,
                            self.attack_3_down_row, self.attack_3_right_row]
        self.num_animations_to_attack_3 = 6
        self.attack_3_animation = 0
        self.attack_3_finished = False

        # these are the rows on the sprite sheet that make him use his fourth attack
        self.attack_4_up_row = 16
        self.attack_4_left_row = 17
        self.attack_4_down_row = 18
        self.attack_4_right_row = 19
        attacking_rows_4 = [self.attack_4_up_row, self.attack_4_left_row,
                            self.attack_4_down_row, self.attack_4_right_row]
        self.num_animations_to_attack_4 = 13
        self.attack_4_animation = 0
        self.attack_4_finished = False

        # these are the rows on the sprite sheet that make him use his fifth attack
        self.attack_5_up_row = 21
        self.attack_5_left_row = 24
        self.attack_5_down_row = 27
        self.attack_5_right_row = 30
        attacking_rows_5 = [self.attack_5_up_row, self.attack_5_left_row, self.attack_5_down_row, self.attack_5_right_row]
        self.num_animations_to_attack_5 = 8
        self.attack_5_animation = 0
        self.has_not_hit_5 = True
        self.attack_5_finished = False

        # create animation needed variables
        self.tile_size = league.Settings.tile_size * 2
        self.direction = Moving.SOUTH
        self.state = Player_State.IDLE
        self.images = {}
        self.images[Player_State.WALK] = {}
        self.images[Player_State.ATTACK_1] = {}
        self.images[Player_State.ATTACK_2] = {}
        self.images[Player_State.ATTACK_3] = {}
        self.images[Player_State.ATTACK_4] = {}
        self.images[Player_State.ATTACK_5] = {}
        self.frame = 0
        self.turn = True

        # Load in all of the pictures required for moving. Rather than calling
        # a function for each row, I combined the rows into an array and we simply
        # loop through that array and then call the function to retrieve the
        # necessary pictures.
        for row in walking_rows:
            self.images[Player_State.WALK].update(self.animate_walking(row))

        if attack_to_animate == 1:
            for row in attacking_rows_1:
                self.images[Player_State.ATTACK_1].update(self.animate_attacking_1(row, self.num_animations_to_attack_1))

        elif attack_to_animate == 2:
            for row in attacking_rows_2:
                self.images[Player_State.ATTACK_2].update(self.animate_attacking_2(row, self.num_animations_to_attack_2))

        elif attack_to_animate == 3:
            for row in attacking_rows_3:
                self.images[Player_State.ATTACK_3].update(self.animate_attacking_3(row, self.num_animations_to_attack_3))

        elif attack_to_animate == 4:
            for row in attacking_rows_4:
                self.images[Player_State.ATTACK_4].update(self.animate_attacking_4(row, self.num_animations_to_attack_4))

        elif attack_to_animate == 5:
            for row in attacking_rows_5:
                self.images[Player_State.ATTACK_5].update(self.animate_attacking_5(row, self.num_animations_to_attack_5))


        # Give our person an initial spawned in orientation
        # 21 rows (starting at 1), before big picture
        loc_in_sprite_sheet = self.pull_sprite(self.direction, 0, file = self.sprites_to_use)
        self.update_sprite(loc_in_sprite_sheet, offset_x = 0)

        pp = pprint.PrettyPrinter(indent=1)
        print("\nThe multi-leveled hash for", self.sprites_to_use)
        pp.pprint(self.images)

        self.rect = self.image.get_rect()
        # How big the world is, so we can check for boundries
        self.world_size = (Settings.width, Settings.height)

        # Which collision detection function?
        self.collide_function = pygame.sprite.collide_circle
        self.collisions = []
        # For collision detection, we need to compare our sprite
        # with collideable sprites.  However, we have to remap
        # the collideable sprites coordinates since they change.
        # For performance reasons I created this sprite so we
        # don't have to create more memory each iteration of
        # collision detection.
        self.collider = Drawable()
        self.collider.image = pygame.Surface([Settings.tile_size, Settings.tile_size])
        self.collider.rect = self.collider.image.get_rect()
        # Overlay
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.overlay = self.font.render(
            str(self.health) + "        4 lives", True, (0, 0, 0))

    def move_left(self, time):
        self.collisions = []
        amount = self.delta * time
        self.state = Player_State.WALK
        self.direction = Moving.WEST
        self.image = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA).convert_alpha()
        self.update_self_variables()
        try:
            if self.x - amount < 0:
                raise OffScreenLeftException
            else:
                self.x = self.x - amount
                self.update(0)
                self.frame = (self.frame + 1) % Settings.fps
                self.update_sprite(self.images[self.state][self.direction][self.frame % self.num_animations_to_walk])
                while(len(self.collisions) != 0):
                    self.x = self.x + amount
                    self.update(0)
        except:
            pass

    def move_right(self, time):
        self.collisions = []
        amount = self.delta * time
        self.state = Player_State.WALK
        self.direction = Moving.EAST
        self.image = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA).convert_alpha()
        self.update_self_variables()
        try:
            if self.x + amount > self.world_size[0] - Settings.tile_size:
                raise OffScreenRightException
            else:
                self.x = self.x + amount
                self.update(0)
                self.frame = (self.frame + 1) % Settings.fps
                self.update_sprite(self.images[self.state][self.direction][self.frame % self.num_animations_to_walk])
                while(len(self.collisions) != 0):
                    self.x = self.x - amount
                    self.update(0)
        except:
            pass

    def move_up(self, time):
        self.collisions = []
        amount = self.delta * time
        self.state = Player_State.WALK
        self.direction = Moving.NORTH
        self.image = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA).convert_alpha()
        self.update_self_variables()
        try:
            if self.y - amount < 0:
                raise OffScreenTopException
            else:
                self.y = self.y - amount
                self.update(0)
                self.frame = (self.frame + 1) % Settings.fps
                self.update_sprite(self.images[self.state][self.direction][self.frame % self.num_animations_to_walk])
                if len(self.collisions) != 0:
                    self.y = self.y + amount
                    self.update(0)
                    self.collisions = []
        except:
            pass

    def move_down(self, time):
        self.collisions = []
        amount = self.delta * time
        self.state = Player_State.WALK
        self.direction = Moving.SOUTH
        self.image = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA).convert_alpha()
        self.update_self_variables()
        try:
            if self.y + amount > self.world_size[1] - Settings.tile_size:
                raise OffScreenBottomException
            else:
                self.y = self.y + amount
                self.update(0)
                self.frame = (self.frame + 1) % Settings.fps
                self.update_sprite(self.images[self.state][self.direction][self.frame % self.num_animations_to_walk])
                if len(self.collisions) != 0:
                    self.y = self.y - amount
                    self.update(0)
                    self.collisions = []
        except:
            pass

    def choose_attack(self, time):
        if self.attack_to_animate == 1:
            self.attack_1(time)
        elif self.attack_to_animate == 2:
            self.attack_2(time)
        elif self.attack_to_animate == 3:
            self.attack_3(time)
        elif self.attack_to_animate == 4:
            self.attack_4(time)
        elif self.attack_to_animate == 5:
            self.attack_5(time)

    def attack_1(self, time):

        if self.attack_1_animation < self.num_animations_to_attack_1:
            self.collisions = []
            amount = self.delta * time
            self.state = Player_State.ATTACK_1
            self.image = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA).convert_alpha()
            try:
                self.update(0)
                self.frame = (self.frame + 1) % Settings.fps
                self.update_sprite(self.images[self.state][self.direction][self.attack_1_animation])
                self.attack_1_animation += 1
            except:
                pass
        elif self.attack_1_animation == self.num_animations_to_attack_1:
            self.attack_1_finished = True
            self.attack_1_animation += 1

    def attack_2(self, time):

        if self.attack_2_animation < self.num_animations_to_attack_2:
            self.collisions = []
            amount = self.delta * time
            self.state = Player_State.ATTACK_2
            self.image = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA).convert_alpha()
            try:
                self.update(0)
                self.frame = (self.frame + 1) % Settings.fps
                self.update_sprite(self.images[self.state][self.direction][self.attack_2_animation])
                self.attack_2_animation += 1
            except:
                pass
        elif self.attack_2_animation == self.num_animations_to_attack_2:
            self.attack_2_finished = True
            self.attack_2_animation += 1

    def attack_3(self, time):

        if self.attack_3_animation < self.num_animations_to_attack_3:
            self.collisions = []
            amount = self.delta * time
            self.state = Player_State.ATTACK_3
            self.image = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA).convert_alpha()
            try:
                self.update(0)
                self.frame = (self.frame + 1) % Settings.fps
                self.update_sprite(self.images[self.state][self.direction][self.attack_3_animation])
                self.attack_3_animation += 1
            except:
                pass
        elif self.attack_3_animation == self.num_animations_to_attack_3:
            self.attack_3_finished = True
            self.attack_3_animation += 1

    def attack_4(self, time):

        if self.attack_4_animation < self.num_animations_to_attack_4:
            self.collisions = []
            amount = self.delta * time
            self.state = Player_State.ATTACK_4
            self.image = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA).convert_alpha()
            try:
                self.update(0)
                self.frame = (self.frame + 1) % Settings.fps
                self.update_sprite(self.images[self.state][self.direction][self.attack_4_animation])
                self.attack_4_animation += 1
            except:
                pass
        elif self.attack_4_animation == self.num_animations_to_attack_4:
            self.attack_4_finished = True
            self.attack_4_animation += 1

    def attack_5(self, time):

        if self.has_not_hit_5:
            self.before_x = self.x
            self.before_y = self.y
        if self.attack_5_animation < self.num_animations_to_attack_5:
            self.collisions = []
            amount = self.delta * time
            self.state = Player_State.ATTACK_5
            size = 192
            self.image = pygame.Surface((size, size), pygame.SRCALPHA).convert_alpha()
            try:
                self.x = self.before_x - 85
                self.y = self.before_y - 65
                self.update(0)
                self.frame = (self.frame + 1) % Settings.fps
                self.update_sprite(self.images[self.state][self.direction][self.attack_5_animation], offset_x = -20, rect_size = 64)
                self.attack_5_animation += 1
                self.has_not_hit_5 = False
            except:
                pass
        elif self.attack_5_animation == self.num_animations_to_attack_5:
            self.attack_5_finished = True
            self.attack_5_animation += 1

    def update_self_variables(self):
        self.attack_1_animation = 0
        self.attack_2_animation = 0
        self.attack_3_animation = 0
        self.attack_4_animation = 0
        self.attack_5_animation = 0
        self.attack_1_finished = False
        self.attack_2_finished = False
        self.attack_3_finished = False
        self.attack_4_finished = False
        self.attack_5_finished = False
        if not self.has_not_hit_5:
            self.x = self.before_x
            self.y = self.before_y
            self.has_not_hit_5 = True

    
    def update(self, time):
        self.rect.x = self.x
        self.rect.y = self.y
        self.collisions = []
        for sprite in self.blocks:
            self.collider.rect.x = sprite.x
            self.collider.rect.y = sprite.y
            if pygame.sprite.collide_rect(self, self.collider):
                self.collisions.append(sprite)
