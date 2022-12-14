from typing import List, cast

from aoc_python.common.utils import get_day_n_input
from aoc_python.d14.cave import Cave, Point, pour_sand

MAX_X = 1000

SAND_SOURCE_POINT = (500, 0)


def main():
    data = get_day_n_input(14)

    # PART 1
    cave = _parse_cave(data)
    count = pour_sand(SAND_SOURCE_POINT, cave)
    print(count)

    # PART 2
    cave = _parse_cave(data, with_floor=True)
    count = pour_sand(SAND_SOURCE_POINT, cave)
    print(count)


def _parse_cave(data: List[str], with_floor=False) -> Cave:
    rock_paths = [_parse_rock_path(line) for line in data]
    max_y = max([y for path in rock_paths for _, y in path])

    cave = [["." for _ in range(MAX_X + 1)] for _ in range(max_y + 1)]
    for path in rock_paths:
        for x, y in path:
            cave[y][x] = "#"

    if with_floor:
        cave.append(["." for _ in range(MAX_X + 1)])
        cave.append(["#" for _ in range(MAX_X + 1)])

    return cave


def _parse_rock_path(line: str) -> List[Point]:
    nodes: List[Point] = []
    for p in line.split(" -> "):
        point = tuple(int(v) for v in p.split(","))
        nodes.append(cast(Point, point))

    points: List[Point] = []
    for p1, p2 in zip(nodes, nodes[1:]):
        line_path = _get_line_path(p1, p2)
        points.extend(line_path)
    return points


def _get_line_path(p1: Point, p2: Point) -> List[Point]:
    if p2 < p1:
        p1, p2 = p2, p1

    x1, y1, x2, y2 = (*p1, *p2)
    if x2 != x1:
        return [(x, y1) for x in range(x1, x2 + 1)]
    return [(x1, y) for y in range(y1, y2 + 1)]


main()
