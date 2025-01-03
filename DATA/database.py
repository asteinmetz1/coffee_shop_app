import pg8000
import pandas as pd
import streamlit as st

# Database credentials
DB_HOST = st.secrets["database"]["db_host"]
DB_PORT = st.secrets["database"]["db_port"]
DB_NAME = st.secrets["database"]["db_name"]
DB_USER = st.secrets["database"]["db_user"]
DB_PASSWORD = st.secrets["database"]["db_password"]

# Create a connection to the PostgreSQL database
def get_connection():
    return pg8000.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def return_coffee_shop_table():
    """Fetch the coffee_shops table as a Pandas DataFrame with proper headers."""
    conn = get_connection()
    cursor = conn.cursor()

    # Retrieve column names
    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'coffee_shops'")
    columns = [col[0] for col in cursor.fetchall()]  # Extract column names

    # Fetch all rows from the coffee_shops table
    cursor.execute("SELECT * FROM coffee_shops")
    table = cursor.fetchall()

    # Convert to DataFrame with column names
    table_df = pd.DataFrame(table, columns=columns)

    cursor.close()
    conn.close()  # Close the connection
    return table_df

def add_rating_to_coffee_shop(user, coffee_shop, coffee, food, price, vibe, convenience):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO ratings (user_id, shop_id, coffee_rating, food_rating, price_rating, vibe_rating, convenience_rating)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (user, coffee_shop, coffee, food, price, vibe, convenience))

    conn.commit()
    cursor.close()
    conn.close()

def overwrite_rating_to_coffee_shop(user, coffee_shop, coffee, food, price, vibe, convenience):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE ratings
    SET coffee_rating = %s, food_rating = %s, price_rating = %s, vibe_rating = %s, convenience_rating = %s
    WHERE user_id = %s AND shop_id = %s
    ''', (coffee, food, price, vibe, convenience, user, coffee_shop))
    conn.commit()
    cursor.close()
    conn.close()

def add_image_url_to_coffee_shop(shop_id, image_url):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE coffee_shops
    SET image_url = %s
    WHERE shop_id = %s
    ''', (image_url, shop_id))
    conn.commit()
    cursor.close()
    conn.close()

def check_if_coffee_shop_already_exists(coffee_shop_name, coffee_shop_address):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM coffee_shops WHERE name = %s and location = %s", (coffee_shop_name, coffee_shop_address))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

def return_user_id(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def return_coffee_shop_id(coffee_shop, location):
    query = "SELECT shop_id FROM coffee_shops WHERE name = %s AND location = %s"
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, (coffee_shop, location))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def has_user_already_rated_shop(user_id, coffee_shop_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ratings WHERE user_id = %s AND shop_id = %s", (user_id, coffee_shop_id))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

def add_a_new_coffee_shop(coffee_shop_name, coffee_shop_address):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO coffee_shops (name, location)
    VALUES (%s, %s)
    ''', (coffee_shop_name, coffee_shop_address))
    conn.commit()
    cursor.close()
    conn.close()

def return_coffee_shop_ratings_table_w_user_id(user_id, shop_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Retrieve column names
    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'ratings'")
    columns = [col[0] for col in cursor.fetchall()]  # Extract column names

    # Fetch all rows from the ratings table
    cursor.execute("SELECT * FROM ratings WHERE user_id = %s AND shop_id = %s", (user_id, shop_id))
    table = cursor.fetchone()

    # Convert to DataFrame with column names
    table_df = pd.DataFrame([table], columns=columns)

    cursor.close()
    conn.close()  # Close the connection
    return table_df