from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import User, Cart
from flask_login import current_user, login_required
from sqlalchemy import text
from . import db

shopping_cart = Blueprint("cart", __name__)

@shopping_cart.route("/cart", methods=["GET"])
def cart():
    query = text("SELECT * FROM cart") 
    carts = db.session.execute(query).fetchall()

    print("--------------------")
    print(carts)
    print("--------------------")


    #print(current_user.id)
    query = text("SELECT * FROM cart WHERE customer_id =" + str(current_user.id))
    cart = db.session.execute(query).fetchone()

    """ print("--------------------")
    print(cart)
    print("--------------------") """

    if cart is not None:
        query = text(
            "SELECT COUNT(*) FROM cart_product WHERE cart_id =" + str(cart.id)
        )
        number_of_items = db.session.execute(query).fetchone()[0]
    else:
        number_of_items = 0

    query = text("SELECT * FROM product WHERE id IN (SELECT product_id FROM cart_product WHERE cart_id = " + str(cart.id) + ")")
    products = db.session.execute(query).fetchall()

    sub_total = sum([product.price for product in products])

    grand_total = sub_total + 3.99 + 4.99 # discount + shipping + tax

    return render_template("cart.html", products=products, sub_total=sub_total, grand_total=grand_total, number_of_items=number_of_items)

@shopping_cart.route("/cart/remove_product/<int:product_id>", methods=["GET"])
@login_required
def remove_product(product_id):
    if not current_user.is_authenticated:
        flash("Você precisa estar logado para gerenciar seu carrinho.", "error")
        return redirect(url_for("auth.login"))

    query = text("SELECT * FROM cart WHERE customer_id =" + str(current_user.id))
    cart = db.session.execute(query).fetchone()

    if cart is None:
        flash("Seu carrinho está vazio.", "info")
        return redirect(url_for("cart.cart"))

    query = text(
        "DELETE FROM cart_product WHERE cart_id = :cart_id AND product_id = :product_id"
    )
    db.session.execute(query, {"cart_id": cart.id, "product_id": product_id})
    db.session.commit()

    flash("Produto removido do carrinho.", "success")
    return redirect(url_for("cart.cart"))
