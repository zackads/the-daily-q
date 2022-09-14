from datetime import datetime

import boto3
from botocore.exceptions import ClientError

ses = boto3.client("ses", region_name="eu-west-2")

# The first and only email address verified with SES, i.e. mine
email_address = ses.list_identities()["Identities"][0]

SENDER = "STEP Assignment <" + email_address + ">"
RECIPIENT = email_address
SUBJECT = "The Weekly STEP Assignment"

def email_current_step_assignment(today: datetime.date):
    assignment = get_this_weeks_assignment(today)

    try:
        response = ses.send_email(
            Destination={"ToAddresses": [RECIPIENT]},
            Message={
                "Body": {
                    "Html": {"Charset": "UTF-8", "Data": body_html(assignment)},
                    "Text": {
                        "Charset": "UTF-8",
                        "Data": body_plaintext(assignment),
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


def get_this_weeks_assignment(today: datetime.date):
    start = datetime(2022, 9, 12)
    current_assignment_index = (today - start).days // 7

    assignments = [
        "https://maths.org/step/assignments/assignment-1",
        "https://maths.org/step/assignments/assignment-2",
        "https://maths.org/step/assignments/assignment-3",
        "https://maths.org/step/assignments/assignment-4",
        "https://maths.org/step/assignments/assignment-5",
        "https://maths.org/step/assignments/assignment-6",
        "https://maths.org/step/assignments/assignment-7",
        "https://maths.org/step/assignments/assignment-8",
        "https://maths.org/step/assignments/assignment-9",
        "https://maths.org/step/assignments/assignment-10",
        "https://maths.org/step/assignments/assignment-11",
        "https://maths.org/step/assignments/assignment-12",
        "https://maths.org/step/assignments/assignment-13",
        "https://maths.org/step/assignments/assignment-14",
        "https://maths.org/step/assignments/assignment-15",
        "https://maths.org/step/assignments/step-support-assignment-16",
        "https://maths.org/step/assignments/step-support-assignment-17",
        "https://maths.org/step/assignments/step-support-assignment-18",
        "https://maths.org/step/assignments/step-support-assignment-19",
        "https://maths.org/step/assignments/step-support-assignment-20",
        "https://maths.org/step/assignments/step-support-assignment-21",
        "https://maths.org/step/assignments/step-support-assignment-22",
        "https://maths.org/step/assignments/step-support-assignment-23",
        "https://maths.org/step/assignments/step-support-assignment-24",
        "https://maths.org/step/assignments/step-support-assignment-25",
        "https://maths.org/step/assignments/mixed-statistics-step-1-questions",
        "https://maths.org/step/assignments/mixed-mechanics-step-1-questions",
        "https://maths.org/step/assignments/mixed-pure-step-1-questions",
        "https://maths.org/step/step-2-calculus",
        "https://maths.org/step/step-2-curve-sketching",
        "https://maths.org/step/step-2-equations-and-inequalities",
        "https://maths.org/step/step-2-trigonometry",
        "https://maths.org/step/step-2-vectors",
        "https://maths.org/step/step-2-mechanics",
        "https://maths.org/step/step-2-statistics",
        "https://maths.org/step/step-2-miscellaneous-pure",
        "https://maths.org/step/step-2-matrices",
        "https://maths.org/step/step-2-complex-numbers-0",
        "https://maths.org/step/step-3-algebra",
        "https://maths.org/step/step-3-calculus",
        "https://maths.org/step/step-3-complex-numbers",
        "https://maths.org/step/step-3-coordinate-geometry-including-polar-coordinates",
        "https://maths.org/step/step-3-differential-equations",
        "https://maths.org/step/step-3-hyperbolic-functions",
        "https://maths.org/step/step-3-matrices-0",
        "https://maths.org/step/step-3-mechanics",
        "https://maths.org/step/step-3-statistics",
        "https://maths.org/step/step-3-vectors",
        "https://maths.org/step/various-mixed-step-3-pure-questions"
    ]

    return assignments[current_assignment_index]


def body_html(assignment_url):
    return """<html>
<head></head>
<body>
    <h1>Weekly STEP Assignment</h1>
    <a href="{}">Solution</a>
</body>
</html>
""".format(
        assignment_url
    )


def body_plaintext(assignment_url):
    return "Weekly STEP Assignment" f"{assignment_url}"
