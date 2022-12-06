import os
import pathlib
from typing import List

import requests

from aoc_python import PROJECT_ROOT_DIR

AOC_BASE_URL = "https://adventofcode.com"
AOC_BASE_PUZZLE_URL = f"{AOC_BASE_URL}/2022"
INPUT_FILES_DIR = f"{PROJECT_ROOT_DIR}/../puzzle_input"


def get_day_n_input(n: int) -> List[str]:
    """Get the input for puzzle on day N."""

    pathlib.Path(INPUT_FILES_DIR).mkdir(parents=True, exist_ok=True)
    input_file_path = f"{INPUT_FILES_DIR}/d{n}"

    try:
        with open(input_file_path) as f:
            data = f.read()
            print("Got puzzle input data from file.")
    except FileNotFoundError:
        data = _fetch_input_from_aoc(day_num=n)
        print("Fetched puzzle input data from AoC.")
        with open(input_file_path, "w") as f:
            f.write(data)
            print("Wrote puzzle input data to file.")

    # get the puzzle input
    return data.splitlines()


def _fetch_input_from_aoc(day_num: int) -> str:
    aoc_cookie = os.environ["AOC_COOKIE"]
    sess = requests.Session()
    sess.cookies.set("session", aoc_cookie)

    resp = sess.get(f"{AOC_BASE_PUZZLE_URL}/day/{day_num}/input")
    return resp.text
