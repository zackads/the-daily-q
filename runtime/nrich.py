import json
from random import choice

import boto3
from botocore.exceptions import ClientError

ses = boto3.client("ses", region_name="eu-west-2")

# The first and only email address verified with SES, i.e. mine
email_address = ses.list_identities()["Identities"][0]

SENDER = "The Daily Q <" + email_address + ">"
RECIPIENT = email_address
SUBJECT = "NRICH Short: "

def email_random_nrich_short_problem():
    problem = get_random_short_problem()

    try:
        response = ses.email_current_step_assignment(
            Destination={"ToAddresses": [RECIPIENT]},
            Message={
                "Body": {
                    "Html": {"Charset": "UTF-8", "Data": body_html(problem['title'], problem['href'])},
                    "Text": {
                        "Charset": "UTF-8",
                        "Data": body_plaintext(problem['title'], problem['href']),
                    },
                },
                "Subject": {"Charset": "UTF-8", "Data": SUBJECT + problem['title']},
            },
            Source=SENDER,
        )
    except ClientError as e:
        return e.response["Error"]["Message"]
    else:
        return "Email sent! Message ID: ", response["MessageId"]

def get_random_short_problem():
    """Short problems from https://nrich.maths.org/11993"""

    with open('static/nrich/short_problems.json', 'r') as f:
        problems = json.load(f)

    return choice(problems)

def body_html(problem_title, problem_url):
    return """<html>
<head></head>
<body>
    <a href="{}"><h1>{}</h1></a>
</body>
</html>
""".format(
        problem_url, problem_title
    )


def body_plaintext(problem_title, problem_url):
    return "Daily NRICH Short" f"{problem_title}: {problem_url}"