import markdown
import os

from greglink import app

DELIMITER = "---\n"
FILE_EXTENSION = "md"

def parse_line(line):
    parts = line.partition(":")
    return (parts[0].strip(), parts[2].strip())


def extract_header(testfile):
    headers = {}

    line = testfile.readline()
    while line and line != DELIMITER:
        line = testfile.readline()

    if not line:
        raise Exception("no headers found in file")

    line = testfile.readline().decode('utf8')
    key, value = parse_line(line)
    headers[key] = value

    while line and line != DELIMITER:
        key, value = parse_line(line)
        headers[key] = value
        line = testfile.readline().decode('utf8')

    return headers


def parse_testfile(testfile):
    testcase = extract_header(testfile)

    content = testfile.read().decode('utf8').strip()
    html = markdown.markdown(content)

    testcase['content'] = html

    return testcase


def find_test(id):
    files = os.listdir(app.config['TEST_ROOT'])

    filename = "%s.%s" % (id, FILE_EXTENSION)

    if filename not in files:
        return None

    filepath = os.path.join(app.config['TEST_ROOT'], filename)

    with open(filepath) as testfile:
        testcase = parse_testfile(testfile)

    return testcase

