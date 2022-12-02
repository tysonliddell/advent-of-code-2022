from aoc_python.common.utils import get_day_n_input
from aoc_python.d1.max_cals import get_most_cals, get_top_three_cals


def main():
    calorie_list = [int(cal) if cal else None for cal in get_day_n_input(1)]
    print(f"PART1: {get_most_cals(calorie_list)}")
    print(f"PART2: {get_top_three_cals(calorie_list)}")


main()
