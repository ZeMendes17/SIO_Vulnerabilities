from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import User
from sqlalchemy import text
from . import db

shops = Blueprint("shops", __name__)


@shops.route("/shop", methods=["GET", "POST"])
def shop():
    print("shop")
    if request.method == "GET":
        search = request.args.get('search')
        if search:
            query = text("SELECT * FROM product WHERE name LIKE :search")
            products = db.session.execute(query, {"search": "%" + search + "%"}).fetchall()
            return render_template("shop.html", products=products, default_value=search.strip())
        query = text("SELECT * FROM product")
        products = db.session.execute(query).fetchall()

        print(products)

        return render_template("shop.html", products=products)
    
    else: #POST
        print("POST in shop")
        if 'search' in request.form:
            search_value = request.form['search_value']
            return redirect(url_for("shops.shop", search=search_value))
        
        elif 'option' in request.form:
            op = int(request.form['option'])
            options = ["nothing", "rating", "priceDesc", "priceAsc", "clothing", "accessories", "miscellaneous"]
            selected = options[op]

            return selected
        
    
@shops.route("/shop/<option>", methods=["GET", "POST"])        
def sort(option):
    if request.method == "GET":
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
        
        elif option == "clothing":
            query = text("SELECT * FROM product WHERE categorie = 'clothing'")
            products = db.session.execute(query).fetchall()
            
            return render_template("shop.html", products=products, option=option)
        
        elif option == "accessories":
            query = text("SELECT * FROM product WHERE categorie = 'accessories'")
            products = db.session.execute(query).fetchall()
            
            return render_template("shop.html", products=products, option=option)
        
        elif option == "miscellaneous":
            query = text("SELECT * FROM product WHERE categorie = 'miscellaneous'")
            products = db.session.execute(query).fetchall()
            
            return render_template("shop.html", products=products, option=option)
        
        else:
            return redirect(url_for("shops.shop"))
        
    elif request.method == "POST":
        if 'search' in request.form:
            search_value = request.form['search_value']
            
            if option == "rating":
                query = text("SELECT * FROM product WHERE name LIKE :search ORDER BY rating DESC")
                products = db.session.execute(query, {"search": "%" + search_value + "%"}).fetchall()

                return render_template("shop.html", products=products, option=option, default_value=search_value.strip())
            
            elif option == "priceDesc":
                query = text("SELECT * FROM product WHERE name LIKE :search ORDER BY price DESC")
                products = db.session.execute(query, {"search": "%" + search_value + "%"}).fetchall()

                return render_template("shop.html", products=products, option=option, default_value=search_value.strip())
            
            elif option == "priceAsc":
                query = text("SELECT * FROM product WHERE name LIKE :search ORDER BY price ASC")
                products = db.session.execute(query, {"search": "%" + search_value + "%"}).fetchall()

                return render_template("shop.html", products=products, option=option, default_value=search_value.strip())
            
            elif option == "clothing":
                query = text("SELECT * FROM product WHERE name LIKE :search AND categorie = 'clothing'")
                products = db.session.execute(query, {"search": "%" + search_value + "%"}).fetchall()

                return render_template("shop.html", products=products, option=option, default_value=search_value.strip())
            
            elif option == "accessories":
                query = text("SELECT * FROM product WHERE name LIKE :search AND categorie = 'accessories'")
                products = db.session.execute(query, {"search": "%" + search_value + "%"}).fetchall()

                return render_template("shop.html", products=products, option=option, default_value=search_value.strip())
            
            elif option == "miscellaneous":
                query = text("SELECT * FROM product WHERE name LIKE :search AND categorie = 'miscellaneous'")
                products = db.session.execute(query, {"search": "%" + search_value + "%"}).fetchall()

                return render_template("shop.html", products=products, option=option, default_value=search_value.strip())
            
            else:
                query = text("SELECT * FROM product WHERE name LIKE :search")
                products = db.session.execute(query, {"search": "%" + search_value + "%"}).fetchall()

                return render_template("shop.html", products=products, option=option, default_value=search_value.strip())
            
        else:
            return redirect(url_for("shops.shop"))
    