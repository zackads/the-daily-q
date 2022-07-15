import os
import boto3
import random
from chalice import Chalice
from botocore.exceptions import ClientError

SENDER = "The Daily Q <zadlington@gmail.com>"
RECIPIENT = "zadlington@gmail.com"
AWS_REGION = "eu-west-2"
SUBJECT = "The Daily Q"

BODY_TEXT = "This is a test email"
BODY_HTML = """<html>
<head></head>
<body>
    <h1>The Daily Q</h1>
    <p>This is a test email
</body>
</html>
"""
CHARSET = "UTF-8"


app = Chalice(app_name="the-daily-q")
s3 = boto3.resource("s3")
s3_bucket = s3.Bucket(os.environ.get("S3_BUCKET_NAME", ""))
ses = boto3.client("ses", region_name=AWS_REGION)


@app.route("/questions", methods=["GET"])
def get_questions():
    questions = [
        "https://the-daily-q.s3.eu-west-2.amazonaws.com/" + q.key
        for q in s3_bucket.objects.all()
    ]

    return questions


@app.route("/email", methods=["POST"])
def send_email():
    try:
        response = ses.send_email(
            Destination={"ToAddresses": [RECIPIENT]},
            Message={
                "Body": {
                    "Html": {"Charset": CHARSET, "Data": BODY_HTML,},
                    "Text": {"Charset": CHARSET, "Data": BODY_TEXT},
                },
                "Subject": {"Charset": CHARSET, "Data": SUBJECT},
            },
            Source=SENDER,
        )
    except ClientError as e:
        return e.response["Error"]["Message"]
    else:
        return "Email sent! Message ID: ", response["MessageId"]


def random_question():
    """
    Select a question from the question bank and return its URL
    """
    questions = [
        "https://the-daily-q.s3.eu-west-2.amazonaws.com/" + q.key
        for q in s3_bucket.objects.all()
    ]
    i = random.randrange(0, questions.length)

    return questions[i]

