from typing import List

DECODER = {
    "A": "ROCK",
    "B": "PAPER",
    "C": "SCISSORS",
    "X": "LOSE",
    "Y": "DRAW",
    "Z": "WIN",
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

WEAK_AGAINST = {v: k for k, v in STRONG_AGAINST.items()}


def _decode(data: List[List[str]]):
    return [[DECODER[x] for x in d] for d in data]


def _get_p2_choice(p1: str, result_needed: str):
    if result_needed == "DRAW":
        return p1
    elif result_needed == "LOSE":
        return STRONG_AGAINST[p1]
    else:
        return WEAK_AGAINST[p1]


def get_p2_total_score(data: List[List[str]]):
    games = _decode(data)
    total = 0
    for p1, result_needed in games:
        p2 = _get_p2_choice(p1, result_needed)

        # add score for p2's choice
        total += START_SCORE[p2]

        # add victory condition
        if p1 == p2:
            total += 3
        elif STRONG_AGAINST[p2] == p1:
            total += 6
    return total
