from flask import Blueprint
from flask import render_template, flash, redirect, url_for, jsonify, abort
from flask_apispec import marshal_with
from sqlalchemy.exc import IntegrityError
from webargs import fields
from webargs.flaskparser import use_kwargs

from database import db

from api.schemas import CompanySchema, ProductSchema, OrderSchema


from api.models import Company, Product, LineItem, Order

app = Blueprint('products', __name__)

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

