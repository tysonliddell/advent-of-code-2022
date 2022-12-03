from typing import Generator, Sequence, Set


def get_priority_sum_of_intersections(collection: Sequence[Sequence[str]]) -> int:
    return sum(map(lambda i: _get_item_priority(i.pop()), _iter_intersections(collection)))


def _iter_intersections(collection: Sequence[Sequence[str]]) -> Generator[Set[str], None, None]:
    """Iterate the the intersecions of a collection of sequences."""
    for sequence in collection:
        yield set.intersection(*map(lambda s: set(s), sequence))


def _get_item_priority(item: str) -> int:
    ascii_ord = ord(item)
    if ord("a") <= ascii_ord <= ord("z"):
        return ascii_ord - ord("a") + 1
    if ord("A") <= ascii_ord <= ord("z"):
        return ascii_ord - ord("A") + 27

    raise ValueError("Input item sould be in range a-z or A-Z")
