"""
Email maths problems etc. periodically
"""

import os
from datetime import datetime, date

import boto3
from botocore.exceptions import ClientError
from chalice import Chalice, Cron

from chalicelib import a_level, nrich, step

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
    """Daily questions"""
    send_email(
        "The Daily Q", *a_level.email_body(a_level.get_random_question(s3_bucket))
    )
    send_email("NRICH Short", *nrich.email_body(nrich.get_random_short_problem()))

def days_until(future_date: datetime): 
    today = datetime.today()
    diff = future_date - today
    return diff.days + 1

def send_countdown(event):
    """Countdown to exams"""
    exam_dates = [
            { "name": "Further Core Pure 1", "date": datetime(2023, 5, 25)},
            { "name": "Further Core Pure 2", "date": datetime(2023, 6, 5)},
            { "name": "Maths Pure 1", "date": datetime(2023, 6, 6)},
            { "name": "Maths Pure 2", "date": datetime(2023, 6, 13)},
            { "name": "Maths Statistics & Mechanics", "date": datetime(2023, 6, 20)},
            { "name": "Further Decision 1", "date": datetime(2023, 6, 23)},
            { "name": "Further Decision 2", "date": datetime(2023, 6, 26)},
        ]

    message_body = "\n".join([f'{exam["name"]}: {days_until(exam["date"])} days until {exam["date"].strftime("%d %B")}' for exam in exam_dates])

    send_email("Daily exam countdown", message_body)

@app.schedule(Cron(0, 7, "?", "*", "MON", "*"))  # Every Monday at 7am UTC
def send_step_assignment(event):
    """Email an assignment from the STEP Support Programme"""
    send_email(
        "Weekly STEP Assignment",
        *step.email_body(step.get_this_weeks_assignment(datetime.today()))
    )


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
                    "Text": {"Charset": "UTF-8", "Data": body_plaintext, },
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
