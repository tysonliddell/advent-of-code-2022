from functools import cmp_to_key
from typing import Generator, List, Tuple

from aoc_python.common.utils import get_day_n_input
from aoc_python.d13.packets import DIVIDER_PACKETS, Packet, compare_packet_pair, compare_packet_pairs


def main():
    data = get_day_n_input(13)
    packet_pairs = _parse_packets(data)

    # Part 1
    result = compare_packet_pairs(packet_pairs)
    print(sum([i + 1 for i, v in enumerate(result) if v]))

    # Part 2
    packets = [packet for pair in packet_pairs for packet in pair]
    packets.extend(DIVIDER_PACKETS)
    packets.sort(key=cmp_to_key(compare_packet_pair))
    packets.reverse()
    i1 = packets.index(DIVIDER_PACKETS[0]) + 1
    i2 = packets.index(DIVIDER_PACKETS[1]) + 1
    decoder_key = i1 * i2
    print(decoder_key)


def _parse_packets(data: List[str]) -> List[Tuple[Packet, Packet]]:
    return list(_iter_packet_pairs(data))


def _iter_packet_pairs(data: List[str]) -> Generator[Tuple[Packet, Packet], None, None]:
    while data:
        packet1 = eval(data.pop(0))
        packet2 = eval(data.pop(0))
        yield (packet1, packet2)

        if data:
            data.pop(0)


main()
