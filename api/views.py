# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import render_template, flash, redirect, url_for, jsonify, abort
from flask_apispec import marshal_with
# from flask_restful import marshal_with as marshal_with2
from sqlalchemy.exc import IntegrityError
from webargs import fields
from webargs.flaskparser import use_kwargs

from database import db

from schemas import CompanySchema, ProductSchema, OrderSchema


from api.models import Company, Product, LineItem, Order

app = Blueprint('leaflink', __name__)

@app.route("/", methods=["GET"])
def route_api_health_check():
    return jsonify(success=True)  


############################ COMPANIES ##################################


@app.route("/companies", methods=["GET"])
@marshal_with(CompanySchema(many=True))
def route_company_get_all():
    companies = db.session.query(Company).all()
    return companies


@app.route("/companies/<int:company_id>", methods=["GET"])
@marshal_with(CompanySchema())
def route_company_get_by_id(company_id):
    company = Company.query.filter(Company.id == company_id).first()
    if not company:
      return abort(400, "The company with id: {0} does not exists".format(company_id))
    return company


@app.route("/companies", methods=["POST"])
@marshal_with(CompanySchema())
@use_kwargs(
    {
        "name": fields.Str(),
        "description": fields.Str(),
        "company_type": fields.Str(),
    }
)
def route_company_create(name, description, company_type):
    if company_type.lower() not in ["buyer", "seller"]:
        return abort(400, "{0} is not a valid company type. Please choose buyer or seller.".format(company_type))
    company = Company(
        name=name,
        description=description,
        company_type=company_type,
    )
    db.session.add(company)
    db.session.commit()
    db.session.refresh(company)
    return company


@app.route("/companies/<int:company_id>", methods=["PUT"])
@marshal_with(CompanySchema())
@use_kwargs(
    {
        "name": fields.Str(),
        "description": fields.Str(),
        "company_type": fields.Str(),
    }
)
def route_company_update(company_id, **kwargs):
    company = Company.query.filter(Company.id == company_id).first()
    for key, val in kwargs.items():
        if val is not None:
            setattr(company, key, val)
    db.session.add(company)
    db.session.commit()
    db.session.refresh(company)
    return company

@app.route("/companies/<int:company_id>", methods=["DELETE"])
def route_company_delete(company_id):
    company = Company.query.filter(Company.id == company_id).first()
    db.session.delete(company)
    db.session.commit()
    return jsonify(success=True)


############################ PRODUCTS ##################################


@app.route("/products", methods=["GET"])
@marshal_with(ProductSchema(many=True))
def route_product_get_all():
    products = db.session.query(Product).all()
    return products


@app.route("/products/<int:product_id>", methods=["GET"])
@marshal_with(ProductSchema())
def route_product_get_by_id(product_id):
    product = Product.query.filter(Product.id == product_id).first()
    if not product:
      return abort(400, "The product with id: {0} does not exists".format(product_id))
    return product


@app.route("/products", methods=["POST"])
@marshal_with(ProductSchema())
@use_kwargs(
    {
        "name": fields.Str(),
        "description": fields.Str(),
        "price": fields.Float(),
        "company_id": fields.Int(),
    }
)
def route_product_create(name, description, price, company_id):
    company = Company.query.filter(Company.id == company_id).first()
    product = Product(
        name=name,
        description=description,
        price=price,
        company=company
    )
    db.session.add(product)
    db.session.commit()
    db.session.refresh(product)
    return product


@app.route("/products/<int:product_id>", methods=["PUT"])
@marshal_with(ProductSchema())
@use_kwargs(
    {
        "name": fields.Str(),
        "description": fields.Str(),
        "price": fields.Float(),
    }
)
def route_product_update(product_id, **kwargs):
    product = Product.query.filter(Product.id == product_id).first()
    for key, val in kwargs.items():
        if val is not None:
            setattr(product, key, val)
    db.session.add(product)
    db.session.commit()
    db.session.refresh(product)
    return product

@app.route("/products/<int:product_id>", methods=["DELETE"])
def route_product_delete(product_id):
    product = Product.query.filter(Product.id == product_id).first()
    db.session.delete(product)
    db.session.commit()
    return jsonify(success=True)


############################ ORDER ##################################


@app.route("/orders", methods=["GET"])
@marshal_with(OrderSchema(many=True))
def route_order_get_all():
    orders = db.session.query(Order).all()
    return orders


@app.route("/orders/<int:order_id>", methods=["GET"])
@marshal_with(OrderSchema())
def route_order_get_by_id(order_id):
    order = Order.query.filter(Order.id == order_id).first()
    if not order:
      return abort(400, "The order with id: {0} does not exists".format(order_id))
    return order


@app.route("/orders", methods=["POST"])
@marshal_with(OrderSchema())
@use_kwargs(
    {
        "buyer_id": fields.Int(),
        "seller_id": fields.Int(),
        "line_items": fields.List(fields.Dict()),
    }
)
def route_order_create(buyer_id, seller_id, line_items):
    order = Order(buyer_id=buyer_id, seller_id=seller_id, line_items=[])
    for li in line_items:
      product = Product.query.filter(Product.id == li['product_id']).first()
      item = LineItem(
        product=product, 
        order=order,
        quantity=li['quantity'],
        unit_price=li['quantity'] * product.price
      )
      order.line_items.append(item)
    db.session.add(order)
    db.session.commit()
    db.session.refresh(order)
    return order


@app.route("/orders/<int:order_id>", methods=["PUT"])
@marshal_with(OrderSchema())
@use_kwargs(
    {
        "name": fields.Str(),
        "description": fields.Str(),
        "price": fields.Float(),
    }
)
def route_order_update(order_id, **kwargs):
    order = Order.query.filter(Order.id == order_id).first()
    for key, val in kwargs.items():
        if val is not None:
            setattr(order, key, val)
    db.session.add(order)
    db.session.commit()
    db.session.refresh(order)
    return order

@app.route("/orders/<int:order_id>", methods=["DELETE"])
def route_order_delete(order_id):
    order = Order.query.filter(Order.id == order_id).first()
    db.session.delete(order)
    db.session.commit()
    return jsonify(success=True)  