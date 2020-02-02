import pygame
import sys
sys.path.append('..')
import league
from player import Player
from overlay import Overlay


def main():
    e = league.Engine("Path of Darkness")
    e.init_pygame()

    sprites = league.Spritesheet('./assets/sprite1.png', league.Settings.tile_size, 32)
    t = league.Tilemap('./assets/world.lvl', sprites, layer = 0)
    b = league.Tilemap('./assets/background.lvl', sprites, layer = 1)
    s = league.Tilemap('./assets/layer2.lvl', sprites, layer = 2)
    world_size = (t.wide*league.Settings.tile_size, t.high *league.Settings.tile_size)
    e.drawables.add(t.passable.sprites())
    e.drawables.add(b.passable.sprites())
    e.drawables.add(s.passable.sprites())

    # ira's code
    p = Player(2, 400, 300)
    o = Overlay(p)
    p.blocks.add(t.impassable)
    p.world_size = world_size
    p.rect = p.image.get_rect()
    q = Player(10, 100, 100)
    q.image = p.image
    e.objects.append(p)
    e.objects.append(q)
    e.drawables.add(p)
    e.drawables.add(q)
    e.drawables.add(o)
    c = league.LessDumbCamera(800, 600, p, e.drawables, world_size)
    #c = league.DumbCamera(800, 600, p, e.drawables, world_size)

    e.objects.append(c)
    e.objects.append(o)

    e.collisions[p] = (q, p.ouch)
    pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // league.Settings.gameTimeFactor)
    e.key_events[pygame.K_a] = p.move_left
    e.key_events[pygame.K_d] = p.move_right
    e.key_events[pygame.K_w] = p.move_up
    e.key_events[pygame.K_s] = p.move_down
    e.events[pygame.USEREVENT + 1] = q.move_right
    e.events[pygame.QUIT] = e.stop


    e.run()

if __name__ =='__main__':
    main()
