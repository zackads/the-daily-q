"""
Get links to mathematics questions and prepare them for emailing
"""

import random
import math
from typing import Tuple, TypedDict


class Problem(TypedDict):
    """
    URLs linking to a single question and its worked solution with examiner feedback.
    Links go to images hosted in S3.
    """

    questionUrl: str
    solutionUrl: str


def get_problems(s3_bucket, directory_name) -> list[Problem]:
    """
    List all URLs to questions and their solutions
    """
    s3_url = f"https://{s3_bucket.name}.s3.eu-west-2.amazonaws.com/"

    questions = [
        s3_url + q.key for q in s3_bucket.objects.filter(Prefix=f'{directory_name}/questions')
    ]
    solutions = [
        s3_url + s.key for s in s3_bucket.objects.filter(Prefix=f'{directory_name}/solutions')
    ]

    return [{"questionUrl": q, "solutionUrl": s} for q, s in zip(questions, solutions)]


def get_random_problem(s3_bucket, directory_name) -> Problem:
    """
    Select a random question from the question bank using a uniform distribution

    Return a tuple of the question URL and the solution URL
    """
    questions = get_problems(s3_bucket, directory_name)
    i = random.randrange(0, len(questions))

    return questions[i]


def get_random_recent_question(s3_bucket) -> Problem:
    """
    Select a random question from the question bank using a triangular distribution.

    Return a tuple of the question URL and the solution URL
    """
    questions = get_problems(s3_bucket)
    i = math.ceil(random.triangular(0, len(questions), len(questions)))

    return questions[i]


def email_body(question: Problem) -> Tuple[str, str]:
    """
    Return the body HTML and plaintext for a question email
    """
    return body_html(question), body_plaintext(question)


def body_html(question: Problem) -> str:
    """
    Format a question email
    """
    return f"""<html>
<head></head>
<body>
    <h1>The Daily Q</h1>
    <img src="{question['questionUrl']}" />
    <a href="{question['solutionUrl']}">Solution</a>
</body>
</html>
"""


def body_plaintext(question: Problem) -> str:
    """
    Plaintext question email
    """
    return f"""
The Daily Q

Question: {question['questionUrl']} 

Solution: {question['solutionUrl']} 
"""
