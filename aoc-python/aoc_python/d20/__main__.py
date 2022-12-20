from aoc_python.common.utils import get_day_n_input
from aoc_python.d20.decrypt import decrypt

TEST_DATA = """1
2
-3
3
-2
0
4""".splitlines()

DECRYPTION_KEY = 811589153


def main():
    # data = TEST_DATA
    data = get_day_n_input(20)

    # Part 1
    file = [int(x) for x in data]
    print(decrypt(file))
    print()

    # Part 2
    keyed_file = [x * DECRYPTION_KEY for x in file]
    print(decrypt(keyed_file, 10))


main()
