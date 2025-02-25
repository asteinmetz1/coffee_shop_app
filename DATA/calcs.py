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
def format_column_names(df):
    df.columns = [
        col.replace("_", " ").title() for col in df.columns
    ]  # Replace underscores with spaces and capitalize each word
    return df

# Get top coffee shops for a user
def get_user_top_shops(user_id, limit, custom_coffee_weight=.3, custom_vibe_weight=.4, custom_food_weight=.1, custom_price_weight=.1, custom_convenience_weight=.1):
    query = f"""
    SELECT
    coffee_shops.name AS Name,
    coffee_shops.location AS Location,
    (
        {custom_coffee_weight} * avg(ratings.coffee_rating) +
        {custom_vibe_weight} * avg(ratings.vibe_rating) +
        {custom_food_weight} * avg(ratings.food_rating) +
        {custom_price_weight} * avg(ratings.price_rating) +
        {custom_convenience_weight} * avg(ratings.convenience_rating)
    ) AS Score
    FROM
        ratings
    JOIN
        coffee_shops ON ratings.shop_id = coffee_shops.shop_id
    WHERE
        ratings.user_id = {user_id}
    GROUP BY
        coffee_shops.name, coffee_shops.location
    ORDER BY
        Score DESC
    LIMIT {limit};
    """
    conn = get_connection()
    first_result = pd.read_sql_query(query, conn)
    result = format_column_names(first_result)
    conn.close()
    return result

def return_coffee_shop_table():
    """Fetch the coffee_shops table as a Pandas DataFrame with proper headers."""
    conn = get_connection()
    cursor = conn.cursor()

    # Retrieve column names
    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'coffee_shops'")
    columns = [col[0] for col in cursor.fetchall()]

    # Fetch all rows from the coffee_shops table
    cursor.execute("SELECT name, location FROM coffee_shops")
    table = cursor.fetchall()

    # Convert to DataFrame with column names
    table_df = pd.DataFrame(table, columns=['Name', 'Location'])

    cursor.close()
    conn.close()
    return table_df


def return_coffee_shop_ratings_table():
    """Fetch the coffee_shops table as a Pandas DataFrame with proper headers."""
    query = '''
    SELECT
    coffee_shops.image_url AS Image,
    coffee_shops.name AS Shop,
    coffee_shops.location AS Location,
    (
        0.3 * avg(ratings.coffee_rating) +
        0.4 * avg(ratings.vibe_rating) +
        0.1 * avg(ratings.food_rating) +
        0.1 * avg(ratings.price_rating) +
        0.1 * avg(ratings.convenience_rating)
    ) as Score,
    AVG(ratings.coffee_rating) AS Coffee,
    AVG(ratings.vibe_rating) AS Vibe,
    AVG(ratings.price_rating) AS Price,
    AVG(ratings.food_rating) AS Food,
    AVG(ratings.convenience_rating) AS Convenience
    FROM
        ratings
    JOIN
        coffee_shops ON ratings.shop_id = coffee_shops.shop_id
    GROUP BY
        coffee_shops.image_url, coffee_shops.name, coffee_shops.location, coffee_shops.shop_id
    order by Score desc;
    '''
    conn = get_connection()
    first_result = pd.read_sql_query(query, conn)
    result = format_column_names(first_result)
    conn.close()
    return result

def return_weighted_rating_for_a_coffee_shop(coffee_shop_id, coffee_weight=0.3, vibe_weight=0.4, food_weight=0.1, price_weight=0.1, convenience_weight=0.1):
    query = f'''
    SELECT
    coffee_shops.name AS shop_name,
    coffee_shops.location AS shop_location,
    ({coffee_weight} * avg(ratings.coffee_rating) +
    {vibe_weight} * avg(ratings.vibe_rating) +
    {food_weight} * avg(ratings.food_rating) +
    {price_weight} * avg(ratings.price_rating) +
    {convenience_weight} * avg(ratings.convenience_rating)) as Score,
    AVG(ratings.coffee_rating) AS Coffee,
    AVG(ratings.vibe_rating) AS Vibe,
    AVG(ratings.price_rating) AS Price,
    AVG(ratings.food_rating) AS Food,
    AVG(ratings.convenience_rating) AS Convenience
    FROM
        ratings
    JOIN
        coffee_shops ON ratings.shop_id = coffee_shops.shop_id
    WHERE coffee_shops.shop_id = {coffee_shop_id}
    GROUP BY
        coffee_shops.shop_id;
    '''
    conn = get_connection()
    first_result = pd.read_sql_query(query, conn)
    result = format_column_names(first_result)
    conn.close()
    return result

def return_weighted_rating_for_all_coffee_shops():
    query = '''
    SELECT
    (
        0.3 * AVG(ratings.coffee_rating) +
        0.4 * AVG(ratings.vibe_rating) +
        0.1 * AVG(ratings.food_rating) +
        0.1 * AVG(ratings.price_rating) +
        0.1 * AVG(ratings.convenience_rating)
    ) as Score,
    avg(ratings.coffee_rating) AS Coffee,
    avg(ratings.vibe_rating) AS Vibe,
    avg(ratings.price_rating) AS Price,
    avg(ratings.food_rating) AS Food,
    avg(ratings.convenience_rating) AS Convenience
    from
        ratings;
    '''
    conn = get_connection()
    result = format_column_names(pd.read_sql_query(query, conn))
    conn.close()
    return result
def return_all_ratings():
    query = '''
    SELECT
    users.username as User,
    coffee_shops.name AS Shop,
    coffee_shops.location AS Location,
        (0.3 * (ratings.coffee_rating) +
        0.4 * (ratings.vibe_rating) +
        0.1 * (ratings.food_rating) +
        0.1 * (ratings.price_rating) +
        0.1 * (ratings.convenience_rating)) as Score,
    ratings.coffee_rating as Coffee,
    ratings.vibe_rating as Vibe,
    ratings.price_rating as Price,
    ratings.food_rating as Food,
    ratings.convenience_rating as Convenience
    FROM
        ratings
    JOIN
        coffee_shops ON ratings.shop_id = coffee_shops.shop_id
    JOIN
        users ON ratings.user_id = users.user_id
    ORDER BY
        users.username,
        coffee_shops.name;
    '''
    conn = get_connection()
    first_result = pd.read_sql_query(query, conn)
    result = format_column_names(first_result)
    conn.close()
    return result