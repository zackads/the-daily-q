import os
import boto3
import random
from chalice import Chalice, Cron
from botocore.exceptions import ClientError

app = Chalice(app_name="the-daily-q")
s3 = boto3.resource("s3")
s3_bucket = s3.Bucket(os.environ.get("S3_BUCKET_NAME", "the-daily-q"))
ses = boto3.client("ses", region_name="eu-west-2")

# The first and only email address verified with SES, i.e. mine
email_address = ses.list_identities()["Identities"][0]

SENDER = "The Daily Q <" + email_address + ">"
RECIPIENT = email_address
SUBJECT = "The Daily Q"


@app.schedule(Cron(0, 7, "*", "*", "?", "*"))  # Daily at 7am UTC
def send_daily_email(event):
    send_email()
    send_email()
    send_email()


def send_email():
    question, solution = random_question()

    try:
        response = ses.send_email(
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

    questions = [S3_URL + q.key for q in s3_bucket.objects.filter(Prefix="questions")]
    solutions = [S3_URL + s.key for s in s3_bucket.objects.filter(Prefix="solutions")]

    return list(zip(questions, solutions))


def random_question():
    """
    Select a question from the question bank.
    
    Return a tuple of the question URL and the solution URL
    """
    questions = get_questions()
    i = random.randrange(0, len(questions))

    return questions[i]


def body_plaintext(question_url, solution_url):
    return "The Daily Q" f"Question: {question_url}" f"Solution: {solution_url}"


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
