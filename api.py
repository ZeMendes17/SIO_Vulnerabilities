from flask import Flask, render_template

app = Flask(__name__)

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
    return render_template('shop.html')

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

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
