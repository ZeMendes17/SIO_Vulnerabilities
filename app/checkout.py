from sqlite3 import IntegrityError
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user
from .models import User, Cart, Order
from sqlalchemy import text
import json
from . import db



checkout = Blueprint("checkout", __name__)
order_id = 1


@checkout.route("/checkout", methods=["GET"])
def check():
    query = text("SELECT * FROM cart WHERE customer_id =" + str(current_user.id))
    cart = db.session.execute(query).fetchone()

    if cart is not None:
        query = text(
            "SELECT COUNT(*) FROM cart_product WHERE cart_id =" + str(cart.id)
        )
        number_of_items = db.session.execute(query).fetchone()[0]
    else:
        number_of_items = 0

    query = text("SELECT * FROM product WHERE id IN (SELECT product_id FROM cart_product WHERE cart_id = " + str(cart.id) + ")")
    products = db.session.execute(query).fetchall()




    subtotal = sum([product.price for product in products]) 
    grand_total = subtotal + 3.99 + 4.99 # tax + shipping
    #shipping = request.form["shipping-option"]

    product_list = []
    for product in products:
        product_dict = {
            "product_name": product[1],
            "price": product[2],
            "quantity": 1,      #product[3] - para já estático
            "image_name": product[4]
        }
        product_list.append(product_dict)

    return render_template("checkout.html", product_list=product_list, subtotal=subtotal, total=grand_total, shipping_cost=4.99, number_of_items=number_of_items)


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

    # Criar um novo Order
    new_order = Order(
        id=order_id,
        customer_id=current_user.id, 
        fname=fname, 
        lname=lname, 
        email=email, 
        shipping_address=address, 
        billing_address=address2, 
        country=country, 
        state=state,
        zip=zip,
        paymentMethod=paymentMethod, 
        cc_name=cc_name, 
        cc_number=cc_number, 
        cc_expiration=cc_expiration, 
        cc_cvv=cc_cvv, 
        shipping=shipping)
    
    try:
        # Adicionar o Order ao banco de dados
        db.session.add(new_order)
        db.session.commit()
        # Incrementar o ID do Order
        order_id += 1
        return redirect(url_for("main.index"))
    except IntegrityError:
        db.session.rollback()
        flash("Shipping Information incorrect!", "error")
        return redirect(url_for("checkout.check"))



