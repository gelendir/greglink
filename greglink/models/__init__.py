from greglink import db

from .status import Status
from .test_execution import TestExecution

def execution_with_status(testcase, status):
    status = db.session.query(Status).filter(Status.name == status).first()
    return TestExecution(id=testcase.id, status=status)

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


