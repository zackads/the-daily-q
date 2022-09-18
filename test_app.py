"""Unit tests"""
import glob

from runtime.chalicelib.nrich import get_random_short_problem


def test_number_solutions_matches_number_questions():
    """The number of A-level solution files should match the number of questions"""
    count_questions = len(glob.glob("static/a_level/questions/*"))
    count_solutions = len(glob.glob("static/a_level/solutions/*"))

    assert count_questions == count_solutions


def test_nrich():
    """Get a random problem and assert it has a title and href"""
    problem = get_random_short_problem()

    assert len(problem["title"]) > 0
    assert problem["href"][0:8] == "https://"
