import sqlite3
db_path = '/Users/austinsteinmetz/PycharmProjects/CoffeeShopAppPagesClone/DATA/ratings.db'
# Connect to the database
conn = sqlite3.connect(db_path)
# Connect to the database
conn.execute("PRAGMA journal_mode=WAL;")  # Enable WAL mode
cursor = conn.cursor()  # Create a cursor object

# Loop to add users
for i in range(1, 6):  # Add 5 users
    username = f'user{i}'
    password = 'password123'
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))

# Commit the transaction after the loop
conn.commit()  # Save all changes at once

# Close the connection
conn.close()  # Ensure the database