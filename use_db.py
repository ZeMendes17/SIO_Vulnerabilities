from db import StoreDatabase

# create tables
data_base = StoreDatabase("storeDataBase.db")
# data_base.create_tables()

# insert products
with open('static/images/products/mug.jpg', 'rb') as image_file:
    mug_image_data = image_file.read()

data_base.add_product("Mug", 9.99, 10, mug_image_data)

with open('static/images/products/tshirt.jpg', 'rb') as image_file:
    tshirt_image_data = image_file.read()

data_base.add_product("T-Shirt", 19.99, 10, tshirt_image_data)

with open('static/images/products/hoodie.jpg', 'rb') as image_file:
    hoodie_image_data = image_file.read()

data_base.add_product("Hoodie", 29.99, 10, hoodie_image_data)


data_base.close()