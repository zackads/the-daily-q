from os import walk
import glob


def test_static_files():
    count_questions = len(glob.glob("static/questions/*"))
    count_solutions = len(glob.glob("static/solutions/*"))

    assert count_questions == count_solutions