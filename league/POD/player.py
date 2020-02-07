from league import *
import pygame
import league
from enums import *
import pprint
from handle_animations import Handle_Animations
import time

class Player(Character, Handle_Animations):
    """
    This is a sample class for a player object.  A player
    is a character, is a drawable, and an updateable object.
    This class should handle everything a player does, such as
    moving, throwing/shooting, collisions, etc.  It was hastily
    written as a demo but should direction.
    """
    def __init__(self, z=0, x=0, y=0):
        super().__init__(z, x, y)

        # This unit's health
        self.health = 100
        # Last time I was hit
        self.last_hit = pygame.time.get_ticks()
        # A unit-less value. Bigger is faster. Changes player speed
        self.delta = 256
        # Where the player is positioned
        self.x = x
        self.y = y

        # these are the rows on the sprite sheet that correspond with him walking
        self.walk_up_row = 8
        self.walk_left_row = 9
        self.walk_down_row = 10
        self.walk_right_row = 11
        walking_rows = [self.walk_up_row, self.walk_left_row, self.walk_down_row, self.walk_right_row]
        self.num_animations_to_walk = 8

        # these are the rows on the sprite sheet that make him use his first attack
        self.attack_1_up_row = 0
        self.attack_1_left_row = 1
        self.attack_1_down_row = 2
        self.attack_1_right_row = 3
        attacking_rows_1 = [self.attack_1_up_row, self.attack_1_left_row, self.attack_1_down_row, self.attack_1_right_row]
        self.num_animations_to_attack_1 = 7
        self.attack_1_animation = 0

        # these are the rows on the sprite sheet that make him use his second attack
        self.attack_2_up_row = 4
        self.attack_2_left_row = 5
        self.attack_2_down_row = 6
        self.attack_2_right_row = 7
        attacking_rows_2 = [self.attack_2_up_row, self.attack_2_left_row, self.attack_2_down_row, self.attack_2_right_row]
        self.num_animations_to_attack_2 = 8
        self.attack_2_animation = 0

        # these are the rows on the sprite sheet that make him use his third attack
        self.attack_3_up_row = 12
        self.attack_3_left_row = 13
        self.attack_3_down_row = 14
        self.attack_3_right_row = 15
        attacking_rows_3 = [self.attack_3_up_row, self.attack_3_left_row, self.attack_3_down_row, self.attack_3_right_row]
        self.num_animations_to_attack_3 = 6
        self.attack_3_animation = 0

        # these are the rows on the sprite sheet that make him use his fourth attack
        self.attack_4_up_row = 16
        self.attack_4_left_row = 17
        self.attack_4_down_row = 18
        self.attack_4_right_row = 19
        attacking_rows_4 = [self.attack_4_up_row, self.attack_4_left_row, self.attack_4_down_row, self.attack_4_right_row]
        self.num_animations_to_attack_4 = 13
        self.attack_4_animation = 0

        # create animation needed variables
        self.tile_size = league.Settings.tile_size * 2
        self.direction = Direction.SOUTH
        self.state = Player_State.IDLE
        self.images = {}
        self.images[Player_State.WALK] = {}
        self.images[Player_State.ATTACK_1] = {}
        self.images[Player_State.ATTACK_2] = {}
        self.images[Player_State.ATTACK_3] = {}
        self.images[Player_State.ATTACK_4] = {}
        self.frame = 0

        # Load in all of the pictures required for moving. Rather than calling
        # a function for each row, I combined the rows into an array and we simply
        # loop through that array and then call the function to retrieve the
        # necessary pictures.
        for row in walking_rows:
            self.images[Player_State.WALK].update(self.animate_walking(row))

        for row in attacking_rows_1:
            self.images[Player_State.ATTACK_1].update(self.animate_attacking_1(row, self.num_animations_to_attack_1))

        for row in attacking_rows_2:
            self.images[Player_State.ATTACK_2].update(self.animate_attacking_2(row, self.num_animations_to_attack_2))

        for row in attacking_rows_3:
            self.images[Player_State.ATTACK_3].update(self.animate_attacking_3(row, self.num_animations_to_attack_3))

        for row in attacking_rows_4:
            self.images[Player_State.ATTACK_4].update(self.animate_attacking_4(row, self.num_animations_to_attack_4))

        #######################################################################
        # This is how our man spawns in
        # *** All we have to do is change the default path below from "player.png"
        # to any of the other sprite sheets and the inheritance will take care
        # of the rest. ***
        #######################################################################
        loc_in_sprite_sheet = self.pull_sprite(19, 0, file="player.png")
        self.update_sprite(loc_in_sprite_sheet)

        pp = pprint.PrettyPrinter(indent=1)
        print("\nThe multi-leveled hash of our pictures")
        pp.pprint(self.images)

        self.rect = self.image.get_rect()
        # How big the world is, so we can check for boundries
        self.world_size = (Settings.width, Settings.height)
        # What sprites am I not allowd to cross?
        self.blocks = pygame.sprite.Group()
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
        self.font = pygame.font.Font('freesansbold.ttf',32)
        self.overlay = self.font.render(str(self.health) + "        4 lives", True, (0,0,0))

    def move_left(self, time):
        self.collisions = []
        amount = self.delta * time
        self.state = Player_State.WALK
        self.direction = Direction.WEST
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
        self.direction = Direction.EAST
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
        self.direction = Direction.NORTH
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
        self.direction = Direction.SOUTH
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

    def update(self, time):
        self.rect.x = self.x
        self.rect.y = self.y
        self.collisions = []
        for sprite in self.blocks:
            self.collider.rect.x= sprite.x
            self.collider.rect.y = sprite.y
            if pygame.sprite.collide_rect(self, self.collider):
                self.collisions.append(sprite)

    def ouch(self):
        now = pygame.time.get_ticks()
        if now - self.last_hit > 1000:
            self.health = self.health - 10
            self.last_hit = now


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

    def update_self_variables(self):
        self.attack_1_animation = 0
        self.attack_2_animation = 0
        self.attack_3_animation = 0
        self.attack_4_animation = 0
