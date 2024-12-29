import sqlite3

db_path = '/Users/austinsteinmetz/PycharmProjects/CoffeeShopAppPagesClone/DATA/ratings.db'
# Connect to the database
def clear_table(table_name):
    confirmation = input(f"Are you sure you want to clear all contents of the table '{table_name}'? Type 'delete' to confirm: ")
    if confirmation.lower() == 'delete':
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA journal_mode=WAL;")  # Enable WAL mode
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {table_name}")
        conn.commit()
        conn.close()
        print(f"All contents of the table '{table_name}' have been cleared.")
    else:
        print("Operation cancelled.")

# Example usage
clear_table('ratings')
clear_table('users')
clear_table('coffee_shops')