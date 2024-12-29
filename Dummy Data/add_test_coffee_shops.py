import sqlite3

conn = sqlite3.connect('/DATA/ratings.db')  # Open connection to the database

cursor = conn.cursor()  # Create a cursor object

dict_of_shops = {'Test Coffee Shop': '123 Test St', 'Test Coffee Shop 2': '456 Test St'}
for shop in dict_of_shops:
    cursor.execute("INSERT INTO coffee_shops (name, location) VALUES (?, ?)", (shop, dict_of_shops[shop]))
    print(f'Inserted {shop} at {dict_of_shops[shop]} into the database')
    conn.commit()  # Save all changes at once

conn.close()  # Ensure the database is properly closed