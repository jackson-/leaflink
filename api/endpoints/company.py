# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import render_template, flash, redirect, url_for
from flask_restful import marshal_with
from sqlalchemy.exc import IntegrityError

from database import db

from api.models import Company, Product, LineItem, Order
from api.schemas.company import CompanySchema


app = Blueprint('companies', __name__)

@marshal_with(CompanySchema(many=True))
@app.route("/")
def list_posts_view():
    companies = Company.query.all()
    return {"companies": companies}
