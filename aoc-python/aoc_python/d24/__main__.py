from typing import List

from aoc_python.common.utils import get_day_n_input
from aoc_python.d24.path_finder import get_shortest_path_time
from aoc_python.d24.valley import Blizzard, Direction, Valley

TEST_DATA = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#""".splitlines()


def main():
    # data = TEST_DATA
    data = get_day_n_input(24)
    valley = _parse_valley(data)

    # Part 1
    time_of_first_exit = get_shortest_path_time(valley, valley.entry, valley.exit, start_time=0)
    print(time_of_first_exit)

    # Part 2
    time_of_return_for_snacks = get_shortest_path_time(valley, valley.exit, valley.entry, start_time=time_of_first_exit)
    time_of_finish = get_shortest_path_time(valley, valley.entry, valley.exit, start_time=time_of_return_for_snacks)
    print(time_of_finish)


def _parse_valley(data: List[str]):
    valley_height = len(data) - 2
    valley_width = len(data[0]) - 2
    start_pos = (0, data[0].index("."))
    end_pos = (valley_height + 1, data[-1].index("."))

    valley = Valley(width=valley_width, height=valley_height, entry=start_pos, exit=end_pos)
    for r, line in enumerate(data):
        for c, val in enumerate(line):
            pos = (r, c)
            if val == ">":
                valley.initial_blizzards.append(Blizzard(position=pos, direction=Direction.RIGHT))
            elif val == "<":
                valley.initial_blizzards.append(Blizzard(position=pos, direction=Direction.LEFT))
            elif val == "^":
                valley.initial_blizzards.append(Blizzard(position=pos, direction=Direction.UP))
            elif val == "v":
                valley.initial_blizzards.append(Blizzard(position=pos, direction=Direction.DOWN))
    return valley


main()
