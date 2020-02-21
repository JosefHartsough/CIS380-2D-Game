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
        pass

    def update_sprite(self, loc, offset_x = 0, offset_y = 0, rect_size = 64):
        loc_offset = 0
        # add = - loc_offset
        self.image.blit(self.sheet, (0, 0), (loc[0] + offset_x, loc[1] + offset_y, loc[0] + rect_size, loc[1] + rect_size))
        # self.image.blit(self.sheet, (loc_offset, loc_offset), (loc[0] + offset_x  + add, loc[1] + offset_y + add, loc[0] + self.tile_size + add, loc[1] + self.tile_size + add))

    def pull_sprite(self, row, index, max_row_length = 13, num_rows = 20, file = "player.png", image_size = 64):
        # create data structure to hold sprite images and for easier math
        all_sprite_pictures = []
        value_for_rows = 0

        # fill up the array to have multiples of the longest row in the file
        for i in range (0, num_rows):
            all_sprite_pictures.append(value_for_rows)
            value_for_rows += max_row_length

        self.sheet = pygame.image.load(f"./assets/{file}").convert_alpha()
        self.image = pygame.Surface((image_size, image_size), pygame.SRCALPHA).convert_alpha()
        sprite_to_retrieve = all_sprite_pictures[row] + index
        offset_x = self.tile_size * (sprite_to_retrieve  % max_row_length)
        offset_y = self.tile_size * (sprite_to_retrieve  // max_row_length)
        return (offset_x, offset_y)

    def animate_walking(self, row):
        range_of_motion = []
        images = {}
        for x in range(0, self.num_animations_to_walk):
            range_of_motion.append(self.pull_sprite(row, x))
        if row == self.walk_up_row:
            images[Moving.NORTH] = range_of_motion
        elif row == self.walk_left_row:
            images[Moving.WEST] = range_of_motion
        elif row == self.walk_down_row:
            images[Moving.SOUTH] = range_of_motion
        elif row == self.walk_right_row:
            images[Moving.EAST] = range_of_motion

        return images

    def animate_attacking_1(self, row, num_animations):
        range_of_motion = []
        images = {}
        for x in range(0, num_animations):
            range_of_motion.append(self.pull_sprite(row, x))
        if row == self.attack_1_up_row:
            images[Moving.NORTH] = range_of_motion
        elif row == self.attack_1_left_row:
            images[Moving.WEST] = range_of_motion
        elif row == self.attack_1_down_row:
            images[Moving.SOUTH] = range_of_motion
        elif row == self.attack_1_right_row:
            images[Moving.EAST] = range_of_motion

        return images

    def animate_attacking_2(self, row, num_animations):
        range_of_motion = []
        images = {}
        for x in range(0, num_animations):
            range_of_motion.append(self.pull_sprite(row, x))
        if row == self.attack_2_up_row:
            images[Moving.NORTH] = range_of_motion
        elif row == self.attack_2_left_row:
            images[Moving.WEST] = range_of_motion
        elif row == self.attack_2_down_row:
            images[Moving.SOUTH] = range_of_motion
        elif row == self.attack_2_right_row:
            images[Moving.EAST] = range_of_motion

        return images

    def animate_attacking_3(self, row, num_animations):
        range_of_motion = []
        images = {}
        for x in range(0, num_animations):
            range_of_motion.append(self.pull_sprite(row, x))
        if row == self.attack_3_up_row:
            images[Moving.NORTH] = range_of_motion
        elif row == self.attack_3_left_row:
            images[Moving.WEST] = range_of_motion
        elif row == self.attack_3_down_row:
            images[Moving.SOUTH] = range_of_motion
        elif row == self.attack_3_right_row:
            images[Moving.EAST] = range_of_motion

        return images

    def animate_attacking_4(self, row, num_animations):
        range_of_motion = []
        images = {}
        for x in range(0, num_animations):
            range_of_motion.append(self.pull_sprite(row, x))
        if row == self.attack_4_up_row:
            images[Moving.NORTH] = range_of_motion
        elif row == self.attack_4_left_row:
            images[Moving.WEST] = range_of_motion
        elif row == self.attack_4_down_row:
            images[Moving.SOUTH] = range_of_motion
        elif row == self.attack_4_right_row:
            images[Moving.EAST] = range_of_motion

        return images

    def animate_attacking_5(self, row, num_animations):
        range_of_motion = []
        images = {}
        for x in range(0, num_animations):
            range_of_motion.append(self.pull_sprite(row, x * 3 + 0, max_row_length = 24, num_rows=35, image_size = 192))
        if row == self.attack_5_up_row:
            images[Moving.NORTH] = range_of_motion
        elif row == self.attack_5_left_row:
            images[Moving.WEST] = range_of_motion
        elif row == self.attack_5_down_row:
            images[Moving.SOUTH] = range_of_motion
        elif row == self.attack_5_right_row:
            images[Moving.EAST] = range_of_motion

        return images
