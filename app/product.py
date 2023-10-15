from datetime import datetime
from flask import Blueprint, render_template, redirect, request, flash
from flask_login import current_user, login_required
from .models import Comment, Product
from sqlalchemy import text
from . import db

products = Blueprint("product", __name__)


@products.route("/product/<int:id>", methods=["GET"])
def product(id):
    query = text("SELECT * FROM product WHERE id =" + str(id))
    product = db.session.execute(query).fetchone()

    # get the comments for the product
    query = text("SELECT * FROM comment WHERE product_id =" + str(id))
    comments = db.session.execute(query).fetchall()

    return render_template("product.html", product=product, comments=comments)


@products.route("/product/<int:id>/addcomment", methods=["POST"])
@login_required
def addcomment(id):
    # get the comment data
    comment = request.form["comment_input"]
    rating = int(request.form["rating_input"])

    # if the option is clear it will just refresh

    if "add_comment" in request.form:
        new_comment = Comment(
            user_name=current_user.username,
            date=datetime.today().strftime("%d/%m/%Y"),
            comment=comment,
            product_id=id,
            rating=rating,
        )
        try:
            db.session.add(new_comment)
            db.session.commit()

            # update the product rating
            query = text("SELECT AVG(rating) FROM comment WHERE product_id =" + str(id))
            rating = db.session.execute(query).fetchone()[0]
            query = text(
                "UPDATE product SET rating = "
                + str(round(rating, 1))
                + " WHERE id ="
                + str(id)
            )
            db.session.execute(query)
            db.session.commit()
        except:
            flash("Error adding comment!", "error")
            return redirect("/product/" + str(id))

    return redirect("/product/" + str(id))
