import os
import boto3
import random
from chalice import Chalice
from botocore.exceptions import ClientError

SENDER = "The Daily Q <" + {os.environ.get("SENDER")} + ">"
RECIPIENT = os.environ.get("RECIPIENT")
SUBJECT = "The Daily Q"

app = Chalice(app_name="the-daily-q")
s3 = boto3.resource("s3")
s3_bucket = s3.Bucket(os.environ.get("S3_BUCKET_NAME", ""))
ses = boto3.client("ses", region_name="eu-west-2")

@app.route("/questions", methods=["GET"])
def get_questions():
    S3_URL = "https://the-daily-q.s3.eu-west-2.amazonaws.com/"
    questions = [q.key for q in s3_bucket.objects.filter(Prefix='questions/')].sort()
    solutions = [s.key for s in s3_bucket.objects.filter(Prefix='solutions/')].sort()

    return list(zip(questions, solutions))


@app.route("/email", methods=["POST"])
def send_email():
    question, solution = random_question()

    try:
        response = ses.send_email(
            Destination={"ToAddresses": [RECIPIENT]},
            Message={
                "Body": {
                    "Html": {"Charset": "UTF-8", "Data": body_html(question, solution)},
                    "Text": {"Charset": "UTF-8", "Data": body_plaintext(question, solution)},
                },
                "Subject": {"Charset": "UTF-8", "Data": SUBJECT},
            },
            Source=SENDER,
        )
    except ClientError as e:
        return e.response["Error"]["Message"]
    else:
        return "Email sent! Message ID: ", response["MessageId"]


def random_question():
    """
    Select a question from the question bank.
    
    Return a tuple of the question URL and the solution URL
    """
    questions = get_questions()
    i = random.randrange(0, questions.length)

    return questions[i]

def body_plaintext(question_url, solution_url):
    return ("The Daily Q"
    f"Question: {question_url}"
    f"Solution: {solution_url}"
    )

def body_html(question_url, solution_url):
    return """<html>
<head></head>
<body>
    <h1>The Daily Q</h1>
    <img src="{}" />
    <a href="{}">Solution</a>
</body>
</html>
""".format(question_url, solution_url)
