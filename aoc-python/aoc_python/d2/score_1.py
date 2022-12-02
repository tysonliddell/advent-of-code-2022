from typing import List


DECODER = {
    "A": "ROCK",
    "B": "PAPER",
    "C": "SCISSORS",
    "X": "ROCK",
    "Y": "PAPER",
    "Z": "SCISSORS",
}


START_SCORE = {
    "ROCK": 1,
    "PAPER": 2,
    "SCISSORS": 3,
}

STRONG_AGAINST = {
    "ROCK": "SCISSORS",
    "PAPER": "ROCK",
    "SCISSORS": "PAPER",
}


def _decode(data: List[List[str]]):
    return [[DECODER[x] for x in d] for d in data]


def get_p2_total_score(data: List[List[str]]):
    games = _decode(data)
    total = 0
    for p1,p2 in games:
        # add score for p2's choice
        total += START_SCORE[p2]

        # add victory condition
        if p1 == p2:
            total += 3
        elif STRONG_AGAINST[p2] == p1:
            total += 6
    return total
