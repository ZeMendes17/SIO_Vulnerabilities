from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from sqlalchemy import text
from . import db

shopping_cart = Blueprint("cart", __name__)


@shopping_cart.route("/cart", methods=["GET"])
@login_required
def cart():
    query = text("SELECT * FROM cart WHERE customer_id =" + str(current_user.id))
    cart = db.session.execute(query).fetchone()

    if cart is not None:
        query = text("SELECT COUNT(*) FROM cart_product WHERE cart_id =" + str(cart.id))
        number_of_items = db.session.execute(query).fetchone()[0]
    else:
        number_of_items = 0

    query = text(
        "SELECT * FROM product WHERE id IN (SELECT product_id FROM cart_product WHERE cart_id = "
        + str(cart.id)
        + ")"
    )
    products = db.session.execute(query).fetchall()

    # get product quantity from cart_product table

    product_quantities = {}

    for product in products:
        print(product.id)
        query = text(
            "SELECT quantity FROM cart_product WHERE cart_id = "
            + str(cart.id)
            + " AND product_id = "
            + str(product.id)
        )
        product_quantity = db.session.execute(query).fetchone()

        # Store the product quantity in the dictionary using the product id as the key
        if product_quantity:
            product_quantities[product.id] = product_quantity[0]
        else:
            # If the product doesn't exist in the cart_product table, assume a quantity of 0
            product_quantities[product.id] = 0

    # Calculate the sub_total using the product quantities
    sub_total = sum(
        product.price * product_quantities[product.id]
        if product_quantities[product.id] is not None
        else 0
        for product in products
    )

    grand_total = sub_total + 3.99 + 4.99  # discount + shipping + tax

    return render_template(
        "cart.html",
        products=products,
        sub_total=sub_total,
        grand_total=grand_total,
        number_of_items=number_of_items,
        product_quantities=product_quantities,
    )


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


@shopping_cart.route("/cart/update_cart", methods=["POST"])
@login_required
def update_cart():
    if not current_user.is_authenticated:
        flash("You need to be logged in to manage your cart.", "error")
        return redirect(url_for("auth.login"))

    query = text("SELECT * FROM cart WHERE customer_id =" + str(current_user.id))
    cart = db.session.execute(query).fetchone()

    if cart is None:
        flash("Your cart is empty.", "info")
        return redirect(url_for("cart.cart"))

    for product_id in request.form:
        id = product_id.split("_")[1]

        if request.form[product_id].isnumeric() == False:
            flash("Invalid quantity.", "error")
            return redirect(url_for("cart.cart"))

        query = text(
            "UPDATE cart_product SET quantity = "
            + request.form[product_id]
            + " WHERE cart_id = "
            + str(cart.id)
            + " AND product_id = "
            + str(id)
            + ""
        )
        db.session.execute(query)
        db.session.commit()

    flash("Cart updated successfully.", "success")
    return redirect(url_for("cart.cart"))
