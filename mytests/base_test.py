import os
basedir = os.path.abspath(os.path.dirname(__file__))
print basedir
import unittest
from app import app, db
 
# My custom base class.  All tests that inherit from this class will have
#    a database setup for them before the tests begin
class BaseTest(unittest.TestCase):
    @classmethod
    def setUp(self):
        app.config.from_object('config.TestingConfig')
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
        self.ctx = app.test_request_context()
    @classmethod
    def tearDown(self):
        db.session.remove()
