import markdown
import yaml

ENCODING = 'utf8'
DELIMITER = "---"
FILE_EXTENSION = "md"


def load_testfile(testfile):
    raw_header = extract_header(testfile)
    header = parse_header(raw_header)
    markup = extract_markup(testfile)

    return header, markup

def extract_header(testfile):
    header_lines = []

    #Skip anything before header delimiter
    for line in read_lines(testfile):
        if line == DELIMITER:
            break

    #Accumulate lines until header delimiter
    for line in read_lines(testfile):
        if line == DELIMITER:
            return "\n".join(header_lines)
        header_lines.append(line)

    return ""

def read_lines(testfile):
    line = testfile.readline()
    while line:
        yield convert_line(line)
        line = testfile.readline()

def convert_line(line):
    return line.decode(ENCODING).strip()

def parse_header(raw_header):
    return yaml.load(raw_header)

def extract_markup(testfile):
    markup = testfile.read().decode(ENCODING).strip()
    return markup

def convert_markup(raw_markup):
    return markdown.markdown(raw_markup)

