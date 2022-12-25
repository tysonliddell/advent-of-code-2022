from aoc_python.common.utils import get_day_n_input

DIGIT_MAP = {
    "=": -2,
    "-": -1,
    "0": 0,
    "1": 1,
    "2": 2,
}


def main():
    data = get_day_n_input(25)

    result = []
    carry = 0
    current_digit_place = 1
    while data or carry:
        val = carry + sum(DIGIT_MAP[line[-current_digit_place]] for line in data)

        snafu_digit = next(snaf for snaf, dec in DIGIT_MAP.items() if dec % 5 == val % 5)
        result.append(snafu_digit)

        carry = val - DIGIT_MAP[snafu_digit]
        carry //= 5

        current_digit_place += 1
        data = [line for line in data if len(line) >= current_digit_place]
    print("".join(reversed(result)))


main()
