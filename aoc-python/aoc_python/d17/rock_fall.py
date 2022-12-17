from typing import Generator, List, Tuple

Position = Tuple[int, int]
Rock = List[str]
Grid = List[List[str]]

JetIterator = Generator[str, None, None]


ROCKS = [
    #################
    """
####
""".strip().splitlines(),
    #################
    """
.#.
###
.#.
""".strip().splitlines(),
    #################
    """
..#
..#
###
""".strip().splitlines(),
    #################
    """
#
#
#
#
""".strip().splitlines(),
    #################
    """
##
##
""".strip().splitlines(),
]

# Reverse the rocks vertically so they agree with our coordinate system.
# We want lower values of `y` to appear nearer to the bottom. y=0 is sitting
# on the floor.
ROCKS = [list(reversed(r)) for r in ROCKS]


def simulate(jet_sequence: str, num_rocks: int = 2022):
    dropper = _iter_drop(jet_sequence)
    final_top = next(top for i, top in enumerate(dropper) if i + 1 == num_rocks)
    return final_top


def get_height_change_sequence(jet_sequence: str, seq_length: int):
    dropper = _iter_drop(jet_sequence)
    height_change_sequence: List[int] = []

    prev_height = 0
    for i, height in enumerate(dropper):
        if i == seq_length:
            return height_change_sequence
        height_change_sequence.append(height - prev_height)
        prev_height = height


def _iter_drop(jet_sequence: str):
    top = 0
    it_jet = iter_jet(jet_sequence)
    it_rock = iter_rock()

    grid = [["." for _ in range(7)] for _ in range(10000000)]

    while True:
        rock = next(it_rock)
        _, rock_rest_y = drop_rock(it_jet, rock, grid, top)
        top = max(top, rock_rest_y + len(rock))
        yield top


def _draw(grid):
    for row in reversed(grid[0:20]):
        print(row)


def drop_rock(iter_jet: JetIterator, rock: Rock, grid: Grid, top: int) -> Position:
    old_x, old_y = 2, top + 3
    while True:
        x, y = move_rock((old_x, old_y), rock, next(iter_jet), grid)
        if y == old_y:
            break
        old_x, old_y = x, y
    blit_grid(grid, rock, (x, y))
    return (x, y)


def blit_grid(grid: Grid, rock: Rock, pos: Position):
    x, y = pos
    for row in range(len(rock)):
        for col in range(len(rock[0])):
            if rock[row][col] == "#":
                grid[y + row][x + col] = rock[row][col]


def move_rock(pos: Position, rock: Rock, jet: str, grid: Grid) -> Position:
    x, y = pos
    if jet == "<" and not is_collision((x - 1, y), rock, grid):
        x -= 1
    elif jet == ">" and not is_collision((x + 1, y), rock, grid):
        x += 1

    if not is_collision((x, y - 1), rock, grid):
        y -= 1

    return x, y


def is_collision(pos: Position, rock: Rock, grid: Grid) -> bool:
    x, y = pos
    if y < 0:
        return True

    rock_width = len(rock[0])
    rock_height = len(rock)
    for r in range(rock_height):
        for c in range(rock_width):
            if rock[r][c] != "#":
                continue
            if x + c < 0 or x + c > 6:
                return True
            pos_x, pos_y = x + c, y + r
            if grid[pos_y][pos_x] != ".":
                return True
    return False


def iter_jet(jet_seq: str):
    while True:
        for c in jet_seq:
            yield c


def iter_rock():
    while True:
        for r in ROCKS:
            yield r
