from flask import Blueprint, jsonify
from app import db
from app.models import User, Product
from sqlalchemy import text

utl = Blueprint("util", __name__)


@utl.route("/generate/database", methods=["GET"])
def generate_database():
    try:
        generate_users()
        generate_products()
        return jsonify({"success": True})
    except Exception as e:
        print(e)
        return jsonify({"success": False})


@utl.route("/generate/users", methods=["GET"])
def generate_users():
    query = text("DELETE FROM user")
    db.session.execute(query)
    db.session.commit()
    users = [
        {
            "username": "admin",
            "password": "admin1234",
            "isaAdmin": True,
            "name": "Admin",
            "email": "admin@gmail.com",
            "phone": "123456789",
        },
        {
            "username": "user",
            "password": "user1234",
            "isaAdmin": False,
            "name": "User",
            "email": "user@gmail.com",
            "phone": "987654321",
        },
    ]
    try:
        db.session.bulk_insert_mappings(User, users)
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        print(e)
        return jsonify({"success": False})


@utl.route("/generate/products", methods=["GET"])
def generate_products():
    query = text("DELETE FROM product")
    db.session.execute(query)
    db.session.commit()
    products = [
        {
            "name": "Mug",
            "price": 9.99,
            "quantity": 30,
            "image_name": "../static/images/products/mug.jpg",
            "description": "DETI mug for coffee or tea",
        },
        {
            "name": "T-Shirt",
            "price": 19.99,
            "quantity": 20,
            "image_name": "../static/images/products/tshirt.jpg",
            "description": "DETI t-shirt for all occasions",
        },
        {
            "name": "Hoodie",
            "price": 29.99,
            "quantity": 10,
            "image_name": "../static/images/products/hoodie.jpg",
            "description": "DETI hoodie for all occasions",
        },
    ]
    try:
        db.session.bulk_insert_mappings(Product, products)
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        print(e)
        return jsonify({"success": False})


@utl.route("/cleaar/database", methods=["GET"])
def clear_database():
    query = text("DELETE FROM user;")
    db.session.execute(query)
    query = text("DELETE FROM product;")
    db.session.execute(query)
    query = text("DELETE FROM order;")
    db.session.execute(query)
    query = text("DELETE FROM comment;")
    db.session.execute(query)

    try:
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        print(e)
        return jsonify({"success": False})
