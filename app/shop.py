from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import User
from sqlalchemy import text
from . import db
from flask_login import current_user

shops = Blueprint("shops", __name__)


@shops.route("/shop", methods=["GET", "POST"])
def shop():
    print("shop")
    if request.method == "GET":
        query = text("SELECT * FROM product")
        products = db.session.execute(query).fetchall()

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

        return render_template("shop.html", products=products, number_of_items=number_of_items)
    
    else: #POST
        if 'search' in request.form:
            search_value = request.form['search_value']
            query = text("SELECT * FROM product WHERE name LIKE :search")
            products = db.session.execute(query, {"search": "%" + search_value + "%"}).fetchall()

            return render_template("shop.html", products=products, default_value=search_value.strip())
        
        elif 'option' in request.form:
            op = int(request.form['option'])
            options = ["nothing", "rating", "priceDesc", "priceAsc"]
            selected = options[op]

            return selected
        
    
@shops.route("/shop/<option>", methods=["GET"])        
def sort(option):
    if option == "nothing":
        return redirect(url_for("shops.shop"))

    elif option == "rating":
        query = text("SELECT * FROM product ORDER BY rating DESC")
        products = db.session.execute(query).fetchall()
        
        return render_template("shop.html", products=products, option=option)
    
    elif option == "priceDesc":
        query = text("SELECT * FROM product ORDER BY price DESC")
        products = db.session.execute(query).fetchall()
        
        return render_template("shop.html", products=products, option=option)

    
    elif option == "priceAsc":
        query = text("SELECT * FROM product ORDER BY price ASC")
        products = db.session.execute(query).fetchall()
        
        return render_template("shop.html", products=products, option=option)
    
@shops.route("/shop/add_to_cart/<int:id>", methods=["POST"])
def add_to_cart(id):
    query = text("SELECT * FROM product WHERE id =" + str(id))
    product = db.session.execute(query).fetchone()

    query = text("SELECT * FROM cart WHERE customer_id =" + str(current_user.id))
    cart = db.session.execute(query).fetchone()

    query = text(
        "SELECT * FROM cart_product WHERE cart_id ="
        + str(cart.id)
        + " AND product_id ="
        + str(product.id)
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

    return redirect("/shop")
    