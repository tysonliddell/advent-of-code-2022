from typing import Generator, List, Tuple

Cave = List[List[str]]
Point = Tuple[int, int]


def pour_sand(source: Point, cave: Cave) -> int:
    sand_unit_count = 0
    source_x, source_y = source
    while True:
        if cave[source_y][source_x] == "o":
            break

        *_, last_pos = _iter_drop_sand_path(source, cave)
        x, y = last_pos
        if y + 1 == len(cave):
            # fell into void
            break

        cave[y][x] = "o"
        sand_unit_count += 1
    return sand_unit_count


def _iter_drop_sand_path(pos: Point, cave: Cave) -> Generator[Point, None, None]:
    yield pos
    while True:
        x, y = pos
        if y + 1 == len(cave):
            # fell into void
            break
        elif cave[y + 1][x] == ".":
            pos = (x, y + 1)
        elif cave[y + 1][x - 1] == ".":
            pos = (x - 1, y + 1)
        elif cave[y + 1][x + 1] == ".":
            pos = (x + 1, y + 1)
        else:
            # unit of sand came to rest
            break
        yield pos
