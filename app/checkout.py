from sqlite3 import IntegrityError
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user
from .models import User
from sqlalchemy import text
import json
from . import db


checkout = Blueprint("checkout", __name__)


@checkout.route("/checkout")
def check():
    return render_template("checkout.html")


@checkout.route("/form_checkout", methods=["POST"])
def form_checkout():
    fname = request.form["firstname"]
    lname = request.form["lastname"]
    user = request.form["username"]
    email = request.form["email"]
    address = request.form["address"]
    address2 = request.form["address2"]
    country = request.form["country"]
    state = request.form["state"]
    zip = request.form["zip"]
    paymentMethod = request.form["paymentMethod"]
    cc_name = request.form["cc-name"]
    cc_number = request.form["cc-number"]
    cc_expiration = request.form["cc-expiration"]
    cc_cvv = request.form["cc-cvv"]
    shipping = request.form["shipping-option"]

    cursor = db.connection.cursor()
    cursor.execute("SELECT product_name, price FROM products")
    products = cursor.fetchall()

    product_list = []
    for product in products:
        product_dict = {
            "product_name": product[0],
            "price": product[1]
        }
        product_list.append(product_dict)


    # Adicionar atributos à tabela de Order
    # Esperar

    return render_template("checkout.html", product_list=json.dumps(product_list))



