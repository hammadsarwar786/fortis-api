import sqlite3


conn = sqlite3.connect('ecommerce_db.db')
cursor = conn.cursor()

# products table
create_products_table = '''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    category TEXT NOT NULL
);
'''
# sales table
create_sales_table = '''
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    sale_date DATE NOT NULL,
    quantity INTEGER NOT NULL,
    revenue REAL NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products (id)
);
'''
create_inventory_table = '''
CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    stock_quantity INTEGER NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products (id)
);
'''

create_trigger = '''
CREATE TRIGGER IF NOT EXISTS update_last_updated
AFTER UPDATE ON inventory
FOR EACH ROW
BEGIN
    UPDATE inventory
    SET last_updated = CURRENT_TIMESTAMP
    WHERE id = OLD.id;
END;
'''

cursor.execute(create_products_table)
conn.commit()
cursor.execute(create_sales_table)
conn.commit()
cursor.execute(create_inventory_table)
conn.commit()
cursor.execute(create_trigger)
conn.commit()


conn.close()
