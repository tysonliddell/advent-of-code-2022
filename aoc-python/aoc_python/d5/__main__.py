from typing import List, cast

from aoc_python.common.utils import get_day_n_input
from aoc_python.d5.stacks import clone_stacks, do_moves, get_top_stack_values
from aoc_python.d5.types import Move, Stack


def main():
    data = get_day_n_input(5)
    stacks = _parse_stacks(data)
    moves = _parse_moves(data)

    cloned_stacks = clone_stacks(stacks)
    do_moves(cloned_stacks, moves)
    print(get_top_stack_values(cloned_stacks))

    do_moves(stacks, moves, is_9001=True)
    print(get_top_stack_values(stacks))


def _parse_stacks(data: List[str]) -> List[Stack]:
    for i in range(len(data)):
        line = data[i]
        if line.startswith(" 1 "):
            break

    stack_init_data = data[:i]
    del data[: i + 1]

    num_stacks = (len(stack_init_data[0]) + 1) // 4
    stacks: List[Stack] = [[] for _ in range(num_stacks)]
    for line in stack_init_data[::-1]:
        for i in range(num_stacks):
            stack_level_value = line[i * 4 : (i + 1) * 4][1]
            if stack_level_value != " ":
                stacks[i].append(stack_level_value)

    return stacks


def _parse_moves(data: List[str]) -> List[Move]:
    moves = []
    for d in data:
        if not d:
            continue
        tokens = d.split(" ")
        move = (int(tokens[1]), int(tokens[3]) - 1, int(tokens[5]) - 1)
        moves.append(cast(Move, move))
    return moves


main()
