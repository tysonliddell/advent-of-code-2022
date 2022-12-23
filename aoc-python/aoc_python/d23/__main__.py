from typing import List, Set

from aoc_python.common.utils import get_day_n_input
from aoc_python.d23.diffuse import iter_diffusion
from aoc_python.d23.grid import get_rectangle_size_from_positions
from aoc_python.d23.types import Position

# from aoc_python.d23.grid import print_grid_from_positions

TEST_DATA = """..............
..............
.......#......
.....###.#....
...#...#.#....
....#...##....
...#.###......
...##.#.##....
....#..#......
..............
..............
..............""".splitlines()


def main():
    # data = TEST_DATA
    data = get_day_n_input(23)

    # Part 1
    positions = _get_positions_from_data(data)
    diffuser = iter_diffusion(positions)
    for _ in range(10):
        next(diffuser)
    print(get_rectangle_size_from_positions(positions) - len(positions))

    # Part 2
    positions = _get_positions_from_data(data)
    diffuser = iter_diffusion(positions)
    diffusion_count = 0
    while True:
        # print_grid_from_positions(positions)
        try:
            next(diffuser)
            diffusion_count += 1
        except StopIteration:
            break
    print(diffusion_count + 1)


def _get_positions_from_data(data: List[str]) -> Set[Position]:
    return set((r, c) for r, row in enumerate(data) for c, val in enumerate(row) if val == "#")


main()
