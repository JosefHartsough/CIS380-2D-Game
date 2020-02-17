from league import *
import pygame
import league
from enums import *
import pprint
from handle_animations import Handle_Animations
from change_scene import Change_Scene
import time
import sys
from player import Player


class Enemies(Player):

    def __init__(self, sprites_to_use, z=0, x=0, y=0):
        super().__init__(sprites_to_use, z, x, y)

    def check_damage(self, time):
        print("inside damage")
        # print("player direction", Player.direction)
        # player.attack_5(time)
