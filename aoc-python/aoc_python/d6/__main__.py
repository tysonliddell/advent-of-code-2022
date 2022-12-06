from aoc_python.common.utils import get_day_n_input
from aoc_python.d6.decode import find_marker


def main():
    data = get_day_n_input(6)[0]
    print(find_marker(data)[1])
    print(find_marker(data, marker_length=14)[1])


main()
