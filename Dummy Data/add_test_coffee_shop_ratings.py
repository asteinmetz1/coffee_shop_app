import pg8000

# Database connection details
DB_HOST = '34.58.9.59'  # Replace with your Cloud SQL public IP
DB_PORT = 5432  # Default PostgreSQL port
DB_NAME = 'postgres'  # Replace with your database name
DB_USER = 'postgres'  # Replace with your PostgreSQL username
DB_PASSWORD = 'A[*d(Q0Nkup`[xlI'  # Replace with your PostgreSQL password
# Connect to the database
conn = pg8000.connect(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
cursor = conn.cursor()

# Test coffee shops to insert
coffee_shops = [
    ("Brewed Awakening", "123 Main Street"),
    ("Daily Grind", "456 Elm Avenue"),
    ("Java Junction", "789 Oak Lane")
]

# Insert data into the coffee_shops table
try:
    for shop in coffee_shops:
        cursor.execute(
            "INSERT INTO coffee_shops (name, location) VALUES (%s, %s)",
            shop
        )
    conn.commit()  # Commit the transaction
    print("Test coffee shops added successfully!")
except Exception as e:
    print(f"Error inserting data: {e}")
finally:
    cursor.close()
    conn.close()