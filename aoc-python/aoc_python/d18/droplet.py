from itertools import product
from typing import Generator, List, Sequence, Set, Tuple

Position = Tuple[int, int, int]
Droplet = Set[Position]


def calculate_surface_area(mini_cubes=Sequence[Position]):
    droplet_map = {}
    for c in mini_cubes:
        adjacent_coords = _get_adjacent_coords(c)
        droplet_map[c] = [c, 6]
        for adj in [a for a in adjacent_coords if a in droplet_map]:
            droplet_map[c][1] -= 1
            droplet_map[adj][1] -= 1
    return sum(d[1] for d in droplet_map.values())


def calculate_internal_surface_area(droplet: Droplet):
    internal_components = _get_internal_components(droplet)
    internal_surface_area = sum(calculate_surface_area(c) for c in internal_components)
    return calculate_surface_area(droplet) - internal_surface_area


def _get_internal_components(droplet: Droplet):
    """
    Take a bounding box volume around a droplet, subtract the droplet volume
    and return the components internal to the droplet (each component that does
    not touch the boundary of the box)
    """
    box = _get_bounding_box(droplet)
    min_x, min_y, min_z = box[0]
    max_x, max_y, max_z = box[1]
    box_remaining = set(_iter_box(box)) - droplet

    internal_componenets = []
    while box_remaining:
        # grab an element in the volume remaining and traverse the component
        # it belongs to
        component = []
        is_internal_component = True
        stack = []
        stack.append(box_remaining.pop())
        while stack:
            pos = stack.pop()
            component.append(pos)

            x, y, z = pos
            if x in (min_x, max_x) or y in (min_y, max_y) or z in (min_z, max_z):
                is_internal_component = False

            adjacent = [p for p in _get_adjacent_coords(pos) if p in box_remaining]
            stack.extend(adjacent)
            box_remaining -= set(adjacent)
        if is_internal_component:
            internal_componenets.append(component)
    return internal_componenets


def _get_adjacent_coords(pos: Position) -> List[Position]:
    offset = (-1, 0, 1)
    x, y, z = pos
    neighbours = [(x + dx, y + dy, z + dz) for dx, dy, dz in product(offset, offset, offset)]
    return [p for p in neighbours if _l1_dist(p, pos) == 1]


def _get_bounding_box(droplet: Droplet):
    min_x = min(p[0] for p in droplet)
    min_y = min(p[1] for p in droplet)
    min_z = min(p[2] for p in droplet)
    corner1 = (min_x, min_y, min_z)

    max_x = max(p[0] for p in droplet)
    max_y = max(p[1] for p in droplet)
    max_z = max(p[2] for p in droplet)
    corner2 = (max_x, max_y, max_z)
    return (corner1, corner2)


def _iter_box(box: Tuple[Position, Position]) -> Generator[Position, None, None]:
    for x in range(box[0][0], box[1][0] + 1):
        for y in range(box[0][1], box[1][1] + 1):
            for z in range(box[0][2], box[1][2] + 1):
                yield (x, y, z)


def _l1_dist(p1: Position, p2: Position):
    return sum(abs(p1[i] - p2[i]) for i in range(len(p1)))
