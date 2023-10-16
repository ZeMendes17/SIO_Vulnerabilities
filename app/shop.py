from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import User
from sqlalchemy import text
from . import db

shops = Blueprint("shops", __name__)


@shops.route("/shop", methods=["GET", "POST"])
def shop():
    print("shop")
    if request.method == "GET":
        query = text("SELECT * FROM product")
        products = db.session.execute(query).fetchall()

        print(products)

        return render_template("shop.html", products=products)
    
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
    