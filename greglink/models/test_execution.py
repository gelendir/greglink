from greglink import db

class TestExecution(db.Model):

    __tablename__ = 'test_executions'

    id = db.Column(db.String, primary_key=True)
    status_id = db.Column(db.Integer, db.ForeignKey('statuses.id'))
    status = db.relationship('Status')

    def __repr__(self):
        return "<TestExecution id:%s status_id:%s status:%s>" % (
                self.id,
                self.status_id,
                repr(self.status))
