import os
from typing import List

import requests

AOC_BASE_URL = "https://adventofcode.com"
AOC_BASE_PUZZLE_URL = f"{AOC_BASE_URL}/2022"


def get_day_n_input(n: int) -> List[str]:
    """Get the input for puzzle on day N."""

    aoc_cookie = os.environ["AOC_COOKIE"]
    sess = requests.Session()
    sess.cookies.set("session", aoc_cookie)

    # get the puzzle input
    resp = sess.get(f"{AOC_BASE_PUZZLE_URL}/day/{n}/input")
    puzzle_input = resp.text.splitlines()
    return puzzle_input
