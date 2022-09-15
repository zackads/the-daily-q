import datetime
from chalice import Chalice, Cron

from chalicelib.a_level import email_random_a_level_question
from chalicelib.nrich import email_random_nrich_short_problem
from chalicelib.step import email_current_step_assignment

app = Chalice(app_name="the-daily-q")


@app.schedule(Cron(0, 7, "*", "*", "?", "*"))  # Daily at 7am UTC
def send_a_level_questions(event):
    email_random_a_level_question()
    email_random_a_level_question()
    email_random_a_level_question()
    email_random_nrich_short_problem()


@app.schedule(Cron(0, 7, "?", "*", "MON", "*"))  # Every Monday at 7am UTC
def send_step_assignment(event):
    email_current_step_assignment(datetime.datetime.today())
