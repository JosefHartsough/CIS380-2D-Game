from league import *
import pygame
import league
from enums import *
import pprint

class Change_Scene():
    """
        This class is meant to make changing scenes much easier in order to 
        speed up our map creation. 
    """
  
    def __init__(self, nx, ny, layer1, layer2):

        self.layer_1_lvl_asset = league.Tilemap(layer1, self.sprites, layer=1)
        self.layer_2_lvl_asset = league.Tilemap(layer2, self.sprites, layer=2)
        self.engine.drawables.add(self.layer_2_lvl_asset.passable.sprites())
        self.blocks.add(self.layer_2_lvl_asset.impassable)
        self.x = nx
        self.y = ny

