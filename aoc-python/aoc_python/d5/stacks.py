from typing import List

from aoc_python.d5.types import Move, Stack


def do_moves(stacks: List[Stack], moves: List[Move], is_9001: bool = False):
    for move in moves:
        _do_move(stacks, move, is_9001=is_9001)


def get_top_stack_values(stacks: List[Stack]) -> str:
    return "".join(s[-1] for s in stacks)


def clone_stacks(stacks: List[Stack]) -> List[Stack]:
    return [s.copy() for s in stacks]


def _do_move(stacks: List[Stack], move: Move, is_9001: bool = False):
    num_to_move, from_stack_i, to_stack_i = move
    from_stack, to_stack = (stacks[from_stack_i], stacks[to_stack_i])

    if is_9001:
        values = from_stack[-num_to_move:]
        del from_stack[-num_to_move:]
        to_stack.extend(values)
    else:
        for _ in range(num_to_move):
            to_stack.append(from_stack.pop())
