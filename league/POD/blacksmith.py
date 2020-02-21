# Class for non playable characters NPC
# We can use this as a base class to develop other NPCs

from league import *
import pygame
from handle_animations import *
import league
import array as arr


class Npc(Character, Handle_Animations):

    def __init__(self, z=0, x=0, y=0):
        super().__init__(z, x, y)

        engine = league.Engine("engine")
        # Health for NPC
        self.health = 100

        # Bool for if possible to ckill the NPC
        self.isKillable = False

        # X and Y for position
        self.npcX = x
        self.npcY = y

        self.tile_size = league.Settings.tile_size * 2
        self.direction = Moving.WEST
        self.state = Player_State.IDLE
        self.images = {}
        self.frame = 0

        # Checks to see if collision has happened with player
        # Still having a bug that it opens when starting the game
        self.npcCollisionCheck = False

        loc_in_sprite_sheet = self.pull_sprite(2, 1, file="ork.png")
        self.update_sprite(loc_in_sprite_sheet)

        # Need to add location for NPC Sprite
        # self.image = pygame.image.load('./assets/sword_ninja_left.png').convert_alpha()
        # self.image  = pygame.transform.scale(self.image, (64,64))
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
        self.collider.image = pygame.Surface(
            [Settings.tile_size, Settings.tile_size])
        self.collider.rect = self.collider.image.get_rect()

    # def nPCText(self):
    #     """
    #     A function to hold all of the text that the NPC will say
    #     and can respond with
    #     """

    # This function will hold all the inventory that the blacksmith has to offer

    def update(self, time):
        self.rect.x = self.x
        self.rect.y = self.y
        self.collisions = []
        for sprite in self.blocks:
            self.collider.rect.x = sprite.x
            self.collider.rect.y = sprite.y
            if pygame.sprite.collide_rect(self, self.collider):
                self.collisions.append(sprite)

    def update_picture(self, image):
        self.image = pygame.image.load(f'./assets/{image}').convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))

