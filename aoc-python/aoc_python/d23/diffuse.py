from collections import Counter
from typing import List, Set

from aoc_python.d23.types import Direction, Position

DIRECTIONS_ORDER = [Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST]


def iter_diffusion(positions: Set[Position]):
    directions = DIRECTIONS_ORDER.copy()

    while True:
        positions_before = positions.copy()
        _diffuse(positions, directions)
        if positions_before == positions:
            break
        yield
        directions.append(directions.pop(0))


def _diffuse(positions: Set[Position], direction_order: List[Direction]):
    moves = {}
    proposals: Counter[Position] = Counter()
    for pos in positions:
        neighbours = _get_neighbours(pos)
        if not (neighbours & positions):
            # all neighbours empty, don't move
            continue
        for dir in direction_order:
            new_pos = _get_empty_neighbour_or_none(pos, dir, positions)
            if new_pos:
                moves[pos] = new_pos
                proposals[new_pos] += 1
                break
    for start, end in moves.items():
        if proposals[end] == 1:
            positions.remove(start)
            positions.add(end)


def _get_empty_neighbour_or_none(pos: Position, dir: Direction, occupied: Set[Position]):
    unoccupied_neighbours = _get_neighbours(pos) - occupied
    if dir == Direction.NORTH:
        return add_positions(pos, (-1, 0)) if len([p for p in unoccupied_neighbours if p[0] < pos[0]]) == 3 else None
    if dir == Direction.SOUTH:
        return add_positions(pos, (1, 0)) if len([p for p in unoccupied_neighbours if p[0] > pos[0]]) == 3 else None
    if dir == Direction.EAST:
        return add_positions(pos, (0, 1)) if len([p for p in unoccupied_neighbours if p[1] > pos[1]]) == 3 else None
    if dir == Direction.WEST:
        return add_positions(pos, (0, -1)) if len([p for p in unoccupied_neighbours if p[1] < pos[1]]) == 3 else None


def _get_neighbours(pos: Position):
    """Get coordinates of all 8 neighbours a position."""
    return set(add_positions(pos, (row, col)) for row in range(-1, 2) for col in range(-1, 2)) - {pos}


def add_positions(p1: Position, p2: Position):
    return tuple(sum(x) for x in zip(p1, p2))
