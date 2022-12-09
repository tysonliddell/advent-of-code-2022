from dataclasses import dataclass
from typing import Tuple


@dataclass
class Move:
    direction: str
    num_steps: int


Position = Tuple[int, int]
