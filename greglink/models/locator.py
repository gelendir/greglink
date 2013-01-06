import os

from greglink import app
from greglink.models.testcase import load_file

EXTENSION = "md"

def all_tests():
    files = os.listdir(app.config['TEST_ROOT'])
    tests = []

    for filename in files:
        filepath = os.path.join(app.config['TEST_ROOT'], filename)
        testcase = load_file(filepath)
        tests.append(testcase)

    return tests


def find_test(id):
    filename = "%s.%s" % (id, EXTENSION)
    filepath = os.path.join(app.config['TEST_ROOT'], filename)

    if not os.path.exists(filepath):
        return None

    return load_file(filepath)
