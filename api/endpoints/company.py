# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import render_template, flash, redirect, url_for
from sqlalchemy.exc import IntegrityError

from database import db

from api.models import Company, Product, LineItem, Order

app = Blueprint('companies', __name__)


@app.route("/")
def list_posts_view():
    companies = Company.query.all()
    return companies
