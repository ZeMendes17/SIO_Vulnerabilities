from db import StoreDatabase

def put_products_on_db():
    data_base = StoreDatabase("storeDataBase.db")
    data_base.add_product("Mug", 9.99, 30, "../static/images/products/mug.jpg", "DETI mug for coffee or tea") 
    data_base.add_product("T-Shirt", 19.99, 20, "../static/images/products/tshirt.jpg", "DETI t-shirt for all occasions")
    data_base.add_product("Hoodie", 29.99, 10, "../static/images/products/hoodie.jpg", "DETI hoodie for all occasions")
    data_base.close()

def put_users_on_db():
    data_base = StoreDatabase("storeDataBase.db")
    data_base.add_user("admin", "admin")
    data_base.add_user("user", "user")
    data_base.close()

def get_products_from_db():
    data_base = StoreDatabase("storeDataBase.db")
    products = data_base.get_products()
    data_base.close()
    return products

def get_users_from_db():
    data_base = StoreDatabase("storeDataBase.db")
    users = data_base.get_users()
    data_base.close()
    return users

def clear_db():
    data_base = StoreDatabase("storeDataBase.db")
    data_base.cursor.execute('DELETE FROM products')
    data_base.cursor.execute('DELETE FROM users')
    data_base.cursor.execute('DELETE FROM customers')
    data_base.cursor.execute('DELETE FROM orders')
    data_base.conn.commit()
    data_base.close()

if __name__ == "__main__":
    #put_products_on_db()
    #put_users_on_db()
    products = get_products_from_db()

    for product in products:
        print(product)

    users = get_users_from_db()

    for user in users:
        print(user)

    #clear_db()
    