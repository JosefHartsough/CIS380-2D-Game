from enum import IntEnum
class Player_State(IntEnum):
    """State is an enumeration of common states a character might
    be in.
    """
    IDLE = 0
    WALK = 1
    ATTACK_1 = 2
    ATTACK_2 = 3
    ATTACK_3 = 4
    ATTACK_4 = 5

from enum import IntEnum
class Moving(IntEnum):
    """Direction is an enumeration of the cardinal directions.
    Enumerated counter-clockwise.
    """
    NORTH = 0
    NORTH_WEST = 1
    WEST = 2
    SOUTH_WEST = 3
    SOUTH = 4
    SOUTH_EAST = 5
    EAST = 6
    NORTH_EAST = 7
