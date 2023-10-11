import sqlite3

class StoreDatabase:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL
            )
        ''')
        self.conn.commit()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL
            )
        ''')
        self.conn.commit()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES customers (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        self.conn.commit()

    def add_product(self, name, price, quantity):
        self.cursor.execute('INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)', (name, price, quantity))
        self.conn.commit()

    def add_customer(self, name, email, phone):
        self.cursor.execute('INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)', (name, email, phone))
        self.conn.commit()

    def add_order(self, customer_id, product_id, quantity):
        self.cursor.execute('INSERT INTO orders (customer_id, product_id, quantity) VALUES (?, ?, ?)', (customer_id, product_id, quantity))
        self.conn.commit()

    def get_products(self):
        self.cursor.execute('SELECT * FROM products')
        return self.cursor.fetchall()

    def get_customers(self):
        self.cursor.execute('SELECT * FROM customers')
        return self.cursor.fetchall()

    def get_orders(self):
        self.cursor.execute('SELECT * FROM orders')
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()