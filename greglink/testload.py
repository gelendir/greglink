import os

from greglink import app
from greglink.models.testcase import TestCase
from greglink.models.testfile import load_testfile

EXTENSION = "md"

class NoHeaderInTestFile(Exception):
    pass

def root_path():
    return app.config['TEST_ROOT']

def path_to_filepath(path):
    parts = path.split("/")
    filepath = os.path.join(root_path(), *parts)
    return filepath

def path_exists(path):
    filepath = path_to_filepath(path)
    if not os.path.exists(filepath):
        return False
    return True

def find_test(path):
    filepath = path_to_filepath(path)
    if not os.path.exists(filepath):
        return None

    return load_test(path, filepath)

def load_test(path, filepath):
    with open(filepath) as testfile:
        header, markup = load_testfile(testfile)

    if not header:
        raise NoHeaderInTestFile("Test file %s has no header" % filepath)

    return TestCase(path, header, markup)

def all_testfiles(dirpath):
    if not os.path.exists(dirpath):
        return []

    return (f for f in os.listdir(dirpath) if f.endswith(EXTENSION))

def all_tests(path='/'):
    dirpath = path_to_filepath(path)
    tests = []

    for filename in all_testfiles(dirpath):
        filepath = os.path.join(dirpath, filename)
        clean_path = [x for x in path.strip("/").split("/") if x]
        urlpath = "/" + "/".join(clean_path + [filename])

        testcase = load_test(urlpath, filepath)
        tests.append(testcase)

    return tests

