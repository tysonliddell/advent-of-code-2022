from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class Op(Enum):
    ADDX = 0
    NOOP = 1


@dataclass
class Instruction:
    op: Op
    arg: Optional[int]


class CPU:
    def __init__(self):
        self.program = None
        self.restart()

    def restart(self):
        self.ip = 0
        self.cycles_done = 0
        self.in_add = False
        self.x = 1

    def upload_program(self, program: List[Instruction]):
        self.program = program

    def tick(self):
        if self.is_finished():
            return

        self.cycles_done += 1
        if not self.in_add and self.curr_instruction().op == Op.ADDX:
            self.in_add = True
            return

        if self.curr_instruction().op == Op.ADDX:
            self.in_add = False
            self.x += self.curr_instruction().arg
        self.ip += 1

    def tick_n(self, n: int):
        for _ in range(n):
            self.tick()

    def run_program(self):
        while not self.is_finished():
            self.tick()

    def is_finished(self):
        return self.ip >= len(self.program)

    def curr_instruction(self) -> Instruction:
        return self.program[self.ip]

    def curr_signal_strength(self) -> int:
        return self.x * (self.cycles_done + 1)
