from flask import Blueprint
from flask import render_template, flash, redirect, url_for, jsonify, abort
from flask_apispec import marshal_with
from sqlalchemy.exc import IntegrityError
from webargs import fields
from webargs.flaskparser import use_kwargs

from database import db

from api.schemas import CompanySchema, ProductSchema, OrderSchema


from api.models import Company, Product, LineItem, Order

app = Blueprint('companies', __name__)

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