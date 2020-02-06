from league import *
import pygame
import league
from enums import *
import pprint

class Player(Character):
    """This is a sample class for a player object.  A player
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
        # A unit-less value.  Bigger is faster. Changes player speed
        self.delta = 256
        # Where the player is positioned
        self.x = x
        self.y = y

        # these are the rows on the spire sheet that correspond with him walking
        self.up_walk_const = 8
        self.left_walk_const = 9
        self.down_walk_const = 10
        self.right_walk_const = 11

        # create animation needed variables
        self.tile_size = league.Settings.tile_size * 2
        self.direction = Direction.WEST
        self.state = Player_State.IDLE
        self.images = {}
        self.frame = 0

        # Load in all of the pictures required for moving
        # The animate functions return a hash and so the first call to self.images
        # needs to create the hash on this side to allow for it. The other calls
        # to the animate functions simply need to add onto the hash and in python
        # that is done by the update() method.
        self.images[Player_State.WALK] = self.animate_move_left()
        self.images[Player_State.WALK].update(self.animate_move_right())
        self.images[Player_State.WALK].update(self.animate_move_up())
        self.images[Player_State.WALK].update(self.animate_move_down())

        # This is how our man spawns in.
        loc_in_sprite_sheet = self.pull_sprite(2, 0)
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

    def animate_move_left(self):
        range_of_motion = []
        images = {}
        for x in range(0, 8):
            range_of_motion.append(self.pull_sprite(self.left_walk_const, x))
        images[Direction.WEST] = range_of_motion
        return images

    def animate_move_right(self):
        range_of_motion = []
        images = {}
        for x in range(0, 8):
            range_of_motion.append(self.pull_sprite(self.right_walk_const, x))
        images[Direction.EAST] = range_of_motion
        return images

    def animate_move_up(self):
        range_of_motion = []
        images = {}
        for x in range(0, 8):
            range_of_motion.append(self.pull_sprite(self.up_walk_const, x))
        images[Direction.NORTH] = range_of_motion
        return images

    def animate_move_down(self):
        range_of_motion = []
        images = {}
        for x in range(0, 8):
            range_of_motion.append(self.pull_sprite(self.down_walk_const, x))
        images[Direction.SOUTH] = range_of_motion
        return images

    def move_left(self, time):
        self.collisions = []
        amount = self.delta * time
        self.state = Player_State.WALK
        self.direction = Direction.WEST
        self.image = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA).convert_alpha()
        try:
            if self.x - amount < 0:
                raise OffScreenLeftException
            else:
                self.x = self.x - amount
                self.update(0)
                self.frame = (self.frame + 1) % Settings.fps
                self.update_sprite(self.images[self.state][self.direction][self.frame % 8])
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
        try:
            if self.x + amount > self.world_size[0] - Settings.tile_size:
                raise OffScreenRightException
            else:
                self.x = self.x + amount
                self.update(0)
                self.frame = (self.frame + 1) % Settings.fps
                self.update_sprite(self.images[self.state][self.direction][self.frame % 8])
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
        try:
            if self.y - amount < 0:
                raise OffScreenTopException
            else:
                self.y = self.y - amount
                self.update(0)
                self.frame = (self.frame + 1) % Settings.fps
                self.update_sprite(self.images[self.state][self.direction][self.frame % 8])
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
        try:
            if self.y + amount > self.world_size[1] - Settings.tile_size:
                raise OffScreenBottomException
            else:
                self.y = self.y + amount
                self.update(0)
                self.frame = (self.frame + 1) % Settings.fps
                self.update_sprite(self.images[self.state][self.direction][self.frame % 8])
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

    def update_sprite(self, loc):
        # pygame.display.update()
        self.image.blit(self.sheet, (0, 0), (loc[0], loc[1], loc[0] + self.tile_size, loc[1] + self.tile_size))

    def pull_sprite(self, row, index, max_row_length = 13, num_rows = 20, file = "player.png"):
        # create data structure to hold sprite images and for easier math
        all_sprite_pictures = []
        value_for_rows = 0

        # fill up the array to have multiples of the longest row in the file
        for i in range (0, num_rows):
            all_sprite_pictures.append(value_for_rows)
            value_for_rows += max_row_length
        self.sheet = pygame.image.load(f"./assets/{file}").convert_alpha()
        self.image = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA).convert_alpha()
        sprite_to_retrieve = all_sprite_pictures[row] + index
        offset_x = self.tile_size * (sprite_to_retrieve  % max_row_length)
        offset_y = self.tile_size * (sprite_to_retrieve  // max_row_length)
        return (offset_x, offset_y)
