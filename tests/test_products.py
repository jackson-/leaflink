import unittest
import os
import json
import config
from main import app_factory
from database import db


class LeafLinkTestCase(unittest.TestCase):
    """This class represents the products test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app_factory(config.Testing, config.project_name)
        self.client = self.app.test_client
        self.company = {"name":"Seller Company", "description":"A selling company", "company_type": "seller"}
        self.product = {"name":"First Product", "description":"A first product", "price": 10.0, "company_id": 1}
        self.updated_product = {"name":"Updated Product", "description":"A first product", "price": 10.0, "company_id": 1}
        self.comparison_product = {
          "company": {
              "company_type": "seller",
              "description": "A selling company",
              "id": 1,
              "name": "Seller Company"
          },
          "description": "A first product",
          "id": 1,
          "name": "First Product",
          "price": 10.0
        }
        self.updated_comparison_product = {
          "company": {
              "company_type": "seller",
              "description": "A selling company",
              "id": 1,
              "name": "Seller Company"
          },
          "description": "A first product",
          "id": 1,
          "name": "Updated Product",
          "price": 10.0
        }
        # binds the app to the current context
        with self.app.app_context():
            # drop and create all tables
            db.drop_all()
            db.create_all()
            self.client().post('/companies', data=self.company)

    def test_product_creation(self):
      res = self.client().post('/products', data=self.product)
      self.assertEqual(res.status_code, 200)
      data = json.loads(res.data)
      for k, v in data.items():
        if type(v) == unicode:
          self.assertEqual(v.encode('utf-8'), self.comparison_product[k])
        else:
          self.assertEqual(v, self.comparison_product[k])

    def test_product_get_all(self):
      res = self.client().get('/products')
      self.assertEqual(res.status_code, 200)
      get_all_data = json.loads(res.data)
      self.assertEqual(get_all_data, [])
      self.client().post('/products', data=self.product)
      res = self.client().get('/products')
      data = json.loads(res.data)
      self.assertEqual(res.status_code, 200)
      self.assertEqual(len(data), 1)
      for k, v in data[0].items():
        if type(v) == unicode:
          self.assertEqual(v.encode('utf-8'), self.comparison_product[k])
        else:
          self.assertEqual(v, self.comparison_product[k])

    def test_product_get_by_id(self):
      self.client().post('/products', data=self.product)
      res = self.client().get('/products/1')
      data = json.loads(res.data)
      self.assertEqual(res.status_code, 200)
      self.assertEqual(type(data), dict)
      for k, v in data.items():
        if type(v) == unicode:
          self.assertEqual(v.encode('utf-8'), self.comparison_product[k])
        else:
          self.assertEqual(v, self.comparison_product[k])

    def test_product_update(self):
      self.client().post('/products', data=self.product)
      res = self.client().put('/products/1', data=self.updated_product)
      data = json.loads(res.data)
      self.assertEqual(res.status_code, 200)
      self.assertEqual(type(data), dict)
      for k, v in data.items():
        if type(v) == unicode:
          self.assertEqual(v.encode('utf-8'), self.updated_comparison_product[k])
        else:
          self.assertEqual(v, self.updated_comparison_product[k])

    def test_product_delete(self):
      self.client().post('/products', data=self.product)
      self.client().delete('/products/1')
      res = self.client().get('/products')
      data = json.loads(res.data)
      self.assertEqual(res.status_code, 200)
      self.assertEqual(len(data), 0)