from greglink.models.testfile import load_testfile, convert_markup
from greglink.models.status import status_name


class NoHeaderInTestfile(Exception):
    pass


class TestCase(object):

    def __init__(self, filepath, header, markup):
        self.filepath = filepath
        self.header = header
        self.markup = markup

    @property
    def id(self):
        return self.header['id']

    @property
    def title(self):
        return self.header['title']

    @property
    def filename(self):
        return self.filepath.rpartition("/")[2]

    @property
    def urlid(self):
        return self.filename.rpartition(".")[0]

    def to_html(self):
        return convert_markup(self.markup)

    def status_name(self):
        return status_name(self.id)


def load_file(filepath):
    with open(filepath) as testfile:
        header, markup = load_testfile(testfile)

    if not header:
        raise NoHeaderInTestfile("Test file %s has no header" % filepath)
    return TestCase(filepath, header, markup)

