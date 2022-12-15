from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Position:
    x: int
    y: int

    def l1_dist_to(self, other: "Position") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __hash__(self) -> int:
        return (self.x, self.y).__hash__()


@dataclass
class Sensor:
    sensor: Position
    beacon: Position


def get_position_of_last_beacon(sensors: List[Sensor]) -> Position:
    for row in range(0, 4000001):
        if row % 100000 == 0:
            print(f"Checked {row} rows.")
        empty_intervals = get_empty_intervals_in_row(sensors, row)
        if len(empty_intervals) > 1:
            return Position(x=empty_intervals[0][1] + 1, y=row)

    raise RuntimeError("How did you get here?")


def get_empty_intervals_in_row(sensors: List[Sensor], row_num: int) -> List[Tuple[int, int]]:
    intervals: List[Tuple[int, int]] = []

    for sensor in sensors:
        dist_to_beacon = sensor.sensor.l1_dist_to(sensor.beacon)
        x = sensor.sensor.x
        d_remaining = dist_to_beacon - sensor.sensor.l1_dist_to(Position(x=x, y=row_num))
        if d_remaining >= 0:
            intervals.append((x - d_remaining, x + d_remaining))

    # merge intervals
    intervals.sort()
    res = [intervals[0]]
    for i in intervals[1:]:
        if i[0] <= res[-1][1]:
            res[-1] = (res[-1][0], max(i[1], res[-1][1]))
        else:
            res.append(i)

    return res


def get_num_empty_positions_in_row(sensors: List[Sensor], row_num: int) -> int:
    beacons_on_row = {s.beacon for s in sensors if s.beacon.y == row_num}
    empty_intervals = get_empty_intervals_in_row(sensors, row_num)
    return sum(x2 - x1 + 1 for x1, x2 in empty_intervals) - len(beacons_on_row)
