from typing import Set

from aoc_python.d24.valley import Position, Valley


def get_shortest_path_time(valley: Valley, start: Position, end: Position, start_time: int = 0) -> int:
    valid_positions = {start}

    i = start_time
    while end not in valid_positions:
        i += 1
        _, blizzard_positions_next = valley.get_state(i)
        valid_positions = _grow_boundary(valid_positions, valley)
        valid_positions -= blizzard_positions_next
    return i


def _grow_boundary(positions: Set[Position], valley: Valley):
    new_positions = positions.copy()
    for pos in positions:
        new_positions.update(valley.get_pos_neighbours(pos))
    return new_positions
