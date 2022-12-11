from operator import mul
from typing import Generator, List, Tuple

from aoc_python.common.utils import get_day_n_input
from aoc_python.d11.monkey import Monkey, do_round

TEST_DATA = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1""".splitlines()


def main():
    data = get_day_n_input(11)
    # data = TEST_DATA

    monkeys = _parse_monkeys(data)
    for _ in range(20):
        do_round(monkeys)
    print(mul(*sorted([m.inspection_count for m in monkeys])[-2:]))


def _iter_monkey_input(data: List[str]) -> Generator[Tuple, None, None]:
    while data:
        num = int(data.pop(0).replace(":", "").split(" ")[1])
        items = eval(f'[{data.pop(0).split(":")[1]}]')

        op = eval(f'lambda old: {data.pop(0).split(":")[1].split("=")[1]}')

        condition, if_true, if_false = (int(data.pop(0).split(" ")[-1]) for _ in range(3))

        # test = lambda x: if_true if x%condition == 0 else if_false
        test = eval(f"lambda x: {if_true} if x%{condition} == 0 else {if_false}")
        # test = lambda x: if_true if x%condition == 0 else if_false
        yield (num, items, op, test)

        while data and data[0] == "":
            data.pop(0)


def _parse_monkeys(data: List[str]) -> List[Monkey]:
    return [Monkey(num=num, items=items, op=op, test=test) for num, items, op, test in _iter_monkey_input(data)]


main()
