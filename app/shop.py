from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import User
from sqlalchemy import text
from . import db

shops = Blueprint("shops", __name__)


@shops.route("/shop", methods=["GET"])
def shop():
    query = text("SELECT * FROM product")
    products = db.session.execute(query).fetchall()

    print(products)

    return render_template("shop.html", products=products)
