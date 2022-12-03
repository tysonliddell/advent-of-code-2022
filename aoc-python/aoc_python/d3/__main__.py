from typing import Generator, List, Tuple

from aoc_python.common.utils import get_day_n_input
from aoc_python.d3.items import get_priority_sum_of_intersections


def main():
    data = get_day_n_input(3)
    print(get_priority_sum_of_intersections(_iter_rucksack_compartments(data)))
    print(get_priority_sum_of_intersections(_iter_groups(data)))


def _iter_rucksack_compartments(
    rucksacks: List[str],
) -> Generator[Tuple[str, str], None, None]:
    """Iterate over each rucksack, breaking each down into two compartments"""
    for rucksack in rucksacks:
        compartment_1 = rucksack[: len(rucksack) // 2]
        compartment_2 = rucksack[len(rucksack) // 2 :]
        yield (compartment_1, compartment_2)


def _iter_groups(rucksacks: List[str]) -> Generator[Tuple[str, str, str], None, None]:
    """Iterate over each group of 3 rucksacks."""
    index = 0
    while index < len(rucksacks):
        yield (rucksacks[index], rucksacks[index + 1], rucksacks[index + 2])
        index += 3


main()
