from typing import List

from aoc_python.common.utils import get_day_n_input
from aoc_python.d16.valve import Valve, Valves, get_max_pressure_release, get_max_pressure_release_with_elephant

# from aoc_python.d16.naive_valve import get_max_pressure_release_naive

TEST_DATA = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II""".splitlines()


def main():
    data = get_day_n_input(16)
    # data = TEST_DATA
    valves = _parse_valves(data)
    # print(get_max_pressure_release_naive(valves))
    print(get_max_pressure_release(valves))
    print(get_max_pressure_release_with_elephant(valves))


def _parse_valves(data: List[str]) -> Valves:
    next_map = {}
    valves: Valves = {}
    for line in data:
        _, name, _, _, rate = line.split(";")[0].split(" ")
        rate_val = int(rate.split("=")[1])
        _, _, _, _, next_list = line.split("; ")[1].split(" ", 4)
        next_map[name] = next_list.replace(" ", "").split(",")
        valves[name] = Valve(name=name, flow_rate=rate_val, next_valves=[])

    for valve in valves.values():
        valve.next_valves = [valves[name] for name in next_map[valve.name]]

    return valves


main()
