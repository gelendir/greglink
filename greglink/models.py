from greglink import db


class Status(db.Model):

    __tablename__ = 'statuses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return "<Status id:%s name:%s>" % (self.id, self.name)

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


def execution_with_status(testcase, status):
    status = db.session.query(Status).filter(Status.name == status).first()
    return TestExecution(id=testcase['id'], status=status)

def execution_success(testcase):
    return execution_with_status(testcase, "success")

def execution_blocked(testcase):
    return execution_with_status(testcase, "blocked")

def execution_failed(testcase):
    return execution_with_status(testcase, "failed")

def test_success(testcase):
    execution = execution_success(testcase)
    db.session.add(execution)
    db.session.commit()
    return execution

def test_blocked(testcase):
    execution = execution_blocked(testcase)
    db.session.add(execution)
    db.session.commit()
    return execution

def test_failed(testcase):
    execution = execution_failed(testcase)
    db.session.add(execution)
    db.session.commit()
    return execution

