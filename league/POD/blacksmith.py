# Class for non playable characters NPC
# We can use this as a base class to develop other NPCs

from league import *
import pygame
from handle_animations import *
import league


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
        self.direction = Direction.WEST
        self.state = Player_State.IDLE
        self.images = {}
        self.frame = 0

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

    # This function is when the player comes close to our blacksmith NPC
    # He will display a menu with text for the ability to buy and seel weapons/armor

    # Class that handles all the dialog for the blacksmith and player
    # def dialog(self):
     #   dialogBox = Font.render()

    def dialog(self, ):
        screen = pygame.display.set_mode((800, 600))

        # Image for the background behing the inventory image
        # TODO: Possibly change this? Just thought it looked cool so i threw that boy in
        # Feel free to change up 
        inventoryScreenBackground = pygame.image.load('./assets/inventoryScreenBackground.png')

        # Sets the screen to the background image
        screen.blit(inventoryScreenBackground, (0,0))

        # Variables for x and y coords for the selector
        x = 189
        y = 145

        # Variable for the dimension sizes of the interactive boxes
        interactiveBoxDimensionsX=50
        interactiveBoxDimensionsY = 50

        # Checks to see if collision has happened with player
        # Still having a bug that it opens when starting the game
        npcCollisionCheck = False
        
        clock = pygame.time.Clock()

        # RGB values for grey
        grey = (96, 96, 96)

        # Creates all the interactive rectangles. I made these so i can control when the user click on our image
        # Creates them for the Npc inventory and the players inventory
        # TODO:Add all the dialog options
        interactiveIconOne = pygame.Rect(185, 145, interactiveBoxDimensionsX, interactiveBoxDimensionsY)
        interactiveIconTwo = pygame.Rect(240, 145, interactiveBoxDimensionsX, interactiveBoxDimensionsY)
        interactiveIconThree = pygame.Rect(300, 145, interactiveBoxDimensionsX, interactiveBoxDimensionsY)
        interactiveIconFour = pygame.Rect(185, 210, interactiveBoxDimensionsX, interactiveBoxDimensionsY)
        interactiveIconFive = pygame.Rect(240, 205, interactiveBoxDimensionsX, interactiveBoxDimensionsY)
        interactiveIconSix = pygame.Rect(300, 205, interactiveBoxDimensionsX, interactiveBoxDimensionsY)
        interactiveIconSeven = pygame.Rect(390, 145, interactiveBoxDimensionsX, interactiveBoxDimensionsY)
        interactiveIconEight = pygame.Rect(460, 145, interactiveBoxDimensionsX, interactiveBoxDimensionsY)
        interactiveIconNine = pygame.Rect(510, 145, interactiveBoxDimensionsX, interactiveBoxDimensionsY)
        interactiveIconTen = pygame.Rect(400, 205, interactiveBoxDimensionsX, interactiveBoxDimensionsY)
        interactiveIconEleven = pygame.Rect(460, 205, interactiveBoxDimensionsX, interactiveBoxDimensionsY)
        interactiveIconTwelve = pygame.Rect(520, 205, interactiveBoxDimensionsX, interactiveBoxDimensionsY)

        myInventory = pygame.Rect(600, 125, 30, 30)
        dialogOptions = pygame.Rect(375, 425, 30, 30)

        # Creates an array that holds all the possible choices for user
        # TODO:Add the remaining choices
        options = [myInventory, dialogOptions, interactiveIconOne, interactiveIconTwo, interactiveIconThree, interactiveIconFour,
        interactiveIconFive, interactiveIconSix, interactiveIconSeven, interactiveIconEight, interactiveIconNine, interactiveIconTen,
        interactiveIconEleven, interactiveIconTwelve,]

        # Selector. Going to change this to an image...whenever i figure out how the fuck to do that
        # Currently having it spawn in the top left of the screen
        selector = pygame.Rect(185, 145, 10, 10)
        
        # Checks if the player has collided with the NPC
        # Sets the movement for the selector
        # TODO:Add functionality for the mouse and not the keyboard for cursor movement
        while not npcCollisionCheck:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    npcCollisionCheck = True

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
            pygame.draw.rect(screen, grey, interactiveIconFour)
            pygame.draw.rect(screen, grey, interactiveIconFive)
            pygame.draw.rect(screen, grey, interactiveIconSix)
            pygame.draw.rect(screen, grey, interactiveIconSeven)
            pygame.draw.rect(screen, grey, interactiveIconEight)
            pygame.draw.rect(screen, grey, interactiveIconNine)
            pygame.draw.rect(screen, grey, interactiveIconTen)
            pygame.draw.rect(screen, grey, interactiveIconEleven)
            pygame.draw.rect(screen, grey, interactiveIconTwelve)
                    
            pygame.draw.rect(screen, grey, dialogOptions)


            # Organized like this in the inventory
            # 1-2-3     7-8-9
            # 4-5-6    10-11-12     
            inventoryBackground = pygame.image.load('./assets/inventory.png')
            inventoryBackground = pygame.transform.scale(inventoryBackground, (400, 200))
            screen.blit(inventoryBackground, (180, 140))

            IconOne = pygame.image.load('./assets/zombie.png').convert_alpha()
            IconOne = pygame.transform.scale(IconOne,(64, 64))
            screen.blit(IconOne, (185, 145))

            IconTwo = pygame.image.load('./assets/zombie.png').convert_alpha()
            IconTwo = pygame.transform.scale(IconTwo,(64, 64))
            screen.blit(IconTwo, (240, 145))

            IconThree = pygame.image.load('./assets/zombie.png').convert_alpha()
            IconThree = pygame.transform.scale(IconTwo,(64, 64))
            screen.blit(IconThree, (300, 145))

            IconFour = pygame.image.load('./assets/zombie.png').convert_alpha()
            IconFour = pygame.transform.scale(IconTwo,(64, 64))
            screen.blit(IconFour, (185, 210))

            IconFive = pygame.image.load('./assets/zombie.png').convert_alpha()
            IconFive = pygame.transform.scale(IconTwo,(64, 64))
            screen.blit(IconFive, (240, 205))

            IconSix = pygame.image.load('./assets/zombie.png').convert_alpha()
            IconSix = pygame.transform.scale(IconTwo,(64, 64))
            screen.blit(IconSix, (300, 205))

            IconSeven = pygame.image.load('./assets/zombie.png').convert_alpha()
            IconSeven = pygame.transform.scale(IconSeven,(64, 64))
            screen.blit(IconSeven, (390, 145))

            IconEight = pygame.image.load('./assets/zombie.png').convert_alpha()
            IconEight = pygame.transform.scale(IconEight,(64, 64))
            screen.blit(IconEight, (460, 145))

            IconNine = pygame.image.load('./assets/zombie.png').convert_alpha()
            IconNine = pygame.transform.scale(IconNine,(64, 64))
            screen.blit(IconNine, (510, 145))

            IconTen = pygame.image.load('./assets/zombie.png').convert_alpha()
            IconTen = pygame.transform.scale(IconTen,(64, 64))
            screen.blit(IconTen, (400, 205))

            IconEleven = pygame.image.load('./assets/zombie.png').convert_alpha()
            IconEleven = pygame.transform.scale(IconEleven,(64, 64))
            screen.blit(IconEleven, (460, 205))

            IconTwelve = pygame.image.load('./assets/zombie.png').convert_alpha()
            IconTwelve = pygame.transform.scale(IconTwelve,(64, 64))
            screen.blit(IconTwelve, (520, 205))
            
            # Font for when printing text
            # TODO:Will be used in the future for dialog and text in general in menu
            # Will be adding more fonts for different things
            font = pygame.font.SysFont("monospace", 25)
        
            npcInventory = font.render("NPC INVENTORY", 1, (255, 255, 255))
            screen.blit(npcInventory, (185, 100))

            playerInventory = font.render("PLAYER INVENTORY", 1, (255, 255, 255))
            screen.blit(playerInventory, (390, 100))

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
                        elif rect == interactiveIconFour:
                            print('4')
                        elif rect == interactiveIconFive:
                            print('5')
                        elif rect == interactiveIconSix:
                            print('6')
                        elif rect == interactiveIconSeven:
                            print('7')
                        elif rect == interactiveIconEight:
                            print('8')
                        elif rect == interactiveIconNine:
                            print('9')
                        elif rect == interactiveIconTen:
                            print('10')
                        elif rect == interactiveIconEleven:
                            print('11')
                        elif rect == interactiveIconTwelve:
                            print('12')                             
                        elif rect == myInventory:
                            print('playerInv')
                        elif rect == dialogOptions:
                            # Quit!
                            npcCollisionCheck = True

            pygame.display.flip()
            clock.tick(60)

