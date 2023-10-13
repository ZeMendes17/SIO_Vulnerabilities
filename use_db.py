from db import StoreDatabase

# create tables
data_base = StoreDatabase("storeDataBase.db")
# data_base.create_tables()
# data_base.close()

# insert products
data_base.add_product("Mug", 9.99, 30, "mug.jpg")
data_base.add_product("T-Shirt", 19.99, 20, "tshirt.jpg")
data_base.add_product("Hoodie", 29.99, 10, "hoodie.jpg")

data_base.close()