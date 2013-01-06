from greglink import db
from datetime import datetime

def datetime_utc_now():
    return datetime.utcnow()

class TestExecution(db.Model):

    __tablename__ = 'test_executions'

    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime_utc_now)
    status_id = db.Column(db.Integer, db.ForeignKey('statuses.id'))

    status = db.relationship('Status')

    def __repr__(self):
        return "<TestExecution id:%s status_id:%s status:%s>" % (
                self.id,
                self.status_id,
                repr(self.status))
