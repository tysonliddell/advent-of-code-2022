from operator import mul
from typing import Generator, List, Tuple

from aoc_python.common.utils import get_day_n_input
from aoc_python.d11.monkey import Monkey, do_round


def main():
    data = get_day_n_input(11)

    monkeys = _parse_monkeys(data)
    for _ in range(10000):
        do_round(monkeys)
    print(mul(*sorted([m.inspection_count for m in monkeys])[-2:]))


def _iter_monkey_input(data: List[str]) -> Generator[Tuple, None, None]:
    while data:
        num = int(data.pop(0).replace(":", "").split(" ")[1])
        items = eval(f'[{data.pop(0).split(":")[1]}]')

        op = eval(f'lambda old: {data.pop(0).split(":")[1].split("=")[1]}')

        condition, if_true, if_false = (int(data.pop(0).split(" ")[-1]) for _ in range(3))
        divisor = condition

        test = eval(f"lambda x: {if_true} if x%{condition} == 0 else {if_false}")
        yield (num, items, op, divisor, test)

        while data and data[0] == "":
            data.pop(0)


def _parse_monkeys(data: List[str]) -> List[Monkey]:
    return [
        Monkey(num=num, items=items, op=op, divisor=divisor, test=test)
        for num, items, op, divisor, test in _iter_monkey_input(data)
    ]


main()
