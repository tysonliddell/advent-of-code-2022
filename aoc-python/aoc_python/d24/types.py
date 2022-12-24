from enum import Enum
from typing import Tuple

Position = Tuple[int, int]


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    def position_delta(self) -> Position:
        match self:
            case Direction.UP:
                return (-1, 0)
            case Direction.DOWN:
                return (1, 0)
            case Direction.LEFT:
                return (0, -1)
            case Direction.RIGHT:
                return (0, 1)

    def __str__(self):
        match self:
            case Direction.UP:
                return "^"
            case Direction.DOWN:
                return "v"
            case Direction.LEFT:
                return "<"
            case Direction.RIGHT:
                return ">"
