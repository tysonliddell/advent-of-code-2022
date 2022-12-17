from functools import cache

from aoc_python.d16.valve import Valve, Valves


def get_max_pressure_release_naive(valves: Valves, time_mins=30):
    @cache
    def backtrack(curr_valve: Valve, time_left: int, total_rate: int, total_released: int) -> int:
        if time_left == 0:
            return total_released

        released_open = 0
        if not curr_valve.valve_open:
            curr_valve.valve_open = True
            released_open = backtrack(
                curr_valve, time_left - 1, total_rate + curr_valve.flow_rate, total_released + total_rate
            )
            curr_valve.valve_open = False

        best_tunnel = max(
            [backtrack(v, time_left - 1, total_rate, total_released + total_rate) for v in curr_valve.next_valves]
        )
        return max(released_open, best_tunnel)

    return backtrack(valves["AA"], time_mins, 0, 0)
