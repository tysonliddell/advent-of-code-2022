from typing import List

from aoc_python.common.utils import get_day_n_input
from aoc_python.d9.rope import get_num_tail_positions
from aoc_python.d9.types import Move


def main():
    data = get_day_n_input(9)
    moves = _parse_moves(data)
    print(get_num_tail_positions(moves))
    print(get_num_tail_positions(moves, number_of_knots=10))


def _parse_moves(data: List[str]) -> List[Move]:
    moves: List[Move] = []
    for line in data:
        dir, steps = line.split(" ")
        move = Move(direction=dir, num_steps=int(steps))
        moves.append(move)
    return moves


main()
