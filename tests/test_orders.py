import unittest
import os
import json
import config
from main import app_factory
from database import db


class LeafLinkTestCase(unittest.TestCase):
    """This class represents the orders test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app_factory(config.Testing, config.project_name)
        self.client = self.app.test_client
        self.seller_company = {"name":"Seller Company", "description":"A selling company", "company_type": "seller"}
        self.buyer_company = {"name":"Buyer Company", "description":"A buying company", "company_type": "buyer"}
        self.product = {"name":"First Product", "description":"A first product", "price": 10.0, "company_id": 1}
        self.product2 = {"name":"Second Product", "description":"A second product", "price": 20.0, "company_id": 1}
        self.order = json.dumps({
          "buyer_id": 2, "seller_id": 1, 
          "line_items": [{"product_id": 1, "quantity": 3}, {"product_id": 2, "quantity": 1}]
        })
        self.comparison_order = {
            "buyer": {
                "company_type": "buyer",
                "description": "A buying company",
                "id": 2,
                "name": "Buyer company"
            },
            "id": 1,
            "line_items": [
                {
                    "product": {
                        "description": "A first product",
                        "id": 1,
                        "name": "First Product",
                        "price": 10
                    },
                    "quantity": 3,
                    "unit_price": 30
                },
                {
                    "product": {
                        "description": "A second product",
                        "id": 1,
                        "name": "Second Product",
                        "price": 20
                    },
                    "quantity": 1,
                    "unit_price": 20
                }
            ],
            "seller": {
                "company_type": "seller",
                "description": "A selling company",
                "id": 1,
                "name": "Seller Company"
            },
            "total":50
        }
        # binds the app to the current context
        with self.app.app_context():
            # drop and create all tables
            db.drop_all()
            db.create_all()
            self.client().post('/companies', data=self.seller_company)
            self.client().post('/companies', data=self.buyer_company)
            self.client().post('/products', data=self.product)
            self.client().post('/products', data=self.product2)

    def test_order_creation(self):
      res = self.client().post('/orders', data=self.order)
      self.assertEqual(res.status_code, 200)
      data = json.loads(res.data)
      self.assertEqual(len(data['line_items']), 2)
      self.assertEqual(data['total'], 50)
      self.assertEqual(data['seller']['id'], 1)
      self.assertEqual(data['buyer']['id'], 2)

    def test_order_get_all(self):
      res = self.client().get('/orders')
      self.assertEqual(res.status_code, 200)
      get_all_data = json.loads(res.data)
      self.assertEqual(get_all_data, [])
      self.client().post('/orders', data=self.order)
      res = self.client().get('/orders')
      data = json.loads(res.data)
      self.assertEqual(res.status_code, 200)
      self.assertEqual(len(data), 1)

    def test_order_get_by_id(self):
      self.client().post('/orders', data=self.order)
      res = self.client().get('/orders/1')
      data = json.loads(res.data)
      self.assertEqual(res.status_code, 200)
      self.assertEqual(type(data), dict)
      self.assertEqual(data['id'], 1)
      self.assertEqual(len(data['line_items']), 2)
      self.assertEqual(data['total'], 50)
      self.assertEqual(data['seller']['id'], 1)
      self.assertEqual(data['buyer']['id'], 2)

    def test_order_delete(self):
      self.client().post('/orders', data=self.order)
      self.client().delete('/orders/1')
      res = self.client().get('/orders')
      data = json.loads(res.data)
      self.assertEqual(res.status_code, 200)
      self.assertEqual(len(data), 0)