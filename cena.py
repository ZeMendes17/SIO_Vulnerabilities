from db import StoreDatabase

# get the database
data_base = StoreDatabase("storeDataBase.db")

# insert a comment into the database
data_base.add_comment(3, "User123", "21/04/2023", "This hoodie is a must-have! The warmth and comfort are perfect for those late-night study sessions in the lab. The department's logo looks fantastic.")
data_base.add_comment(3, "Amélia", "23/04/2023", "I couldn't resist getting this hoodie. It's a cozy reminder of my university days. The department's logo still holds a special place in my heart, and this hoodie lets me wear that pride. Great quality and very comfortable.")

# commit the changes
data_base.conn.commit()

# close the database
data_base.close()