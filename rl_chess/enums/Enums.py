from enum import Enum


class Color(Enum):
    BLACK = 0,
    WHITE = 1


class MoveDirection(Enum):
    UP = 0,
    DOWN = 1,
    LEFT = 2,
    RIGHT = 3,
    UP_LEFT = 4,
    UP_RIGHT = 5,
    DOWN_LEFT = 6,
    DOWN_RIGHT = 7,
    ONE_O_CLOCK = 8,
    TWO_O_CLOCK = 9,
    FOUR_O_CLOCK = 10,
    FIVE_O_CLOCK = 11,
    SEVEN_O_CLOCK = 12,
    EIGHT_O_CLOCK = 13,
    TEN_O_CLOCK = 14,
    ELEVEN_O_CLOCK = 15
