"""NRICH Olympiad-style maths problems"""
import json
from random import choice
from typing import TypedDict, Tuple


class NRICHShort(TypedDict):
    """
    https://nrich.maths.org/11993
    """

    title: str
    href: str


def get_random_short_problem() -> NRICHShort:
    """Short problems from https://nrich.maths.org/11993"""

    with open("nrich_short_problems.json", "r") as file:
        problems = json.load(file)

    return choice(problems)


def email_body(problem: NRICHShort) -> Tuple[str, str]:
    return body_html(problem), body_plaintext(problem)


def body_html(problem: NRICHShort) -> str:
    return f"""<html>
<head></head>
<body>
    <a href="{problem['href']}"><h1>{problem['title']}</h1></a>
</body>
</html>
"""


def body_plaintext(problem: NRICHShort):
    return "Daily NRICH Short" f"{problem['title']}: {problem['url']}"
