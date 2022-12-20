from dataclasses import dataclass
from typing import List


@dataclass
class ValueWithOrigin:
    initial_position: int
    value: int


Data = List[ValueWithOrigin]
File = List[int]


def decrypt(file: File, num_mixes: int = 1):
    data = [ValueWithOrigin(initial_index, value) for initial_index, value in enumerate(file)]
    for _ in range(num_mixes):
        mix(data)
    return get_coords(data)


def get_coords(data: Data):
    start_index = 0
    while data[start_index].value != 0:
        start_index += 1
    return sum(data[(start_index + x) % len(data)].value for x in (1000, 2000, 3000))


def mix(data: Data):
    print("Mixing")
    for initial_index in range(len(data)):
        curr_index = get_curr_index(initial_index, data)
        shift(curr_index, data[curr_index].value, data)


def get_curr_index(index: int, data: Data):
    for i, val_with_origin in enumerate(data):
        if val_with_origin.initial_position == index:
            return i

    raise IndexError("Index not found")


def shift(index: int, amount_to_shift: int, data: List):
    size = len(data)
    sign = 1 if amount_to_shift >= 0 else -1

    cycle_length = len(data) - 1
    amount_to_shift = sign * (abs(amount_to_shift) % cycle_length)

    while amount_to_shift != 0:
        tmp = data[index % size]
        data[index % size] = data[(index + sign) % size]
        data[(index + sign) % size] = tmp
        amount_to_shift -= sign
        index += sign
