import unittest
import os
import json
import config
from main import app_factory
from database import db


class BucketlistTestCase(unittest.TestCase):
    """This class represents the bucketlist test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app_factory(config.Testing, config.project_name)
        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            # drop and create all tables
            db.drop_all()
            db.create_all()

    def test_company_creation(self):
      company = {"name":"New Company", "description":"A company", "company_type": "buyer"}
      res = self.client().post('/companies', data=company)
      self.assertEqual(res.status_code, 200)
      comparison = {"id":1,"name":"New Company", "description":"A company", "company_type": "buyer", "products": [], "orders": []}
      self.assertEqual(json.loads(res.data), comparison)

    def test_company_get_all(self):
      res = self.client().get('/companies')
      self.assertEqual(res.status_code, 200)
      self.assertEqual(json.loads(res.data), [])
      company = {"name":"New Company", "description":"A company", "company_type": "buyer"}
      res = self.client().post('/companies', data=company)
      self.assertEqual(res.status_code, 200)
      self.assertEqual(len(json.loads(res.data)), 1)
