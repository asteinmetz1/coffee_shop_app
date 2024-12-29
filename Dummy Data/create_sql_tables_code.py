import sqlite3

db_path = '/Users/austinsteinmetz/PycharmProjects/CoffeeShopAppPagesClone/DATA/ratings.db'

# Connect to (or create) the database
conn = sqlite3.connect(db_path)


# Enable WAL mode
with sqlite3.connect('../DATA/ratings.db') as conn:
    conn.execute("PRAGMA journal_mode=WAL;")
    print   ("WAL mode enabled.")

# Create a cursor to execute SQL commands
cursor = conn.cursor()


# Create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS coffee_shops (
        shop_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        location TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS ratings (
        rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        shop_id INTEGER,
        coffee_rating INTEGER,
        price_rating INTEGER,
        food_rating INTEGER,
        vibe_rating INTEGER,
        convenience_rating  INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(user_id),
        FOREIGN KEY(shop_id) REFERENCES coffee_shops(shop_id)
    )
''')

# Commit changes and close the connection
conn.commit()
conn.close()

