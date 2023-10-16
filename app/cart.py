from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import User, Cart
from flask_login import current_user
from sqlalchemy import text
from . import db

shopping_cart = Blueprint("cart", __name__)

@shopping_cart.route("/cart", methods=["GET"])
def cart():
    query = text("SELECT * FROM cart WHERE customer_id =" + str(current_user.id))
    cart = db.session.execute(query).fetchone()

    query = text("SELECT * FROM product WHERE id IN (SELECT product_id FROM cart_product WHERE cart_id = " + str(cart.id) + ")")
    products = db.session.execute(query).fetchall()

    sub_total = sum([product.price for product in products])

    grand_total = sub_total + 3.99 + 4.99 # discount + shipping + tax

    return render_template("cart.html", products=products, sub_total=sub_total, grand_total=grand_total)