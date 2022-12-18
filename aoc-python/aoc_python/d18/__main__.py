from aoc_python.common.utils import get_day_n_input
from aoc_python.d18.droplet import calculate_internal_surface_area, calculate_surface_area

TEST_DATA = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5""".splitlines()


def main():
    # data = TEST_DATA
    data = get_day_n_input(18)

    droplets = set(tuple(int(i) for i in line.split(",")) for line in data)
    surface_area = calculate_surface_area(droplets)
    print(surface_area)

    internal_surface_area = calculate_internal_surface_area(droplets)
    print(internal_surface_area)


main()
