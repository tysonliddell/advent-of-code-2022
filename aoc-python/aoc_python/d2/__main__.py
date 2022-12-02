from aoc_python.common.utils import get_day_n_input
from aoc_python.d2.score_1 import get_p2_total_score as get_strategy1_score
from aoc_python.d2.score_2 import get_p2_total_score as get_strategy2_score


def main():
    data = [line.split() for line in get_day_n_input(2)]
    print(get_strategy1_score(data))
    print(get_strategy2_score(data))


main()
