from datetime import datetime
from flask import Blueprint, render_template, redirect, request, flash
from .models import Comment
from sqlalchemy import text
from . import db

products = Blueprint("product", __name__)


@products.route("/product/<int:id>", methods=["GET", "POST"])
def product(id):
    if request.method == "GET":
        print("Getting product with id: " + str(id))
        query = text("SELECT * FROM product WHERE id =" + str(id))
        product = db.session.execute(query).fetchone()
        print(product)

        # get the comments for the product
        query = text("SELECT * FROM comment WHERE product_id =" + str(id))
        comments = db.session.execute(query).fetchall()
        print(comments)

        return render_template("product.html", product=product, comments=comments)

    else:  # POST
        # get the comment data
        user = request.form["name_input"]
        comment = request.form["comment_input"]

        # if the option is clear it will just refresh

        if "add_comment" in request.form:
            new_comment = Comment(
                user_name=user,
                date=datetime.today().strftime("%d/%m/%Y"),
                comment=comment,
                product_id=id,
            )
            try:
                db.session.add(new_comment)
                db.session.commit()
            except:
                flash("Error adding comment!", "error")
                return redirect("/product/" + str(id))

        return redirect("/product/" + str(id))
