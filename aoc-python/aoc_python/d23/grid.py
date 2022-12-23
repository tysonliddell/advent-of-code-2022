from typing import Set

from aoc_python.d23.types import Position


def get_rectangle_size_from_positions(positions: Set[Position], include_edge_border=True):
    top_left = min(p[0] for p in positions), min(p[1] for p in positions)
    bottom_right = max(p[0] for p in positions), max(p[1] for p in positions)
    rect_height = abs(top_left[0] - bottom_right[0]) + bool(include_edge_border)
    rect_width = abs(top_left[1] - bottom_right[1]) + bool(include_edge_border)
    return rect_height * rect_width


def print_grid_from_positions(positions: Set[Position], include_edge_border=True):
    min_row, min_col = min(p[0] for p in positions), min(p[1] for p in positions)
    max_row, max_col = max(p[0] for p in positions), max(p[1] for p in positions)
    offset_positions = set((p[0] - min_row, p[1] - min_col) for p in positions)

    grid = []
    for r in range(max_row + bool(include_edge_border) + 1):
        row = []
        for c in range(max_col + bool(include_edge_border) + 1):
            row.append("#" if (r, c) in offset_positions else ".")
        grid.append(row)

    for row in grid:
        print("".join(row))
