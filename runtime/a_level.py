import random

from botocore.exceptions import ClientError

from runtime.app import ses, RECIPIENT, SUBJECT, SENDER, \
    s3_bucket


def email_random_a_level_question():
    question, solution = random_question()

    try:
        response = ses.email_random_a_level_question(
            Destination={"ToAddresses": [RECIPIENT]},
            Message={
                "Body": {
                    "Html": {"Charset": "UTF-8", "Data": body_html(question, solution)},
                    "Text": {
                        "Charset": "UTF-8",
                        "Data": body_plaintext(question, solution),
                    },
                },
                "Subject": {"Charset": "UTF-8", "Data": SUBJECT},
            },
            Source=SENDER,
        )
    except ClientError as e:
        return e.response["Error"]["Message"]
    else:
        return "Email sent! Message ID: ", response["MessageId"]


def get_questions():
    S3_URL = "https://the-daily-q.s3.eu-west-2.amazonaws.com/"

    questions = [S3_URL + q.key for q in s3_bucket.objects.filter(Prefix="a_level/questions")]
    solutions = [S3_URL + s.key for s in s3_bucket.objects.filter(Prefix="a_level/solutions")]

    return list(zip(questions, solutions))


def random_question():
    """
    Select a question from the question bank.

    Return a tuple of the question URL and the solution URL
    """
    questions = get_questions()
    i = random.randrange(0, len(questions))

    return questions[i]


def body_html(question_url, solution_url):
    return """<html>
<head></head>
<body>
    <h1>The Daily Q</h1>
    <img src="{}" />
    <a href="{}">Solution</a>
</body>
</html>
""".format(
        question_url, solution_url
    )


def body_plaintext(question_url, solution_url):
    return "The Daily Q" f"Question: {question_url}" f"Solution: {solution_url}"
