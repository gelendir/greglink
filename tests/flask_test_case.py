import unittest
from greglink import app, database


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['TESTING'] = True
        self.app = app.test_client()
        database.init_db()

    def tearDown(self):
        database.destroy_db()

