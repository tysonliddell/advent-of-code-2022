from enum import Enum
from typing import List, Tuple

Grid = List[List[str]]
Position = Tuple[int, int]


class Direction(Enum):
    NORTH = 0
    SOUTH = 1
    WEST = 2
    EAST = 3
