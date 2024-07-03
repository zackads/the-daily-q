"""
Email maths problems etc. periodically
"""

import os
import boto3
from botocore.exceptions import ClientError
from chalice import Chalice, Cron

from chalicelib import problems
from chalicelib import algorithms

s3 = boto3.resource("s3")
s3_bucket = s3.Bucket(os.environ.get("S3_BUCKET_NAME", "the-daily-q"))

app = Chalice(app_name="the-daily-q")
ses = boto3.client("ses", region_name="eu-west-2")

# The first and only email address verified with SES, i.e. mine
email_address = ses.list_identities()["Identities"][0]
SENDER = "The Daily Q <" + email_address + ">"
RECIPIENT = email_address


@app.schedule(Cron(0, 6, "*", "*", "?", "*"))  # daily at 6am utc
def send_emails(event):
    send_email(
        "The Daily Q - Probability",
        *problems.email_body(problems.get_random_problem(s3_bucket, "problems/probability"))
    )
    send_email(
        "The Daily Q - Statistics",
        *problems.email_body(problems.get_random_problem(s3_bucket, "problems/statistics"))
    )
    send_email(
        "The Daily Q - Algorithms",
        *algorithms.email_body(algorithms.get_random_problem())
    )


@app.route("/test", methods=["GET"])
def send_test_email():
    """For testing"""
    send_email(
        "The Daily Q - Probability",
        *problems.email_body(problems.get_random_problem(s3_bucket, "problems/probability"))
    )
    send_email(
        "The Daily Q - Statistics",
        *problems.email_body(problems.get_random_problem(s3_bucket, "problems/statistics"))
    )
    send_email(
        "The Daily Q - Algorithms",
        *algorithms.email_body(algorithms.get_random_problem())
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
