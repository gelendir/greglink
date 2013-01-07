import os

from greglink import app
from greglink.models.testcase import TestCase
from greglink.models.testfile import load_testfile

EXTENSION = "md"

class NoHeaderInTestfile(Exception):
    pass

def root_path():
    return app.config['TEST_ROOT']

def urlpath_to_filepath(urlpath):
    filepath = os.path.join(root_path(), urlpath)
    return filepath

def find_test(urlpath):
    filepath = urlpath_to_filepath(urlpath)
    if not os.path.exists(filepath):
        return None

    return load_test(filepath, urlpath)

def load_test(filepath, urlpath):
    with open(filepath) as testfile:
        header, markup = load_testfile(testfile)

    if not header:
        raise NoHeaderInTestfile("Test file %s has no header" % filepath)

    return TestCase(urlpath, header, markup)

def all_tests(dirpath='/'):
    parts = dirpath.split("/")
    dirpath = os.path.join(root_path(), *parts)
    print root_path()
    print dirpath
    if not os.path.exists(dirpath):
        return []

    files = os.listdir(dirpath)
    tests = []

    for filename in (f for f in files if f.endswith(".md")):

        filepath = os.path.join(dirpath, filename)
        urlpath = filepath[len(root_path()):]

        testcase = load_test(filepath, urlpath)
        tests.append(testcase)

    return tests

