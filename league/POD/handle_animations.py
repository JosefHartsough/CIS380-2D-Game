from league import *
import pygame
import league
from enums import *
import pprint

class Handle_Animations:
    """
    This class is made so that all of the other sprites can inherit it to allow
    for easy animation.
    """

    def __init__(self):
        self.up_walk_const = 8
        self.left_walk_const = 9
        self.down_walk_const = 10
        self.right_walk_const = 11

        self.tile_size = league.Settings.tile_size * 2

    def animate_move_left(self):
        range_of_motion = []
        images = {}
        for x in range(0, 8):
            range_of_motion.append(self.pull_sprite(self.left_walk_const, x))
        images[Direction.WEST] = range_of_motion
        return images

    def animate_move_right(self):
        range_of_motion = []
        images = {}
        for x in range(0, 8):
            range_of_motion.append(self.pull_sprite(self.right_walk_const, x))
        images[Direction.EAST] = range_of_motion
        return images

    def animate_move_up(self):
        range_of_motion = []
        images = {}
        for x in range(0, 8):
            range_of_motion.append(self.pull_sprite(self.up_walk_const, x))
        images[Direction.NORTH] = range_of_motion
        return images

    def animate_move_down(self):
        range_of_motion = []
        images = {}
        for x in range(0, 8):
            range_of_motion.append(self.pull_sprite(self.down_walk_const, x))
        images[Direction.SOUTH] = range_of_motion
        return images

    def update_sprite(self, loc):
        # pygame.display.update()
        self.image.blit(self.sheet, (0, 0), (loc[0], loc[1], loc[0] + self.tile_size, loc[1] + self.tile_size))

    def pull_sprite(self, row, index, max_row_length = 13, num_rows = 20, file = "player.png"):
        # create data structure to hold sprite images and for easier math
        all_sprite_pictures = []
        value_for_rows = 0

        # fill up the array to have multiples of the longest row in the file
        for i in range (0, num_rows):
            all_sprite_pictures.append(value_for_rows)
            value_for_rows += max_row_length
        self.sheet = pygame.image.load(f"./assets/{file}").convert_alpha()
        self.image = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA).convert_alpha()
        sprite_to_retrieve = all_sprite_pictures[row] + index
        offset_x = self.tile_size * (sprite_to_retrieve  % max_row_length)
        offset_y = self.tile_size * (sprite_to_retrieve  // max_row_length)
        return (offset_x, offset_y)
