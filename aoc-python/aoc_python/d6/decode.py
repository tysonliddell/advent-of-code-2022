from collections import Counter
from typing import Tuple


def find_marker(data: str, marker_length: int = 4) -> Tuple[str, int]:
    index = 0
    seen = Counter(data[:marker_length])

    while len(seen) != marker_length:
        old_c, new_c = data[index], data[index + marker_length]
        seen[old_c] -= 1
        if seen[old_c] == 0:
            del seen[old_c]
        seen[new_c] += 1
        index += 1

    return (data[index : index + marker_length], index + marker_length)
