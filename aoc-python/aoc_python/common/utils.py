from typing import List
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import keyring
import requests
import sqlite3


AOC_BASE_URL = "https://adventofcode.com"
AOC_AUTH_URL = f"{AOC_BASE_URL}/auth/github"
AOC_BASE_PUZZLE_URL = f"{AOC_BASE_URL}/2022"
CHROME_COOKIES_DB = "/Users/tyson/Library/Application Support/Google/Chrome/Default/Cookies"


def decrypt_chrome_cookie(encrypted_value: bytes) -> str:
    """
    Taken from https://stackoverflow.com/a/23727331
    """

    # Trim off the 'v10' that Chromeium prepends
    encrypted_value = encrypted_value[3:]

    # Default values used by both Chrome and Chromium in OSX and Linux
    salt = b'saltysalt'
    iv = b' ' * 16
    length = 16

    # On Mac, use your password from Keychain
    # On Linux, use 'peanuts'
    my_pass = keyring.get_password("Chrome Safe Storage", "Chrome")
    my_pass = my_pass.encode('utf8')

    # 1003 on Mac, 1 on Linux
    iterations = 1003

    key = PBKDF2(my_pass, salt, length, iterations)
    cipher = AES.new(key, AES.MODE_CBC, IV=iv)

    decrypted = cipher.decrypt(encrypted_value)

    # Get rid of padding
    clean = lambda x: x[:-x[-1]].decode('utf8')
    return clean(decrypted)


def get_github_session_cookie() -> str:
    """Get an existing Github session cookie from the Chrome cookie database."""
    try:
        conn = sqlite3.connect(CHROME_COOKIES_DB)
        row = conn.cursor().execute(
            "SELECT encrypted_value FROM cookies "
            "WHERE host_key = 'github.com' "
            "AND name = 'user_session';"
        ).fetchone()
        if not row:
            raise RuntimeError(
                "No active Github session in Chrome. "
                "Login to Github in chrome to create a session."
            )
        encrypted_user_session: bytes = row[0]
    finally:
        conn.close()

    return decrypt_chrome_cookie(encrypted_user_session)


def get_day_n_input(n: int) -> List[str]:
    """Get the input for puzzle on day N."""

    # grab an existing Github session cookie and use it to login
    # to Advent of Code.
    import os
    aoc_cookie = os.environ.get("AOC_COOKIE", None)
    sess = requests.Session()
    if aoc_cookie:
        sess.cookies.set("session", aoc_cookie)
    else:
        raise RuntimeError("FIXME: We don't use github anymore")

    # get the puzzle input
    resp = sess.get(f"{AOC_BASE_PUZZLE_URL}/day/{n}/input")
    puzzle_input = resp.text.splitlines()
    return puzzle_input
