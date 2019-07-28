import unittest
import os
import json
import config
from main import app_factory
from database import db


class LeafLinkTestCase(unittest.TestCase):
    """This class represents the companies test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app_factory(config.Testing, config.project_name)
        self.client = self.app.test_client
        self.new_company = company = {"name":"New Company", "description":"A company", "company_type": "buyer"}
        self.updated_company = company = {"name":"Updated Company", "description":"A company", "company_type": "buyer"}
        self.comparison_company = {"id":1,"name":"New Company", "description":"A company", "company_type": "buyer", "products": [], "orders": []}
        self.updated_comparison_company = {"id":1,"name":"Updated Company", "description":"A company", "company_type": "buyer", "products": [], "orders": []}
        # binds the app to the current context
        with self.app.app_context():
            # drop and create all tables
            db.drop_all()
            db.create_all()

    def test_company_creation(self):
      res = self.client().post('/companies', data=self.new_company)
      self.assertEqual(res.status_code, 200)
      data = json.loads(res.data)
      for k, v in data.items():
        if type(v) == unicode:
          self.assertEqual(v.encode('utf-8'), self.comparison_company[k])
        else:
          self.assertEqual(v, self.comparison_company[k])

    def test_company_get_all(self):
      res = self.client().get('/companies')
      self.assertEqual(res.status_code, 200)
      get_all_data = json.loads(res.data)
      self.assertEqual(get_all_data, [])
      self.client().post('/companies', data=self.new_company)
      res = self.client().get('/companies')
      data = json.loads(res.data)
      self.assertEqual(res.status_code, 200)
      self.assertEqual(len(data), 1)
      for k, v in data[0].items():
        if type(v) == unicode:
          self.assertEqual(v.encode('utf-8'), self.comparison_company[k])
        else:
          self.assertEqual(v, self.comparison_company[k])

    def test_company_get_by_id(self):
      self.client().post('/companies', data=self.new_company)
      res = self.client().get('/companies/1')
      data = json.loads(res.data)
      self.assertEqual(res.status_code, 200)
      self.assertEqual(type(data), dict)
      for k, v in data.items():
        if type(v) == unicode:
          self.assertEqual(v.encode('utf-8'), self.comparison_company[k])
        else:
          self.assertEqual(v, self.comparison_company[k])

    def test_company_update(self):
      self.client().post('/companies', data=self.new_company)
      res = self.client().put('/companies/1', data=self.updated_company)
      data = json.loads(res.data)
      self.assertEqual(res.status_code, 200)
      self.assertEqual(type(data), dict)
      for k, v in data.items():
        if type(v) == unicode:
          self.assertEqual(v.encode('utf-8'), self.updated_comparison_company[k])
        else:
          self.assertEqual(v, self.updated_comparison_company[k])

    def test_company_delete(self):
      self.client().post('/companies', data=self.new_company)
      self.client().delete('/companies/1')
      res = self.client().get('/companies')
      data = json.loads(res.data)
      self.assertEqual(res.status_code, 200)
      self.assertEqual(len(data), 0)