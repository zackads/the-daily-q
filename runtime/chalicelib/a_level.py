"""
Get links to A-level Mathematics questions and prepare them for emailing
"""

import random
from typing import Tuple, TypedDict


class ALevelQuestion(TypedDict):
    """
    URLs linking to a single A-level question and its worked solution with examiner feedback.
    Links go to images hosted in S3.
    """
    questionUrl: str
    solutionUrl: str


def get_questions(s3_bucket) -> list[ALevelQuestion]:
    """
    List all URLs to A-level questions and their solutions
    """
    s3_url = f'https://{s3_bucket.name}.s3.eu-west-2.amazonaws.com/'

    questions = [s3_url + q.key for q in s3_bucket.objects.filter(Prefix="a_level/questions")]
    solutions = [s3_url + s.key for s in s3_bucket.objects.filter(Prefix="a_level/solutions")]

    return [{'questionUrl': q, 'solutionUrl': s} for q, s in zip(questions, solutions)]


def get_random_question(s3_bucket) -> ALevelQuestion:
    """
    Select a question from the question bank.

    Return a tuple of the question URL and the solution URL
    """
    questions = get_questions(s3_bucket)
    i = random.randrange(0, len(questions))

    return questions[i]


def email_body(question: ALevelQuestion) -> Tuple[str, str]:
    """
    Return the body HTML and plaintext for an A-level question email
    """
    return body_html(question), body_plaintext(question)


def body_html(question: ALevelQuestion) -> str:
    """
    Format an A-level question email
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


def body_plaintext(question: ALevelQuestion) -> str:
    """
    Plaintext A-level question email
    """
    return f"""
The Daily Q

Question: {question['questionUrl']} 

Solution: {question['solutionUrl']} 
"""
