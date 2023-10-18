from flask_login import UserMixin
from . import db, ma

cart_product = db.Table(
    "cart_product",
    db.Column("cart_id", db.Integer, db.ForeignKey("cart.id")),
    db.Column("product_id", db.Integer, db.ForeignKey("product.id")),
)

wishlist_product = db.Table(
    "wishlist_product",
    db.Column("wishlist_id", db.Integer, db.ForeignKey("wishlist.id")),
    db.Column("product_id", db.Integer, db.ForeignKey("product.id")),
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(100))
    isAdmin = db.Column(db.Boolean, default=False)
    username = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    image = db.Column(db.String(20), nullable=False, default="default.jpg")
    cart = db.relationship("Cart", backref="user")
    wishlist = db.relationship("Wishlist", backref="user")


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    products = db.relationship(
        "Product", secondary="cart_product", back_populates="carts"
    )

class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    products = db.relationship(
        "Product", secondary="wishlist_product", back_populates="wishlists"
    )


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    image_name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    rating = db.Column(db.Float)
    categorie = db.Column(db.String(100))
    carts = db.relationship("Cart", secondary=cart_product, back_populates="products")
    wishlists = db.relationship("Wishlist", secondary=wishlist_product, back_populates="products")


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    quantity = db.Column(db.Integer)
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    user = db.relationship("User", backref="order")
    email = db.Column(db.String(100))
    shipping_address = db.Column(db.String(100))
    billing_address = db.Column(db.String(100))
    country = db.Column(db.String(100))
    state = db.Column(db.String(100))
    zip = db.Column(db.String(100))
    paymentMethod = db.Column(db.String(100))
    cc_name = db.Column(db.String(100))
    cc_number = db.Column(db.Integer)
    cc_expiration = db.Column(db.Date)
    cc_cvv = db.Column(db.Integer)



class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    user_name = db.Column(db.String(100))
    date = db.Column(db.String(100))
    comment = db.Column(db.String(100))
    rating = db.Column(db.Integer)
