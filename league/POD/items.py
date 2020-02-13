from league import *
import pygame
from handle_animations import *
import league
import array as arr
import POD.player
import os
import sys
from pathlib import Path
from functools import partial


class Items(self):

    file = Path(__file__).parent
    # Dictionary that holds all the icons for the items
    ItemIcons = {}

    for picture in os.listdir(os.path.join(file, "./assets")):
        try:
            ItemIcons.update({picture: pygame.image.load(
                os.path.join(file, 'assets', picture)).convert()})
        except:
            pass
    itemTuple = ((ItemIcons['vampire.png'], ItemIcons['vampire.png'],
              ItemIcons['vampire.png'], ItemIcons['vampire.png']))

    weaponTuple = ((ItemIcons['vamprie.png'], ItemIcons['vampire.png'],
                ItemIcons['vampire.png'], ItemIcons['vampire.png']))

    armorTuple = ((ItemIcons['vampireUp.png'], ItemIcons['vampireRight.png'],
               ItemIcons['vampire.png'], ItemIcons['vampireLeft.png']))
