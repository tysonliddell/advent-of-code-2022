from typing import List, cast

from aoc_python.common.utils import get_day_n_input
from aoc_python.d4.overlap import get_fully_contained_count, get_overlap_count
from aoc_python.d4.types import RangePair


def main():
    data = get_day_n_input(4)
    range_pairs = _parse_range_pairs(data)
    print(get_fully_contained_count(range_pairs))
    print(get_overlap_count(range_pairs))


def _parse_range_pairs(data: List[str]) -> List[RangePair]:
    return [_parse_range_pair(d) for d in data]


def _parse_range_pair(s: str) -> RangePair:
    pair = s.split(",")
    result = tuple(tuple(int(x) for x in p.split("-")) for p in pair)
    return cast(RangePair, result)


main()
