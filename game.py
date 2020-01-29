import pygame
import sys
sys.path.append('..')
import league


def main():
    e = league.Engine("Path of Darkness")
    e.init_pygame()

    sprites = league.Spritesheet('./assets/tileset1.png', league.Settings.tile_size, 32)
    t = league.Tilemap('./assets/world.lvl', sprites, layer = 0)
    b = league.Tilemap('./assets/background.lvl', sprites, layer = 1)
    s = league.Tilemap('./assets/layer2.lvl', sprites, layer = 2)
    world_size = (t.wide*league.Settings.tile_size, t.high *league.Settings.tile_size)
    e.drawables.add(t.passable.sprites())
    e.drawables.add(b.passable.sprites())
    e.drawables.add(s.passable.sprites())
