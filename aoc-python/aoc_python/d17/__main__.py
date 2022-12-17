from aoc_python.common.utils import get_day_n_input
from aoc_python.d17.pattern import solve_part_2
from aoc_python.d17.rock_fall import simulate

TEST_DATA = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>""".splitlines()


def main():
    # data = TEST_DATA
    data = get_day_n_input(17)
    jet_sequence = data[0]

    print(simulate(jet_sequence))

    # Uncomment these lines to derive the hardcoded sequence needed for Part 2.
    # from aoc_python.d17.rock_fall import get_height_change_sequence
    # print(get_height_change_sequence(jet_sequence, 5000))

    print(solve_part_2())


main()
