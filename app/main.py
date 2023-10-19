from flask import Blueprint, render_template, redirect, url_for, request, flash
from sqlalchemy import text
from . import db
from flask_login import current_user, login_required

main = Blueprint("main", __name__)


@main.route("/")
def index():
    if current_user.is_authenticated:
        query = text("SELECT * FROM product")
        products = db.session.execute(query).fetchall()

        query = text("SELECT * FROM cart")
        carts = db.session.execute(query).fetchall()

        # get number of items in cart
        query = text("SELECT * FROM cart WHERE customer_id =" + str(current_user.id))

        cart = db.session.execute(query).fetchone()

        if cart is not None:
            query = text(
                "SELECT COUNT(*) FROM cart_product WHERE cart_id =" + str(cart.id)
            )
            number_of_items = db.session.execute(query).fetchone()[0]
        else:
            number_of_items = 0

        return render_template(
            "index.html", products=products, number_of_items=number_of_items
        )
    else:
        query = text("SELECT * FROM product")
        products = db.session.execute(query).fetchall()

        return render_template("index.html", products=products)


@main.route("/add_to_cart_index/<int:id>", methods=["POST"])
@login_required
def add_to_cart(id):
    if not current_user.is_authenticated:
        flash("You must be logged in to add items to your cart.", "error")
        return redirect("/")

    query = text("SELECT * FROM product WHERE id =" + str(id))
    product = db.session.execute(query).fetchone()

    query = text("SELECT * FROM cart WHERE customer_id =" + str(current_user.id))
    cart = db.session.execute(query).fetchone()

    query = text(
            "INSERT INTO cart_product (cart_id, product_id, quantity) VALUES ("
            + str(cart.id)
            + ","
            + str(product.id)
            + 
            "," + str(1) + 
            ")"
        )
    product_in_cart = db.session.execute(query).fetchone()

    if product_in_cart is None:
        query = text(
            "INSERT INTO cart_product (cart_id, product_id) VALUES ("
            + str(cart.id)
            + ","
            + str(product.id)
            + ")"
        )
        db.session.execute(query)
        db.session.commit()
        flash("Product added to cart!", "success")
    else:
        flash("Product already in cart!", "error")

    return redirect("/")

@main.route("/add_to_wishlist_index/<int:id>", methods=["GET"])
@login_required
def add_to_wishlist(id):
    if not current_user.is_authenticated:
        flash("You must be logged in to add items to your wishlist.", "error")
        return redirect("/")

    query = text("SELECT * FROM product WHERE id =" + str(id))
    product = db.session.execute(query).fetchone()

    query = text("SELECT * FROM wishlist WHERE customer_id =" + str(current_user.id))
    wishlist = db.session.execute(query).fetchone()

    query = text(
        "SELECT * FROM wishlist_product WHERE wishlist_id ="
        + str(wishlist.id)
        + " AND product_id ="
        + str(product.id)
    )
    product_in_wishlist = db.session.execute(query).fetchone()

    if product_in_wishlist is None:
        query = text(
            "INSERT INTO wishlist_product (wishlist_id, product_id) VALUES ("
            + str(wishlist.id)
            + ","
            + str(product.id)
            + ")"
        )
        db.session.execute(query)
        db.session.commit()
        flash("Product added to wishlist!", "success")
    else:
        flash("Product already in wishlist!", "error")

    return redirect("/")
