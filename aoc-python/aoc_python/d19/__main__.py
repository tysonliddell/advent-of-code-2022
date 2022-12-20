import re
from collections import Counter
from typing import List

from aoc_python.common.utils import get_day_n_input
from aoc_python.d19.robot import Blueprint

TEST_DATA = [
    """Blueprint 1:
 Each ore robot costs 4 ore.
 Each clay robot costs 2 ore.
 Each obsidian robot costs 3 ore and 14 clay.
 Each geode robot costs 2 ore and 7 obsidian.""".replace(
        "\n", ""
    ),
    """Blueprint 2:
 Each ore robot costs 2 ore.
 Each clay robot costs 3 ore.
 Each obsidian robot costs 3 ore and 8 clay.
 Each geode robot costs 3 ore and 12 obsidian.""".replace(
        "\n", ""
    ),
]

BLUEPRINT_REGEX = re.compile(
    r"Blueprint (\d+):"
    r"\sEach (\w+) robot costs (\d+) (\w+)."
    r"\sEach (\w+) robot costs (\d+) (\w+)."
    r"\sEach (\w+) robot costs (\d+) (\w+) and (\d+) (\w+)."
    r"\sEach (\w+) robot costs (\d+) (\w+) and (\d+) (\w+)."
)

NUM_MINS = 24


def main():
    # data = TEST_DATA
    data = get_day_n_input(19)
    start_robots = Counter({"ore": 1})
    blueprints = _parse_blueprints(data)
    results = {}
    for bp in blueprints:
        print(f"Processing Blueprint {bp.id}")
        results[bp.id] = bp.get_max_material("geode", start_robots, 24)
    print(sum(id * geode_count for id, geode_count in results.items()))
    print()

    # Part 2
    solution = 1
    for bp in blueprints[:3]:
        print(f"Processing Blueprint {bp.id}")
        res = bp.get_max_material("geode", start_robots, 32)
        print(res)
        solution *= res
    print(solution)


def _parse_blueprints(data: List[str]) -> list[Blueprint]:
    blueprints = []
    for line in data:
        match = BLUEPRINT_REGEX.match(line)
        assert match is not None
        bp = Blueprint(id=int(match.group(1)))
        bp.costs[match.group(2)] = Counter({match.group(4): int(match.group(3))})
        bp.costs[match.group(5)] = Counter({match.group(7): int(match.group(6))})
        bp.costs[match.group(8)] = Counter(
            {match.group(10): int(match.group(9)), match.group(12): int(match.group(11))}
        )
        bp.costs[match.group(13)] = Counter(
            {match.group(15): int(match.group(14)), match.group(17): int(match.group(16))}
        )
        blueprints.append(bp)
    return blueprints


main()
