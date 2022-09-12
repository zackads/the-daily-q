from os import walk
import glob


def test_static_files():
    count_questions = len(glob.glob("static/a_level/questions/*"))
    count_solutions = len(glob.glob("static/a_level/solutions/*"))

    assert count_questions == count_solutions