from collections import defaultdict
from math import inf
from typing import Dict, List, Tuple

Grid = List[List[int]]
Position = Tuple[int, int]


def shortest_path_length(grid: Grid, start: Position, end: Position) -> float:
    visited = set()
    to_visit = set([start])
    distances: Dict[Position, float] = defaultdict(lambda: inf)
    distances[start] = 0

    pos = start
    while pos != end:
        visited.add(pos)
        to_visit.remove(pos)

        neigbour_dist = distances[pos] + 1
        for n in _get_reachable_neighbours(grid, pos):
            distances[n] = min(distances[n], neigbour_dist)
            if n not in visited:
                to_visit.add(n)
        possible_next_positions = sorted([p for p in to_visit], key=lambda p: distances[p])
        if not possible_next_positions:
            break  # path not found
        pos = possible_next_positions[0]

    return distances[end]


def get_positions_with_elevation(grid: Grid, elev: int) -> List[Position]:
    positions = []
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == elev:
                positions.append((r, c))
    return positions


def _get_reachable_neighbours(grid, pos) -> List[Position]:
    r, c = pos
    max_r, max_c = len(grid), len(grid[0])
    neighbours = [
        (row, col)
        for row, col in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
        if 0 <= row < max_r and 0 <= col < max_c
    ]
    return [(row, col) for (row, col) in neighbours if grid[row][col] - grid[r][c] <= 1]
