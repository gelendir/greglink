from greglink import db

from .status import Status
from .test_execution import TestExecution

def save_execution(execution, test_id):
    execution.test_id = test_id
    db.session.add(execution)
    db.session.commit()
    return execution

def save_success(testcase):
    test_id = testcase.id
    execution = TestExecution.with_success()
    return save_execution(execution, test_id)

def save_blocked(testcase):
    test_id = testcase.id
    execution = TestExecution.with_blocked()
    return save_execution(execution, test_id)

def save_failed(testcase):
    test_id = testcase.id
    execution = TestExecution.with_failed()
    return save_execution(execution, test_id)


