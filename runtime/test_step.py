from datetime import datetime

import pytest

from runtime.step import get_this_weeks_assignment


def test_get_this_weeks_assignment():
    first_week = [
        datetime(2022, 9, 12),
        datetime(2022, 9, 13),
        datetime(2022, 9, 14),
        datetime(2022, 9, 15),
        datetime(2022, 9, 16),
        datetime(2022, 9, 17),
        datetime(2022, 9, 18),
    ]
    for day in first_week:
        assert get_this_weeks_assignment(day) == "https://maths.org/step/assignments/assignment-1"

    second_week = [
        datetime(2022, 9, 19),
        datetime(2022, 9, 20),
        datetime(2022, 9, 21),
        datetime(2022, 9, 22),
        datetime(2022, 9, 23),
        datetime(2022, 9, 24),
    ]

    for day in second_week:
        assert get_this_weeks_assignment(day) == "https://maths.org/step/assignments/assignment-2"

    last_week = [
        datetime(2023, 8, 14),
        datetime(2023, 8, 15),
        datetime(2023, 8, 16),
        datetime(2023, 8, 17),
        datetime(2023, 8, 18),
        datetime(2023, 8, 19),
        datetime(2023, 8, 20),
    ]
    for day in last_week:
        assert get_this_weeks_assignment(day) == \
               "https://maths.org/step/various-mixed-step-3-pure-questions"

    with pytest.raises(IndexError):
        no_more_assignments_date = datetime(2023, 8, 21)
        get_this_weeks_assignment(no_more_assignments_date)
