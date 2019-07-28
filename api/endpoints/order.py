from flask import Blueprint
from flask import render_template, flash, redirect, url_for, jsonify, abort
from flask_apispec import marshal_with
from sqlalchemy.exc import IntegrityError
from webargs import fields
from webargs.flaskparser import use_kwargs

from database import db

from api.schemas import CompanySchema, ProductSchema, OrderSchema


from api.models import Company, Product, LineItem, Order

app = Blueprint('orders', __name__)


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
    total = 0
    for li in line_items:
      product = Product.query.filter(Product.id == li['product_id']).first()
      total += li['quantity'] * product.price
      item = LineItem(
        product=product, 
        order=order,
        quantity=li['quantity'],
        unit_price=li['quantity'] * product.price
      )
      order.line_items.append(item)
    order.total = total
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