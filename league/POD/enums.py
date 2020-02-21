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
    ATTACK_5 = 6


from enum import IntEnum
class Moving(IntEnum):
    """Direction is an enumeration of the cardinal directions.
    Enumerated counter-clockwise.
    """
    NORTH = 8
    NORTH_WEST = 1
    WEST = 9
    SOUTH_WEST = 3
    SOUTH = 10
    SOUTH_EAST = 5
    EAST = 11
    NORTH_EAST = 7

from enum import IntEnum
class Attack_Damage(IntEnum):
    """
    These are the values for each attack
    """
    FIRST_ATTACK = 1000
    SECOND_ATTACK = 50
    THIRD_ATTACK = 30
    FOURTH_ATTACK = 10
    FIFTH_ATTACK = 2500
