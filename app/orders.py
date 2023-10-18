from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from sqlalchemy import text
from . import db

orders = Blueprint("orders", __name__)

@login_required
@orders.route("/orders")
def orders_page():
    query = text("SELECT * FROM [order] WHERE customer_id =" + str(current_user.id) + " ORDER BY order_number DESC")
    orders = db.session.execute(query).fetchall()
    
    all_order_products = {}
    product_names = {}
    final_prices = {}
    for order in orders:
        query = text("SELECT * FROM order_product WHERE order_id =" + str(order.id))
        order_products = db.session.execute(query).fetchall()
        all_order_products[order.id] = order_products

        final_price = order.tax + order.shipping_cost
        for order_product in order_products:
            final_price += order_product.price_each * order_product.quantity

        final_prices[order.id] = final_price
        #get names
        for order_product in order_products:
            query = text("SELECT name FROM product WHERE id =" + str(order_product.product_id))
            product_name = db.session.execute(query).fetchone()
            product_names[order_product.product_id] = product_name[0]

    # get product names


    return render_template("orders.html", orders=orders, all_order_products=all_order_products, product_names=product_names, final_prices=final_prices)