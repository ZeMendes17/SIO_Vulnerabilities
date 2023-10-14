import sqlite3

class StoreDatabase:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        # self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL,
                image_name TEXT,
                description TEXT
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

        # Create product comments table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY,
                product_id INTEGER NOT NULL,
                user_name TEXT NOT NULL,
                date TEXT NOT NULL,
                comment TEXT NOT NULL,
                            
                FOREIGN KEY (product_id) REFERENCES products (id)
            )                    
        ''')

    def drop_tables(self):
        self.cursor.execute('DROP TABLE IF EXISTS products')
        self.conn.commit()

        self.cursor.execute('DROP TABLE IF EXISTS customers')
        self.conn.commit()

        self.cursor.execute('DROP TABLE IF EXISTS orders')
        self.conn.commit()

    def add_product(self, name, price, quantity, image_name, description):
        self.cursor.execute('INSERT INTO products (name, price, quantity, image_name, description) VALUES (?, ?, ?, ?, ?)', (name, price, quantity, image_name, description))
        self.conn.commit()

    def remove_product(self, id):
        self.cursor.execute('DELETE FROM products WHERE id=?', (id,))
        self.conn.commit()

    def add_user(self, username, password):
            # vulnerable to SQL injection
            # query = "INSERT INTO USERS (username, password) VALUES ('%s', '%s')" % (username, password)
            try:
                # SQL injection vulnerability here
                # self.cursor.execute(query)

                self.cursor.execute("INSERT INTO USERS (username, password) VALUES (?, ?)", (username, password))
                self.conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False
            
    def get_user(self, username):
        # SQL injection vulnerability here
        # query = "SELECT username, password FROM USERS WHERE username='%s'" % username
        # self.cursor.execute(query)
        
        self.cursor.execute("SELECT username, password FROM USERS WHERE username=?", (username,))
        return self.cursor.fetchone()

    def add_order(self, customer_id, product_id, quantity):
        self.cursor.execute('INSERT INTO orders (customer_id, product_id, quantity) VALUES (?, ?, ?)', (customer_id, product_id, quantity))
        self.conn.commit()

    def get_products(self):
        self.cursor.execute('SELECT * FROM products')
        return self.cursor.fetchall()
    
    def get_product(self, id):
        self.cursor.execute('SELECT * FROM products WHERE id=?', (id,))
        return self.cursor.fetchone()
    
    def get_users(self):
        self.cursor.execute('SELECT * FROM users')
        return self.cursor.fetchall()

    def get_customers(self):
        self.cursor.execute('SELECT * FROM customers')
        return self.cursor.fetchall()

    def get_orders(self):
        self.cursor.execute('SELECT * FROM orders')
        return self.cursor.fetchall()
    
    # insert a comment into the database
    def add_comment(self, product_id, user_name, date, comment):
        self.cursor.execute('INSERT INTO comments (product_id, user_name, date, comment) VALUES (?, ?, ?, ?)', (product_id, user_name, date, comment))
        self.conn.commit()

    # get all comments for a product
    def get_comments(self, product_id):
        self.cursor.execute('SELECT * FROM comments WHERE product_id=?', (product_id,))
        return self.cursor.fetchall()
    

    def close(self):
        self.conn.close()