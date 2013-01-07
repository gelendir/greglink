from greglink.models.testfile import convert_markup
from greglink import db
from greglink.models.status import Status
from greglink.models.test_execution import TestExecution


class TestCase(object):

    def __init__(self, urlpath, header, markup):
        self.urlpath = urlpath
        self.header = header
        self.markup = markup

    @property
    def id(self):
        return self.header['id']

    @property
    def title(self):
        return self.header['title']

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

