from typing import List, Optional

from aoc_python.d4.types import Range, RangePair


def get_fully_contained_count(range_pairs: List[RangePair]) -> int:
    return len([pair for pair in range_pairs if _is_redundant(pair)])


def get_overlap_count(range_pairs: List[RangePair]) -> int:
    return len([pair for pair in range_pairs if _get_intersection(pair)])


def _get_intersection(pair: RangePair) -> Optional[Range]:
    intersection = (max(pair[0][0], pair[1][0]), min(pair[0][1], pair[1][1]))
    return None if intersection[0] > intersection[1] else intersection


def _is_redundant(pair: RangePair) -> bool:
    """Returns True if one of the ranges in the pair is redundant."""
    intersection = _get_intersection(pair)
    return intersection in pair
