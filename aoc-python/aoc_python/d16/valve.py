import pickle
from dataclasses import dataclass
from math import inf
from typing import Dict, List, Set


@dataclass
class Valve:
    name: str
    flow_rate: int
    next_valves: List["Valve"]
    valve_open: bool = False

    def __hash__(self) -> int:
        return self.name.__hash__()


Valves = Dict[str, Valve]
HopCountMap = Dict[str, Dict[str, int]]
ValveSequence = List[str]


def get_max_pressure_release(valves: Valves, start_valve="AA", time_left=30) -> int:
    num_hops = _get_valve_num_hops_map(valves)  # num_hops[foo][bar] gives number of hops from valve foo to bar
    valve_sequences = _get_all_valve_opening_sequences(num_hops, valves, [start_valve], time_left)
    totals = [_get_total_pressure_released(seq, num_hops, valves, time_left) for seq in valve_sequences]
    return max(totals)


def get_max_pressure_release_with_elephant(valves: Valves, start_valve="AA", time_left=26):
    num_hops = _get_valve_num_hops_map(valves)  # num_hops[foo][bar] gives number of hops from valve foo to bar
    valve_sequences = _get_all_valve_opening_sequences(num_hops, valves, [start_valve], time_left)

    max_length = len([v for v in valves.values() if v.flow_rate > 0]) + 1
    valve_sequences_by_length: Dict[int, List[ValveSequence]] = {i: [] for i in range(0, max_length + 1)}
    for seq in valve_sequences:
        valve_sequences_by_length[len(seq)].append(seq)

    # sort the valve sequences grouped by length so we can (somewhat) quickly search them
    for sequences in valve_sequences_by_length.values():
        sequences.sort(key=lambda s: -_get_total_pressure_released(s, num_hops, valves, time_left))

    max_pressure_released = 0
    i = 0
    for seq in valve_sequences:
        i += 1
        total = _get_total_pressure_released(seq, num_hops, valves, time_left)

        # Since we are looking for the complement of each sequence, symmetry allows us to
        # half the search space.
        if total < max_pressure_released // 2:
            continue

        print(f"{i}/{len(valve_sequences)}")

        req_elephant_valve_seq_length = max_length - len(seq) + 1
        total_elephant = _get_best_valve_sequence_total(
            req_elephant_valve_seq_length,
            set(seq) - {start_valve},
            valve_sequences_by_length,
            num_hops,
            valves,
            time_left,
        )
        max_pressure_released = max(max_pressure_released, total + total_elephant)
        print(max_pressure_released)
    return max_pressure_released


_total_cache = {}


def _get_best_valve_sequence_total(
    required_length: int, ignore: Set[str], valve_sequences_by_length, valve_hop_map, valves, time_mins: int
):
    global _total_cache
    ignore_key = tuple(sorted(ignore))
    if (required_length, ignore_key) not in _total_cache:
        # print("cache miss")
        found = False
        totals = []
        for length in range(1, required_length + 1):
            for seq in valve_sequences_by_length[length]:
                if not set(seq) & ignore:
                    found = True
                    break
            if not found:
                seq = []
            totals.append(_get_total_pressure_released(seq, valve_hop_map, valves, time_mins))
        _total_cache[(required_length, ignore_key)] = max(totals)
    else:
        # print("cache hit")
        pass

    return _total_cache[(required_length, ignore_key)]


def _get_total_pressure_released(
    valve_sequence: ValveSequence, hop_count_map: HopCountMap, valves: Valves, time_mins: int
) -> int:
    rate, total = 0, 0
    for from_v, to_v in zip(valve_sequence, valve_sequence[1:]):
        if time_mins <= 0:
            break
        mins_used = hop_count_map[from_v][to_v]
        mins_used += 1  # add an extra second to wait for valve to open
        total += rate * min(mins_used, time_mins)

        time_mins -= mins_used
        rate += valves[to_v].flow_rate

    # add the remaining minutes after the valve sequence is finished
    return total + rate * max(0, time_mins)


def _is_valve_sequence_complete(valve_sequence: ValveSequence, valve_hop_map: HopCountMap, target_time: int) -> int:
    for from_v, to_v in zip(valve_sequence, valve_sequence[1:]):
        if target_time <= 0:
            break
        mins_used = valve_hop_map[from_v][to_v] + 1
        target_time -= mins_used
    return target_time <= 0


def _get_all_valve_opening_sequences(
    hop_count_map: HopCountMap, valves: Valves, current_valve_seqence: ValveSequence, max_time: int
) -> List[List[str]]:
    # Get all possible valve opening sequences that can be traversed within the time threshold.

    if len(current_valve_seqence) == len(valves) or _is_valve_sequence_complete(
        current_valve_seqence, hop_count_map, max_time
    ):
        return [current_valve_seqence]

    closed_valves = valves.keys() - set(current_valve_seqence)
    res = [current_valve_seqence]
    for valve in closed_valves:
        if valves[valve].flow_rate != 0:  # critical optimisation
            res.extend(
                _get_all_valve_opening_sequences(hop_count_map, valves, current_valve_seqence + [valve], max_time)
            )
    return res


def _get_valve_num_hops_map(valves: Valves) -> HopCountMap:
    # Build a matrix of shortest number of hops between valves.
    # Takes a couple of minutes to build. Cache it to disk for easy debugging.
    #
    # We do this because any solution can be uniquely determined by a list of unique valves, representing
    # the order in which they were opened. We can use a mapping of the number of hops between any two such
    # valves to quickly compute the total flow through the system for a given ordering of valve openings.

    visited = set()

    def number_of_hops(from_valve: Valve, to_valve: Valve):
        if from_valve == to_valve:
            return 0

        visited.add(from_valve)
        distances = [inf]
        for v in from_valve.next_valves:
            if v not in visited:
                distances.append(number_of_hops(v, to_valve) + 1)
        visited.remove(from_valve)
        return min(distances)

    try:
        valve_hop_map = pickle.load(open("valve_hop_map.pickle", "rb"))
    except (OSError, IOError):
        print("Building valve hop map.")
        valve_hop_map = {v.name: {} for v in valves.values()}
        i = 0
        for from_v in valves.values():
            i += 1
            print(f"{(i/len(valve_hop_map))*100:.2f}%")
            distances_from_v = {to_v.name: number_of_hops(from_v, to_v) for to_v in valves.values()}
            valve_hop_map[from_v.name] = distances_from_v
        pickle.dump(valve_hop_map, open("valve_hop_map.pickle", "wb"))
        print("Built map.")
    return valve_hop_map
