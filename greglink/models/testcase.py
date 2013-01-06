from greglink.models.testfile import load_testfile, convert_markup
from greglink import db
from greglink.models.status import Status
from greglink.models.test_execution import TestExecution


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
        status = (
                    db.session.query(Status.name)
                    .join(TestExecution)
                    .filter(TestExecution.test_id == self.id)
                    .order_by(TestExecution.created_at.desc())
                    .first())

        if status:
            return status[0]
        return None


def load_file(filepath):
    with open(filepath) as testfile:
        header, markup = load_testfile(testfile)

    if not header:
        raise NoHeaderInTestfile("Test file %s has no header" % filepath)
    return TestCase(filepath, header, markup)

