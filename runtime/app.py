import os
import boto3
from chalice import Chalice, Cron

from runtime.a_level import email_random_a_level_question

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
    email_random_a_level_question()
    email_random_a_level_question()
    email_random_a_level_question()