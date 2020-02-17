import pygame
import sys
sys.path.append('..')
import league
from player import Player
from overlay import Overlay
from blacksmith import Npc
from alchemist import NpcAlchemist
from armorer import NpcArmor
from enemies import Enemies

def main():
    engine = league.Engine("Path of Darkness")
    engine.init_pygame()

    # Load the assets
    sprites = league.Spritesheet('./assets/sprite1.png', league.Settings.tile_size, 32)
    world_lvl_asset = league.Tilemap('./assets/world.lvl', sprites, layer = 0)
    layer_1_lvl_asset = league.Tilemap('./assets/layer1.lvl', sprites, layer = 1)
    layer_2_lvl_asset = league.Tilemap('./assets/layer2.lvl', sprites, layer = 2)

    # set the world size
    world_size = (world_lvl_asset.wide*league.Settings.tile_size, world_lvl_asset.high *league.Settings.tile_size)

    # Tell the engine about the assets created
    engine.drawables.add(world_lvl_asset.passable.sprites())
    engine.drawables.add(layer_1_lvl_asset.passable.sprites())
    engine.drawables.add(layer_2_lvl_asset.passable.sprites())

    # Create the player and give him a position and overlay
    player = Player("girl_big.png", 3, 400, 300)
    player_overlay = Overlay(player)

    # create an enemy to figure out how to do damage. Using the player since he
    # has all of the attacks and abilities I do
    enemy = Enemies("naked_man_with_long_sword.png", 3, 400, 400)
    # Create npcBlacksmith and give position
    npcBlacksmith = Npc(2, 100, 500)

    # Create npcAlchemist and give position
    npcAlchemist = NpcAlchemist(200, 600, 120)

    # Create npcArmorer and give position
    npcArmorer = NpcArmor(200, 700, 400)

    # The assets the player can not go through
    player.blocks.add(world_lvl_asset.impassable)
    player.blocks.add(layer_1_lvl_asset.impassable)
    player.blocks.add(layer_2_lvl_asset.impassable)
    enemy.blocks.add(world_lvl_asset.impassable)
    enemy.blocks.add(layer_1_lvl_asset.impassable)
    enemy.blocks.add(layer_2_lvl_asset.impassable)

    # Set sizing options for the player
    player.world_size = world_size
    player.rect = player.image.get_rect()
    enemy.world_size = world_size
    enemy.rect = enemy.image.get_rect()

    # Add the player to the engine
    engine.objects.append(player)
    engine.drawables.add(player)
    engine.objects.append(enemy)
    engine.drawables.add(enemy)
    # engine.drawables.add(player_overlay)

    # Add the NPCs to the engine
    # engine.objects.append(npcBlacksmith)
    engine.objects.append(npcBlacksmith)
    engine.drawables.add(npcBlacksmith)
    engine.objects.append(npcAlchemist)
    engine.drawables.add(npcAlchemist)
    engine.objects.append(npcArmorer)
    engine.drawables.add(npcArmorer)

    # create the camera and add it to the engine
    camera = league.LessDumbCamera(800, 600, player, engine.drawables, world_size)
    # camera = league.DumbCamera(800, 600, player, engine.drawables, world_size)
    engine.objects.append(camera)
    # engine.objects.append(player_overlay)

    # look for different events in the game and call their methods
    # engine.collisions[player] = (q, player.ouch)
    # engine.collisions[player] = (npcBlacksmith, npcBlacksmith.dialog)
    # engine.collisions[player] = (npcAlchemist, npcAlchemist.dialog)
    # engine.collisions[player] = (npcArmorer, npcArmorer.dialog)
    pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // league.Settings.gameTimeFactor)
    engine.key_events[pygame.K_a] = player.move_left
    engine.key_events[pygame.K_d] = player.move_right
    engine.key_events[pygame.K_w] = player.move_up
    engine.key_events[pygame.K_s] = player.move_down
    engine.key_events[pygame.K_1] = player.attack_1
    engine.key_events[pygame.K_2] = player.attack_2
    engine.key_events[pygame.K_3] = player.attack_3
    engine.key_events[pygame.K_4] = player.attack_4
    engine.key_events[pygame.K_5] = player.attack_5
    engine.key_events[pygame.K_6] = enemy.check_damage

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
