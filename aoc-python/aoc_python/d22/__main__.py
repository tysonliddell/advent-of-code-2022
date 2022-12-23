from typing import List

from aoc_python.common.utils import get_day_n_input
from aoc_python.d22.map import Board, PositionBounds, follow_cube_path, follow_path, get_password

TEST_DATA = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5""".splitlines()


def main():
    # data = TEST_DATA
    data = get_day_n_input(22)

    moves, board = _parse_map(data)
    position, direction = follow_path(moves, board)
    # board.display()
    print(get_password(position, direction))

    position, direction = follow_cube_path(moves, board)
    # board.display()
    print(get_password(position, direction))


def _parse_map(lines: List[str]):
    board = [line for line in lines if line and not line[0].isalnum()]
    moves = lines[-1].strip()

    # pad rows with trailing whitespace to ensure they are all tbe same length
    board_width = max(len(row) for row in board)
    board = [row.ljust(board_width) for row in board]

    col_bounds = [(len(row) - len(row.lstrip()), len(row.rstrip()) - 1) for row in board]
    row_bounds = []
    for c in range(len(board[0])):
        col = "".join([row[c] for row in board if len(row) > c])
        bounds = (len(col) - len(col.lstrip()), len(col.rstrip()) - 1)
        row_bounds.append(bounds)

    board = [list(row) for row in board]  # type: ignore

    position_bounds: List[List[PositionBounds]] = []
    for r, row in enumerate(board):
        position_bounds.append([])
        for c, col in enumerate(row):
            col_min, col_max = col_bounds[r]
            row_min, row_max = row_bounds[c]
            p = PositionBounds(row=r, col=c, row_min=row_min, row_max=row_max, col_min=col_min, col_max=col_max)
            position_bounds[-1].append(p)

    return moves, Board(tiles=board, bounds=position_bounds)  # type: ignore


main()
