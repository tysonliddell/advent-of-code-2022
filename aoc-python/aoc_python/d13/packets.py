from typing import List, Tuple, Union

Packet = Union[int, List["Packet"]]

DIVIDER_PACKETS = ([[2]], [[6]])


def compare_packet_pairs(packet_pairs: List[Tuple[Packet, Packet]]) -> List[bool]:
    res = []
    for packet1, packet2 in packet_pairs:
        res.append(compare_packet_pair(packet1, packet2))
    return [x > 0 for x in res]


def compare_packet_pair(packet1: Packet, packet2: Packet) -> int:
    if isinstance(packet1, int) and isinstance(packet2, int):
        return packet2 - packet1
    if isinstance(packet1, list) and isinstance(packet2, list):
        for i in range(len(packet1)):
            if i >= len(packet2):
                return -1
            val1, val2 = packet1[i], packet2[i]
            cmp = compare_packet_pair(val1, val2)
            if cmp != 0:
                return cmp
        return len(packet2) - len(packet1)

    if isinstance(packet1, int):
        packet1 = [packet1]
    if isinstance(packet2, int):
        packet2 = [packet2]
    return compare_packet_pair(packet1, packet2)
