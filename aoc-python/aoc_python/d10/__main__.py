from typing import List

from aoc_python.common.utils import get_day_n_input
from aoc_python.d10.cpu import CPU, Instruction, Op


def main():
    data = get_day_n_input(10)
    instructions = _parse_instructions(data)
    cpu = CPU()
    cpu.upload_program(instructions)
    cpu.restart()

    print(sum(_iter_signal_strength(cpu)))
    _draw_crt(cpu)


def _iter_signal_strength(cpu: CPU, offset: int = 20, step: int = 40):
    cpu.tick_n(offset - 1)
    yield cpu.curr_signal_strength()

    cpu.tick_n(step)
    while not cpu.is_finished():
        yield cpu.curr_signal_strength()
        cpu.tick_n(step)


def _draw_crt(cpu: CPU):
    cpu.restart()
    while not cpu.is_finished():
        col = cpu.cycles_done % 40
        if col == 0:
            print("")
        sprite_pos = cpu.x
        draw_pixel = abs(sprite_pos - col) <= 1
        print("#" if draw_pixel else ".", end="")
        cpu.tick()
    print("")


def _parse_instructions(data: List[str]) -> List[Instruction]:
    instructions: List[Instruction] = []
    for line in data:
        tokens = line.split(" ")
        if len(tokens) == 1:
            instructions.append(Instruction(op=Op.NOOP, arg=None))
        elif len(tokens) == 2:
            instructions.append(Instruction(op=Op.ADDX, arg=int(tokens[1])))
        else:
            raise ValueError("Unexpected instruction format")
    return instructions


main()
