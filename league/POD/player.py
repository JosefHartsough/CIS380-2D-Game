from league import *
import pygame
import league
from enums import *
import pprint
from handle_animations import Handle_Animations
from change_scene import Change_Scene
import time
import sys


class Player(Character, Handle_Animations, Change_Scene):
    """
    This is a sample class for a player object.  A player
    is a character, is a drawable, and an updateable object.
    This class should handle everything a player does, such as
    moving, throwing/shooting, collisions, etc.  It was hastily
    written as a demo but should direction.
    """

    def __init__(self, sprites_to_use, z=0, x=0, y=0):
        super().__init__(z, x, y)

        # What sprites am I not allowd to cross?
        self.blocks = pygame.sprite.Group()
        # This unit's health
        self.health = 100
        # Last time I was hit
        self.last_hit = pygame.time.get_ticks()
        # A unit-less value. Bigger is faster. Changes player speed
        self.delta = 100
        # Where the player is positioned
        self.x = x
        self.y = y
        self.z = 0


        # Image for the background behing the inventory image
        # TODO: Possibly change this? Just thought it looked cool so i threw that boy in
        # Feel free to change up
        self.inventoryScreenBackground = pygame.image.load('./assets/inventoryScreenBackground.png')

        # Loads all the icons for the items in the inventory
        # Organized like this in the inventory
        # 1-2-3     7-8-9
        # 4-5-6    10-11-12
        self.inventoryBackground = pygame.image.load('./assets/inventory.png')
        self.inventoryBackground = pygame.transform.scale(self.inventoryBackground, (400, 200))

        self.IconOne = pygame.image.load('./assets/ax.png').convert_alpha()
        self.IconOne = pygame.transform.scale(self.IconOne,(64, 64))

        self.IconTwo = pygame.image.load('./assets/bluesword.png').convert_alpha()
        self.IconTwo = pygame.transform.scale(self.IconTwo,(64, 64))

        self.IconThree = pygame.image.load('./assets/bow.png').convert_alpha()
        self.IconThree = pygame.transform.scale(self.IconTwo,(64, 64))

        # images to pull from
        self.sprites_to_use = sprites_to_use

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

        for row in attacking_rows_1:
            self.images[Player_State.ATTACK_1].update(self.animate_attacking_1(row, self.num_animations_to_attack_1))

        for row in attacking_rows_2:
            self.images[Player_State.ATTACK_2].update(self.animate_attacking_2(row, self.num_animations_to_attack_2))
        
        for row in attacking_rows_3:
            self.images[Player_State.ATTACK_3].update(self.animate_attacking_3(row, self.num_animations_to_attack_3))

        for row in attacking_rows_4:
            self.images[Player_State.ATTACK_4].update(self.animate_attacking_4(row, self.num_animations_to_attack_4))

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

    def update(self, time):
        self.rect.x = self.x
        self.rect.y = self.y
        self.collisions = []
        for sprite in self.blocks:
            self.collider.rect.x = sprite.x
            self.collider.rect.y = sprite.y
            if pygame.sprite.collide_rect(self, self.collider):
                self.collisions.append(sprite)

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

    def change_layers(self, time):
        if (self.x > 400 and self.x < 450) and (self.y < 20):
            self.blocks.remove(self.layer_1_lvl_asset.impassable)
            self.blocks.remove(self.layer_2_lvl_asset.impassable)
            self.layer_1_lvl_asset = league.Tilemap(
                './assets/scene2layer1.lvl', self.sprites, layer=1)
            self.layer_2_lvl_asset = league.Tilemap(
                './assets/scene2layer2.lvl', self.sprites, layer=2)
            self.engine.drawables.add(
                self.layer_1_lvl_asset.passable.sprites())
            self.blocks.add(self.layer_1_lvl_asset.impassable)
            self.engine.drawables.add(
                self.layer_2_lvl_asset.passable.sprites())
            self.blocks.add(self.layer_2_lvl_asset.impassable)
            self.x = 200
            self.y = 300
            pygame.display.flip()
        # self.Change_Scene(300, 200, './assets/scene2layer1.lvl', './assets/scene2layer2.lvl')


    def playerInventory(self, time):
    
        screen = pygame.display.set_mode((800, 600))

        # Sets the screen to the background image
        screen.blit(self.inventoryScreenBackground, (0,0))
        screen.blit(self.inventoryBackground, (180, 140))

        # Variables for x and y coords for the selector
        x = 189
        y = 145

        # Variable for the dimension sizes of the interactive boxes
        interactiveBoxDimensionsX = 40
        interactiveBoxDimensionsY = 40

        self.npcCollisionCheck = True

        clock = pygame.time.Clock()

        # RGB values for grey
        grey = (96, 96, 96)

        # Creates all the interactive rectangles. I made these so i can control when the user click on our image
        # Creates them for the Npc inventory and the players inventory
        # TODO:Add all the dialog options
        # TODO:Need to fix formatting slightly, not sure why they got messsed up
        interactiveIconOne = pygame.Rect(190, 160, interactiveBoxDimensionsX, interactiveBoxDimensionsY)
        interactiveIconTwo = pygame.Rect(260, 160, interactiveBoxDimensionsX, interactiveBoxDimensionsY)
        interactiveIconThree = pygame.Rect(320, 160, interactiveBoxDimensionsX, interactiveBoxDimensionsY)
      
        myInventory = pygame.Rect(600, 125, 30, 30)
        dialogOptions = pygame.Rect(375, 425, 30, 30)

        # Creates an array that holds all the possible choices for user
        # TODO:Add the remaining choices
        options = [myInventory, dialogOptions, interactiveIconOne, interactiveIconTwo, interactiveIconThree]

        # Selector. Going to change this to an image...whenever i figure out how the fuck to do that
        # Currently having it spawn in the top left of the screen
        selector = pygame.Rect(185, 145, 10, 10)

        # Checks if the player has collided with the NPC
        # Sets the movement for the selector
        # TODO:Add functionality for the mouse and not the keyboard for cursor movement
        while self.npcCollisionCheck:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.npcCollisionCheck = True

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_w] and y > 0:
                y -= 5
            if pressed[pygame.K_s] and y < 600 - 60:
                y += 5
            if pressed[pygame.K_a] and x > 0:
                x -= 5
            if pressed[pygame.K_d] and x < 800 - 60:
                x += 5

            # Selector x and y
            selector.x, selector.y = x, y

            #screen.fill((0, 0, 0))

            # Color for the selector
            color = (0, 128, 255)

            # Draws all the rects that are our interactive box
            # IMPORTANT:Make sure all of the interactive boxes
            # are drawn before the selector and icon images
            # otherwise they will overlap.
            pygame.draw.rect(screen, grey, interactiveIconOne)
            pygame.draw.rect(screen, grey, interactiveIconTwo)
            pygame.draw.rect(screen, grey, interactiveIconThree) 
            #pygame.draw.rect(screen, grey, dialogOptions)
            pygame.draw.rect(screen, grey, myInventory)

            # Blits all the images of the item icons on the the respective spots
            # TODO: Maybe make this cleaner if we have time? nahhh im lazy who cares
            screen.blit(self.IconOne, (185, 145))
            screen.blit(self.IconTwo, (240, 145))
            screen.blit(self.IconThree, (300, 145))
            

            # Font for when printing text
            # TODO:Will be used in the future for dialog and text in general in menu
            # Will be adding more fonts for different things
            font = pygame.font.SysFont("monospace", 25)

            # # Text for NPC Inventory
            # npcInventory = font.render("NPC INVENTORY", 1, (255, 255, 255))
            # screen.blit(npcInventory, (185, 100))
            # Text for Player Iventory
            playerInventory = font.render("PLAYER INVENTORY", 1, (255, 255, 255))
            screen.blit(playerInventory, (220, 100))

            # Draws our selector
            pygame.draw.rect(screen, color, selector)


            # Check to see if the user presses the enter key
            # TODO:Make it so it is all clicking interactions from the mouse
            if pressed[pygame.K_RETURN]:
                # Check to see if the selection rect
                # collides with any other rect
                for rect in options:
                    # Add rects as needed
                    if selector.colliderect(rect):
                        if rect == interactiveIconOne:
                            print('interact1!')
                        elif rect == interactiveIconTwo:
                            print('2')
                        elif rect == interactiveIconThree:
                            print('3')
                        elif rect == myInventory:
                        
                            self.npcCollisionCheck = True

            pygame.display.flip()
            clock.tick(60)
 