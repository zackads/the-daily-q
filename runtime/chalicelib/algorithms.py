"""
Get links to algorithms questions and prepare them for emailing
"""

import random
from typing import Tuple, TypedDict


def get_random_problem() -> str:
    question_numbers = {
        1: 38,  # chapter number : number of questions
        2: 55,
        3: 45,
        4: 53,
        5: 16
    }

    random_chapter = random.choice(list(question_numbers.keys()))
    random_problem = random.randint(1, question_numbers[random_chapter])

    return str(random_chapter) + "." + str(random_problem)


def email_body(problem_number: str) -> Tuple[str, str]:
    return body_html(problem_number), body_plaintext(problem_number)


def body_html(problem_number: str) -> str:
    """
    Format a question email
    """
    return f"""<html>
<head></head>
<body>
    <h1>The Daily Q</h1>
    <a href="https://www.algorist.com/algowiki/index.php/Solution_Wiki,_The_Algorithm_Design_Manual,_3rd_Edition">
        Algorithms questions
    </a>
    <p>Select question <b>{problem_number}</b></p>
</body>
</html>
"""


def body_plaintext(problem_number: str) -> str:
    """
    Plaintext question email
    """
    return f"""
The Daily Q

Do problem number {problem_number}. 

https://www.algorist.com/algowiki/index.php/Solution_Wiki,_The_Algorithm_Design_Manual,_3rd_Edition 
"""
