"""
Email maths problems etc. periodically
"""

import os
from datetime import datetime
import random
import boto3
from botocore.exceptions import ClientError
from chalice import Chalice, Cron

from chalicelib import questions

s3 = boto3.resource("s3")
s3_bucket = s3.Bucket(os.environ.get("S3_BUCKET_NAME", "the-daily-q"))

app = Chalice(app_name="the-daily-q")
ses = boto3.client("ses", region_name="eu-west-2")

# The first and only email address verified with SES, i.e. mine
email_address = ses.list_identities()["Identities"][0]
SENDER = "The Daily Q <" + email_address + ">"
RECIPIENT = email_address


# @app.schedule(Cron(0, 6, "*", "*", "?", "*"))  # daily at 6am utc
# def send_a_level_questions(event):
#     """Daily question"""
#     send_email(
#         "The Daily Q", *questions.email_body(questions.get_random_question(s3_bucket, "degree"))
#     )


@app.schedule(Cron(0, 6, "*", "*", "?", "*"))  # daily at 6am utc
def send_leetcode_problem(event):
    """Daily Leetcode problem"""
    i = random.randint(1, 150)
    with open("static/leetcode.txt", "r") as leetcode_file:
        with open("static/neetcode.txt", "r") as solutions_file:
            problem_links = [l.strip() for l in leetcode_file.readlines()]
            solution_links = [l.strip() for l in solutions_file.readlines()]

    body = f"""<html>
<head></head>
<body>
    <h1>The Leetcode 150</h1>
    <a href="{problem_links[i]}">Today's problem</a>
    <a href="{solution_links[i]}">Solution on Neetcode</a>
</body>
</html>
"""

    send_email("Leetcode 150", body, body)


@app.route("/test", methods=["GET"])
def send_test_email():
    """For testing"""
    send_email(
        "Test A-level Q", *a_level.email_body(a_level.get_random_question(s3_bucket))
    )
    send_email("Test NRICH Short", *nrich.email_body(nrich.get_random_short_problem()))
    send_email(
        "Test Weekly STEP Assignment",
        *step.email_body(step.get_this_weeks_assignment(datetime.today()))
    )


def send_email(subject: str, body_html: str, body_plaintext: str) -> None:
    """Send an email to RECIPIENT"""
    try:
        response = ses.send_email(
            Destination={"ToAddresses": [RECIPIENT]},
            Message={
                "Body": {
                    "Html": {"Charset": "UTF-8", "Data": body_html},
                    "Text": {
                        "Charset": "UTF-8",
                        "Data": body_plaintext,
                    },
                },
                "Subject": {"Charset": "UTF-8", "Data": subject},
            },
            Source=SENDER,
        )
    except ClientError as error:
        app.log.error(
            "Sending email failed with error message %s",
            error.response["Error"]["Message"],
        )
    else:
        app.log.info("Email sent with MessageId %s", response["MessageId"])
