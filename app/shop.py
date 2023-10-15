from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import User
from sqlalchemy import text
from . import db

shops = Blueprint("shops", __name__)


@shops.route("/shop", methods=["GET", "POST"])
def shop():
    if request.method == "GET":
        query = text("SELECT * FROM product")
        products = db.session.execute(query).fetchall()

        print(products)

        return render_template("shop.html", products=products)
    
    else: #POST
        print("POST")
        if 'search' in request.form:
            search_value = request.form['search_value']
            query = text("SELECT * FROM product WHERE name LIKE :search")
            products = db.session.execute(query, {"search": "%" + search_value + "%"}).fetchall()

            return render_template("shop.html", products=products, default_value=search_value.strip())