import operator
from typing import List, Tuple, cast

from aoc_python.d9.types import Move, Position


def get_num_tail_positions(moves: List[Move], number_of_knots: int = 2) -> int:
    assert number_of_knots > 1

    head_positions = _get_positions_from_moves(moves)
    for _ in range(number_of_knots - 1):
        head_positions = _get_successor_positions(head_positions)
    return len(set(head_positions))


def _get_successor_positions(head_positions: List[Position]) -> List[Position]:
    tail_pos = head_positions[0]
    tail_positions = [tail_pos]

    for new_head in head_positions[1:]:
        tail_pos = _follow_head_one_step(new_head, tail_pos)
        if tail_pos != tail_positions[-1]:
            tail_positions.append(tail_pos)
    return tail_positions


def _follow_head_one_step(new_head: Position, tail: Position) -> Position:
    if _is_touching(new_head, tail):
        return tail
    return _closest_pos_within_one_step(tail, new_head)


def _is_touching(p1: Position, p2: Position) -> bool:
    x_diff, y_diff = abs(p1[0] - p2[0]), abs(p1[1] - p2[1])
    return max(x_diff, y_diff) <= 1


def _closest_pos_within_one_step(p1: Position, p2: Position) -> Position:
    """Return the closest position, at most a step away from p1, to p2."""
    l1_dist_to_p2 = lambda p: abs(p2[0] - p[0]) + abs(p2[1] - p[1])

    possible_positions = [(p1[0] + x, p1[1] + y) for x in range(-1, 2) for y in range(-1, 2)]
    possible_positions.sort(key=l1_dist_to_p2)
    return possible_positions[0]


MOVE_TO_TRANSLATION = {
    "U": (0, 1),
    "D": (0, -1),
    "L": (-1, 0),
    "R": (1, 0),
}


def _get_positions_from_moves(moves: List[Move]) -> List[Position]:
    pos = (0, 0)
    positions = [pos]

    for move in moves:
        for _ in range(move.num_steps):
            pos = _translate(pos, MOVE_TO_TRANSLATION[move.direction])
            positions.append(pos)
    return positions


def _translate(pos: Position, move_vec: Tuple[int, int]) -> Position:
    return cast(Position, tuple(map(operator.add, pos, move_vec)))


def _debug_print_grid(positions):
    min_x = min(x[0] for x in positions)
    max_x = max(x[0] for x in positions)
    min_y = min(x[1] for x in positions)
    max_y = max(x[1] for x in positions)

    for r in range(max_y, min_y - 1, -1):
        x_vals = set(p[0] for p in positions if p[1] == r)
        for c in range(min_x, max_x + 1):
            print("#" if c in x_vals else " ", end="")
        print("")
