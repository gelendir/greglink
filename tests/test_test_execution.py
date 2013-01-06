import unittest

from datetime import datetime
from flask_test_case import FlaskTestCase
from greglink.models.test_execution import TestExecution
from greglink.models.status import Status

from greglink import db
from mock import patch


class TestTestExecution(FlaskTestCase):

    @patch('greglink.models.test_execution.datetime')
    def test_insert_test_execution(self, datetime_mock):
        utcnow = datetime(2000, 1, 2, 3, 4, 5)
        datetime_mock.utcnow.return_value = utcnow

        status = db.session.query(Status).first()

        execution = TestExecution(
            test_id = "test1",
            status = status
        )

        db.session.add(execution)
        db.session.commit()

        result = db.session.query(TestExecution).first()

        self.assertEquals(result.test_id, "test1")
        self.assertEquals(result.status_id, status.id)
        self.assertEquals(result.created_at, utcnow)

    def test_test_execution_with_statusname(self):
        execution = TestExecution.with_status("success")
        self.assertEquals(execution.status.name, "success")

    def test_test_execution_with_success(self):
        execution = TestExecution.with_success()
        self.assertEquals(execution.status.name, "success")

    def test_test_execution_with_blocked(self):
        execution = TestExecution.with_blocked()
        self.assertEquals(execution.status.name, "blocked")

    def test_test_execution_with_failed(self):
        execution = TestExecution.with_failed()
        self.assertEquals(execution.status.name, "failed")

if __name__ == "__main__":
    unittest.main()
