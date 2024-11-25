import sqlite3

connection = sqlite3.connect('db.sqlite3')

cursor = connection.cursor()

# cursor.execute("PRAGMA foreign_keys = OFF")
# cursor.execute("DROP TABLE orders_order")
# cursor.execute("DROP TABLE orders_orderproduct_variations")
# cursor.execute("DROP TABLE orders_payment")
# cursor.execute("DROP TABLE orders_shippingmethod")
# cursor.execute("PRAGMA foreign_keys = ON")

cursor.execute("UPDATE accounts_account SET is_active = 1 WHERE email = 'support@crochetandhooks.com'")