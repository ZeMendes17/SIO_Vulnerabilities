from flask import Blueprint, render_template
from sqlalchemy import text
from . import db

main = Blueprint("main", __name__)


@main.route("/")
def index():
    query = text("SELECT * FROM product")
    products = db.session.execute(query).fetchall()

    return render_template("index.html", products=products)
