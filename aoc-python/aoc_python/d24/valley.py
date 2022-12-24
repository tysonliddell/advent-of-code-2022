from dataclasses import dataclass, field
from functools import cache
from typing import List, Set, Tuple

from aoc_python.d24.types import Direction, Position


@dataclass
class Blizzard:
    position: Position
    direction: Direction

    def move(self):
        delta = self.direction.position_delta()
        self.position = (self.position[0] + delta[0], self.position[1] + delta[1])


@dataclass
class Valley:
    width: int
    height: int
    entry: Position
    exit: Position
    initial_blizzards: List[Blizzard] = field(default_factory=list)

    def __hash__(self) -> int:
        # DIRTY HACK for @cache, since we only ever have one instance of a valley object.
        return 0

    @cache
    def get_state(self, time_mins: int) -> Tuple[List[Blizzard], Set[Position]]:
        if time_mins == 0:
            return self.initial_blizzards, set([bliz.position for bliz in self.initial_blizzards])
        else:
            blizzards, _ = self.get_state(time_mins - 1)
            new_blizzards = blizzards.copy()

            self._move_blizzards(new_blizzards)
            return new_blizzards, set([bliz.position for bliz in new_blizzards])

    def get_pos_neighbours(self, pos: Position):
        neighbours = set()
        for delta in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nbr = pos[0] + delta[0], pos[1] + delta[1]
            if nbr in [self.entry, self.exit]:
                neighbours.add(nbr)
            elif 0 < nbr[0] <= self.height and 0 < nbr[1] <= self.width:
                neighbours.add(nbr)
        return neighbours

    def _move_blizzards(self, blizzards: List[Blizzard]):
        for bliz in blizzards:
            bliz.move()
            pos = bliz.position
            if bliz.position[0] == 0:
                bliz.position = (self.height, pos[1])
            elif bliz.position[0] == self.height + 1:
                bliz.position = (1, pos[1])
            elif bliz.position[1] == 0:
                bliz.position = (pos[0], self.width)
            elif bliz.position[1] == self.width + 1:
                bliz.position = (pos[0], 1)

    def draw_valley(self, time_mins: int):
        blizzards, positions = self.get_state(time_mins)
        for r in range(self.height + 2):
            for c in range(self.width + 2):
                if (r, c) not in positions:
                    print(".", end="")
                else:
                    blizs_at_pos = [b for b in blizzards if b.position == (r, c)]
                    if len(blizs_at_pos) > 1:
                        print(len(blizs_at_pos), end="")
                    else:
                        print(str(blizs_at_pos[0].direction), end="")
            print()
