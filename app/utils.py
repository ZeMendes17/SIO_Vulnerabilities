from flask import Blueprint, jsonify
from app import db
from app.models import User, Product, Comment
from sqlalchemy import text

utl = Blueprint("util", __name__)


@utl.route("/generate/database", methods=["GET"])
def generate_database():
    try:
        generate_users()
        generate_products()
        generate_comments()
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
    

@utl.route("/generate/comments", methods=["GET"])
def generate_comments():
    query = text("DELETE FROM comment")
    db.session.execute(query)
    db.session.commit()
    comments = [
        {
            "user_name": "António Mendes",
            "date": "01/10/2021",
            "comment": "I absolutely love my new mug! The design " +
            "is even more vibrant in person, and it's the perfect size for my morning coffee. Plus, it arrived quickly and was well-packaged!",
            "product_id": 1,
        },
        {
            "user_name": "Leonor",
            "date": "14/02/2022",
            "comment": "The mug I received is nice, but there was a small chip on the rim. It might have happened during shipping. It would be great if the packaging could be improved to prevent this in the future. Otherwise, I like the design and the quality of the mug itself.",
            "product_id": 1,
        },
        {
            "user_name": "CoffeeAddict007",
            "date": "03/01/2023",
            "comment": "I had an issue with my order, but the customer service was amazing. They responded promptly to my email and quickly resolved the problem. I now have my perfect mug, and I'm really impressed with their service. Thanks for going above and beyond!",
            "product_id": 1,
        },
        {
            "user_name": "Maria",
            "date": "03/01/2021",
            "comment": "I'm so proud to wear this t-shirt with our department's logo. The quality of the shirt is fantastic, and the logo looks sharp. It's a great way to show my department pride and strike up conversations with fellow students. I'm very happy with this purchase!",
            "product_id": 2,
        },
        {
            "user_name": "User122",
            "date": "04/03/2023",
            "comment": "I graduated from the engineering department a few years ago, and I had to get this t-shirt to reminisce about my university days. The shirt is comfortable, and the department's logo brings back some wonderful memories.",
            "product_id": 2,
        },
        {
            "user_name": "John",
            "date": "05/08/2022",
            "comment": "This hoodie is a must-have! The warmth and comfort are perfect for those late-night study sessions. The department's logo looks fantastic!",
            "product_id": 3,
        },
        {
            "user_name": "Mário",
            "date": "06/11/2022",
            "comment": "I couldn't resist getting this hoodie. It's a cozy reminder of my university days. The department's logo still holds a special place in my heart, and this hoodie lets me wear that pride. Great quality and very comfortable.",
            "product_id": 3,
        },
    ]
    try:
        db.session.bulk_insert_mappings(Comment, comments)
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        print(e)
        return jsonify({"success": False})


@utl.route("/clear/database", methods=["GET"])
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
