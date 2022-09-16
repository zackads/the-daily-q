"""
Email maths problems etc. periodically
"""

import datetime
import os
import boto3
from botocore.exceptions import ClientError
from chalice import Chalice, Cron

from chalicelib.step import email_current_step_assignment
from chalicelib.a_level import get_random_question, email_body

s3 = boto3.resource("s3")
s3_bucket = s3.Bucket(os.environ.get("S3_BUCKET_NAME", "the-daily-q"))

app = Chalice(app_name="the-daily-q")
ses = boto3.client("ses", region_name="eu-west-2")

# The first and only email address verified with SES, i.e. mine
email_address = ses.list_identities()["Identities"][0]
SENDER = "The Daily Q <" + email_address + ">"
RECIPIENT = email_address


@app.schedule(Cron(0, 7, "*", "*", "?", "*"))  # Daily at 7am UTC
def send_a_level_questions(event):
    """Email three A-level past paper questions"""
    subject = "The Daily Q"
    send_email(subject, *email_body(get_random_question(s3_bucket)))
    send_email(subject, *email_body(get_random_question(s3_bucket)))
    send_email(subject, *email_body(get_random_question(s3_bucket)))


@app.route("/test", methods=["GET"])
def send_test_email():
    """For testing"""
    return send_email("Test Email", *email_body(get_random_question(s3_bucket)))


@app.schedule(Cron(0, 7, "?", "*", "MON", "*"))  # Every Monday at 7am UTC
def send_step_assignment(event):
    """Email an assignment from the STEP Support Programme"""
    email_current_step_assignment(datetime.datetime.today())


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
        app.log.error("Sending email failed with error message %s",
                      error.response["Error"]["Message"])
    else:
        app.log.info("Email sent with MessageId %s", response["MessageId"])
