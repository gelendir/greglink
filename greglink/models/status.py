from greglink import db
from greglink.models.test_execution import TestExecution

class Status(db.Model):

    __tablename__ = 'statuses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return "<Status id:%s name:%s>" % (self.id, self.name)


def status_name(test_id):
    status = (
                db.session.query(Status.name).
                join(TestExecution).
                filter(TestExecution.id == test_id).
                first())

    if status:
        return status[0]
    return None
