from typing import Tuple

from aoc_python.d8.types import Grid


def get_num_trees_visible(grid: Grid) -> int:
    num_rows = len(grid)
    num_cols = len(grid[0])
    is_visible = [[False for _ in row] for row in grid]

    # left to right
    for row in range(1, num_rows - 1):
        is_visible[row][0] = True
        max_height = grid[row][0]
        for col in range(1, num_cols - 1):
            val = grid[row][col]
            if val > max_height:
                is_visible[row][col] = True
                max_height = val

    # right to left
    for row in range(1, num_rows - 1):
        is_visible[row][-1] = True
        max_height = grid[row][-1]
        for col in range(num_cols - 2, 0, -1):
            val = grid[row][col]
            if val > max_height:
                is_visible[row][col] = True
                max_height = val

    # top to bottom
    for col in range(1, num_cols - 1):
        is_visible[0][col] = True
        max_height = grid[0][col]
        for row in range(1, num_rows - 1):
            val = grid[row][col]
            if val > max_height:
                is_visible[row][col] = True
                max_height = val

    # bottom to top
    for col in range(1, num_cols - 1):
        is_visible[-1][col] = True
        max_height = grid[-1][col]
        for row in range(num_rows - 2, 0, -1):
            val = grid[row][col]
            if val > max_height:
                is_visible[row][col] = True
                max_height = val

    # add 4 for the corners that were missed
    return sum(sum(row) for row in is_visible) + 4


def get_max_scenic_score(grid: Grid) -> int:
    return max(max(row) for row in _get_scenic_scores(grid))


def _get_scenic_scores(grid: Grid) -> Grid:
    scores = [[0 for _ in row] for row in grid]
    num_rows = len(grid)
    num_cols = len(grid[0])

    for row in range(1, num_rows - 1):
        for col in range(1, num_cols - 1):
            scores[row][col] = _get_scenic_score((row, col), grid)
    return scores


def _get_scenic_score(pos: Tuple, grid: Grid) -> int:
    num_rows = len(grid)
    num_cols = len(grid[0])

    row, col = pos
    height = grid[row][col]
    score = 1

    # look down
    for i in range(row + 1, num_rows):
        if grid[i][col] >= height:
            break
    score *= i - row

    # look up
    for i in range(row - 1, -1, -1):
        if grid[i][col] >= height:
            break
    score *= row - i

    # look right
    for i in range(col + 1, num_cols):
        if grid[row][i] >= height:
            break
    score *= i - col

    # look left
    for i in range(col - 1, -1, -1):
        if grid[row][i] >= height:
            break
    score *= col - i

    return score
