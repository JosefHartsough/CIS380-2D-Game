import pygame
import sys
sys.path.append('..')
import league
from player import Player
from overlay import Overlay
from blacksmith import Npc
from alchemist import NpcAlchemist
from armorer import NpcArmor
from turns import Turns
from enemy import Enemy
from operator import itemgetter

def main():
    engine = league.Engine("Path of Darkness")
    engine.init_pygame()

    # Load the assets
    sprites = league.Spritesheet('./assets/sprite1.png', league.Settings.tile_size, 32)
   # sprites1=league.Spritesheet('./assets/beach_tileset.png', league.Settings.tile_size, 16)
    world_lvl_asset = league.Tilemap('./assets/world.lvl', sprites, layer = 0)
    layer_1_lvl_asset = league.Tilemap('./assets/layer1.lvl', sprites, layer = 1)
    layer_2_lvl_asset = league.Tilemap('./assets/layer2.lvl', sprites, layer = 2)
   # water_lvl_asset = league.Tilemap('./assets/layer3.lvl', sprites1, layer = 1)

    # set the world size
    world_size = (world_lvl_asset.wide*league.Settings.tile_size, world_lvl_asset.high *league.Settings.tile_size)

    # Tell the engine about the assets created
    engine.drawables.add(world_lvl_asset.passable.sprites())
    engine.drawables.add(layer_1_lvl_asset.passable.sprites())
    engine.drawables.add(layer_2_lvl_asset.passable.sprites())
  #  engine.drawables.add(water_lvl_asset.passable.sprites())

    # Create the player and give him a position and overlay
    player = Player("playerBase.png", 3, 400, 250)
    player_overlay = Overlay(player)


              
    # create an enemy to figure out how to do damage. Using the player since he
    # has all of the attacks and abilities I do
    enemy = Enemy("naked_man_with_long_sword.png", 3, 400, 400, attack_to_animate = 1, health = 100, damage = 10)
    enemy_2 = Enemy("ork.png", 3, 500, 500, attack_to_animate = 2, health = 200, damage = 100)
    skeletonOne = Enemy("skeleton.png", 4, 1500, 1800, attack_to_animate = 1, health=100, damage=10 )
    skeletonTwo = Enemy("skeleton.png", 4, 1500, 1800, attack_to_animate = 1, health=100, damage=10 )
    skeletonThree = Enemy("skeleton.png", 4, 1500, 1800, attack_to_animate =1 , health=100, damage=10 )
    skeletonFour = Enemy("skeleton.png", 4, 1500, 1800, attack_to_animate = 1, health=100, damage=10 )
    skeletonFive = Enemy("skeleton.png", 4, 1500, 1800, attack_to_animate = 1, health=100, damage=10 )
    dragonBoss = Enemy("dragon.png", 1, 400, 400, attack_to_animate = 1, health=100, damage=10 )

    # Creates all our Npcs  
    npcBlacksmith = Npc(2, 100, 500)                    #Blacksmith
    npcAlchemist = NpcAlchemist(200, 600, 120)          #Alchemist
    npcArmorer = NpcArmor(200, 700, 400)                #Armor

    # Array of our enemies
    enemies = [enemy, enemy_2, skeletonOne, skeletonTwo, skeletonThree, skeletonFour, skeletonFive, dragonBoss]

    # Array of our NPCs
    npcList = [npcBlacksmith, npcAlchemist, npcArmorer]

    
    for i in enemies:
      i.blocks.add(world_lvl_asset.impassable)
      i.blocks.add(layer_1_lvl_asset.impassable)
      i.blocks.add(layer_2_lvl_asset.impassable)
      i.world_size = world_size
      i.rect = i.image.get_rect()

    player.blocks.add(world_lvl_asset.impassable)
    player.blocks.add(layer_1_lvl_asset.impassable)
    player.blocks.add(layer_2_lvl_asset.impassable)
    
    
  
    player.world_size = world_size
    player.rect = player.image.get_rect()
       

    # Adds the player, enemies, and NPCs to the game
    engine.objects.append(player)
    engine.drawables.add(player)
    engine.objects.extend(enemies)
    engine.drawables.add(enemies)
    engine.objects.extend(npcList)
    engine.drawables.add(npcList)
  
   
    # interface for the turn system
    turns = Turns(player, enemies, engine)

    # create the camera and add it to the engine
    camera = league.LessDumbCamera(800, 600, player, engine.drawables, world_size)
    # camera = league.DumbCamera(800, 600, player, engine.drawables, world_size)
    engine.objects.append(camera)
    engine.objects.append(player_overlay)

    # look for different events in the game and call their methods
    # engine.collisions[player] = (q, player.ouch)
    # engine.collisions[player] = (npcBlacksmith, npcBlacksmith.dialog)
    # engine.collisions[player] = (npcAlchemist, npcAlchemist.dialog)
    # engine.collisions[player] = (npcArmorer, npcArmorer.dialog)
    pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // league.Settings.gameTimeFactor)
    engine.key_events[pygame.K_a] = turns.move_left
    engine.key_events[pygame.K_d] = turns.move_right
    engine.key_events[pygame.K_w] = turns.move_up
    engine.key_events[pygame.K_s] = turns.move_down

    engine.key_events[pygame.K_1] = turns.attack_1
    engine.key_events[pygame.K_2] = turns.attack_2
    engine.key_events[pygame.K_3] = turns.attack_3
    engine.key_events[pygame.K_4] = turns.attack_4
    engine.key_events[pygame.K_5] = turns.attack_5

    engine.key_events[pygame.K_i] = player.playerInventory

    engine.key_events[pygame.K_m] = player.change_layers
    # Need to add when near each vendor, e opens the inventory menu
    # rangeX = range(100, 120)
    # if (player.x == rangeX):
    #     engine.key_events[pygame.K_e] = npcBlacksmith.dialog

    # engine.events[pygame.USEREVENT + 1] = q.move_right
    engine.events[pygame.QUIT] = engine.stop

    engine.run()


if __name__ == '__main__':
    main()
