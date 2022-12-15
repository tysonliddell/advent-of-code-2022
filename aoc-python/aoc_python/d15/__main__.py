from typing import Generator, List

from aoc_python.common.utils import get_day_n_input
from aoc_python.d15.sensors import Position, Sensor, get_num_empty_positions_in_row, get_position_of_last_beacon

ROW = 2000000

TEST_DATA = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3""".splitlines()


def main():
    data = get_day_n_input(15)
    # data = TEST_DATA
    sensors = list(_iter_sensors(data))

    # Part 1
    print(get_num_empty_positions_in_row(sensors, ROW))

    # Part 2
    pos = get_position_of_last_beacon(sensors)
    print(pos.x * 4000000 + pos.y)


def _iter_sensors(data: List[str]) -> Generator[Sensor, None, None]:
    for line in data:
        tokens = line.replace(",", "").replace(":", "").split(" ")
        sensor_x, sensor_y = int(tokens[2].split("=")[1]), int(tokens[3].split("=")[1])
        sensor = Position(x=sensor_x, y=sensor_y)

        beacon_x, beacon_y = int(tokens[8].split("=")[1]), int(tokens[9].split("=")[1])
        beacon = Position(x=beacon_x, y=beacon_y)
        yield Sensor(sensor=sensor, beacon=beacon)


main()
