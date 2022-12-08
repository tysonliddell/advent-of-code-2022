from aoc_python.common.utils import get_day_n_input
from aoc_python.d8.grid import get_max_scenic_score, get_num_trees_visible


def main():
    data = get_day_n_input(8)
    grid = [[int(x) for x in line] for line in data]
    print(get_num_trees_visible(grid))
    print(get_max_scenic_score(grid))


main()
