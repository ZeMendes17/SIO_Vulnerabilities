import sqlite3
from flask import Flask, render_template, request

from db import StoreDatabase

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/index.html', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/about.html', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/contact-us.html', methods=['GET'])
def contact_us():
    return render_template('contact-us.html')

@app.route('/shop-detail.html', methods=['GET'])
def shop_detail():
    return render_template('shop-detail.html')

@app.route('/shop.html', methods=['GET'])
def shop():
    products = get_products_on_db()

    print(products)

    return render_template('shop.html', products=products)

@app.route('/my-account.html', methods=['GET'])
def my_account():
    return render_template('my-account.html')

@app.route('/cart.html', methods=['GET'])
def cart():
    return render_template('cart.html')

@app.route('/whishlist.html', methods=['GET'])
def wishlist():
    return render_template('wishlist.html')

@app.route('/service.html', methods=['GET'])
def service():
    return render_template('service.html')

@app.route('/login.html', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/signin.html', methods=['GET'])
def signin():
    return render_template('signin.html')

@app.route('/form_login', methods=['POST', 'GET'])
def form_login():
    if request.method == 'POST':
        user = request.form['username']
        key = request.form['password']

        data_base = StoreDatabase("storeDataBase.db")
        user_info = data_base.get_user(user)
        data_base.close()

        if user_info is None:
            return render_template('login.html', info='User not found!')

        if user_info[1] != key:
            return render_template('login.html', info='Wrong password!')

        return render_template('index.html', info='Welcome ' + user_info[0] + '!')

    return render_template('login.html')

@app.route('/form_signin', methods=['POST', 'GET'])
def form_signin():
    if request.method == 'POST':
        user = request.form['username']
        key = request.form['password']
        conf_key = request.form['confirm_password']

        if key != conf_key:
            return render_template('signin.html', info='Passwords do not match!')

        data_base = StoreDatabase("storeDataBase.db")
        success = data_base.add_user(user, key)
        data_base.close()

        if success:
            return render_template('signin.html', info='Sign in successful!')
        else:
            return render_template('signin.html', info='Username already exists!')

    return render_template('signin.html')


def get_products_on_db():
    data_base = StoreDatabase("storeDataBase.db")
    products = data_base.get_products()
    data_base.close()
    return products


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
