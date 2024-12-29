import streamlit as st
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from DATA.auth import get_user_credentials, user_login_check, show_logged_in_user
import DATA.database as db_file
import DATA.calcs as calcs
from DATA.ui_color import make_it_pretty

# --------------PAGE CODE------------------- #
make_it_pretty()
user_login_check()

st.title("Coffee Shop Ratings")
coffee_shop_df = db_file.return_coffee_shop_table()
coffee_shop_list = [f"{row['name']} - {row['location']}" for index, row in coffee_shop_df.iterrows()]
try:
    coffee_shop = st.selectbox('Pick A Shop', coffee_shop_list)
    shop = coffee_shop.split(' - ', 1)[0]
except AttributeError:
    st.error("No Coffee Shops Yet.")
    st.stop()

location = coffee_shop.split(' - ', 1)[1]
shop_id = db_file.return_coffee_shop_id(shop, location)

# Log the shop_id to check if it's correct
st.write(f"Selected Shop ID: {shop_id}")

coffee_shop_weighted_rating_df = calcs.return_weighted_rating_for_a_coffee_shop(shop_id)
all_coffee_shops_weighted_average_df = calcs.return_weighted_rating_for_all_coffee_shops()

# Log the contents of coffee_shop_weighted_rating_df to check if it has data
st.write("Coffee Shop Weighted Rating DataFrame:")
st.write(coffee_shop_weighted_rating_df)

# region Selected Coffee Shop Metrics
try:
    weighted_rating = coffee_shop_weighted_rating_df['Weighted Score'][0]
    coffee_rating = coffee_shop_weighted_rating_df['Coffee Rating Avg'][0]
    vibe_rating = coffee_shop_weighted_rating_df['Vibe Rating Avg'][0]
    price_rating = coffee_shop_weighted_rating_df['Price Rating Avg'][0]
    food_rating = coffee_shop_weighted_rating_df['Food Rating Avg'][0]
    convenience_rating = coffee_shop_weighted_rating_df['Convenience Rate Avg'][0]
except KeyError as e:
    st.error(f"KeyError: {e}. No data available for the selected coffee shop.")
    st.stop()

# region All Coffee Shop Metrics
all_shops_weighted_rating = all_coffee_shops_weighted_average_df['Weighted Score'][0]
all_shops_coffee_rating = all_coffee_shops_weighted_average_df['Coffee Rating Avg'][0]
all_shops_vibe_rating = all_coffee_shops_weighted_average_df['Vibe Rating Avg'][0]
all_shops_price_rating = all_coffee_shops_weighted_average_df['Price Rating Avg'][0]
all_shops_food_rating = all_coffee_shops_weighted_average_df['Food Rating Avg'][0]
all_shops_convenience_rating = all_coffee_shops_weighted_average_df['Convenience Rate Avg'][0]
# endregion

# region Difference from averages
weighted_rating_difference_from_average = (weighted_rating - all_shops_weighted_rating)/all_shops_weighted_rating
coffee_rating_difference_from_average = (coffee_rating - all_shops_coffee_rating) / all_shops_coffee_rating
vibe_rating_difference_from_average = (vibe_rating - all_shops_vibe_rating) / all_shops_vibe_rating
price_rating_difference_from_average = (price_rating - all_shops_price_rating) / all_shops_price_rating
food_rating_difference_from_average = (food_rating - all_shops_food_rating) / all_shops_food_rating
convenience_rating_difference_from_average = (convenience_rating - all_shops_convenience_rating) / all_shops_convenience_rating
# endregion

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric("Weighted Rating", round(weighted_rating, 1), f"{weighted_rating_difference_from_average:.0%}")
with col2:
    st.metric("Coffee", round(coffee_rating, 1), f"{coffee_rating_difference_from_average:.0%}")
with col3:
    st.metric("Vibe", round(vibe_rating, 1), f"{vibe_rating_difference_from_average:.0%}")
with col4:
    st.metric("Price", round(price_rating, 1), f"{price_rating_difference_from_average:.0%}")
with col5:
    st.metric("Food", round(food_rating, 1), f"{food_rating_difference_from_average:.0%}")
with col6:
    st.metric("Convenience", round(convenience_rating, 1), f"{convenience_rating_difference_from_average:.0%}")

show_logged_in_user()