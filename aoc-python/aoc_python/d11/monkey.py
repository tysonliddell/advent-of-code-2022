from dataclasses import dataclass, field
from typing import Callable, List


@dataclass
class Monkey:
    num: int
    items: List[int] = field(default_factory=list)
    op: Callable[[int], int] = lambda x: 0
    test: Callable[[int], int] = lambda x: 0
    inspection_count: int = 0


def do_round(monkeys: List[Monkey]):
    for monkey in monkeys:
        while monkey.items:
            item = monkey.items.pop(0)
            monkey.inspection_count += 1
            worry_level = monkey.op(item) // 3
            next_monkey = monkey.test(worry_level)
            monkeys[next_monkey].items.append(worry_level)
