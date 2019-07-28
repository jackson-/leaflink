# -*- coding:utf-8 -*-
from database import db
from datetime import datetime
from flask import url_for


class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    company_type = db.Column(db.Text, nullable=False)
    products = db.relationship("Product", back_populates="company")

    def __repr__(self):
        """Display when printing a Company object"""
        return "<Company: {}>".format(self.name)


class Product(db.Model):
    """A Product class"""

    __tablename__ = "products"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    company = db.relationship("Company", back_populates="products")
    line_items = db.relationship("LineItem", back_populates="product")

    def __repr__(self):
        """Display when printing a Product object"""

        return "<Product: {}>".format(self.name)



class Order(db.Model):
    """A Order class"""

    __tablename__ = "orders"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    total = db.Column(db.Float)
    buyer_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    buyer = db.relationship("Company", foreign_keys=[buyer_id])
    seller = db.relationship("Company", foreign_keys=[seller_id])
    line_items = db.relationship("LineItem", back_populates="order", cascade="all, delete-orphan")


    def __repr__(self):
        """Display when printing a Order object"""

        return "<Order: {}>".format(self.name)


class LineItem(db.Model):
    """A LineItem class"""

    __tablename__ = 'lineitems'
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    quantity = db.Column(db.Integer)
    unit_price = db.Column(db.Float)
    product = db.relationship("Product", back_populates="line_items")
    order = db.relationship("Order", back_populates="line_items")

    def __repr__(self):
        """Display when printing a LineItem object"""

        return "<LineItem: {}>".format(self.name)