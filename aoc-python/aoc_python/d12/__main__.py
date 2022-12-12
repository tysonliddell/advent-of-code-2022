from typing import List, Tuple

from aoc_python.common.utils import get_day_n_input
from aoc_python.d12.grid import Grid, Position, get_positions_with_elevation, shortest_path_length


def main():
    data = get_day_n_input(12)
    grid, start, end = _parse_grid(data)

    # Part 1
    shortest_path_from_start = shortest_path_length(grid, start, end)
    print(shortest_path_from_start)

    # Part 2
    start_positions = get_positions_with_elevation(grid, ord("a"))
    path_lengths = [shortest_path_length(grid, pos, end) for pos in start_positions]
    path_lengths.sort()
    return print(path_lengths[0])


def _parse_grid(data: List[str]) -> Tuple[Grid, Position, Position]:
    grid = [[ord(c) for c in line] for line in data]
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if chr(val) == "S":
                start = (r, c)
                grid[r][c] = ord("a")
            elif chr(val) == "E":
                end = (r, c)
                grid[r][c] = ord("z")

    return (grid, start, end)


main()
