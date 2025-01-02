import streamlit as st
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from DATA.auth import get_user_credentials, user_login_check, show_logged_in_user
import DATA.database as db_file
from DATA.calcs import get_user_top_shops, return_coffee_shop_ratings_table, return_coffee_shop_table, return_all_ratings


# --------------PAGE CODE------------------- #
st.logo("Images/Brew'd-logo.png", size='large')
st.set_page_config(page_title="Brew'd", page_icon=':coffee')

user_login_check()

st.title("Submit a Rating")

# Initialize session state for sliders
if 'coffee_rating' not in st.session_state:
    st.session_state['coffee_rating'] = 5
if 'food_rating' not in st.session_state:
    st.session_state['food_rating'] = 5
if 'pricing_rating' not in st.session_state:
    st.session_state['pricing_rating'] = 5
if 'vibe_rating' not in st.session_state:
    st.session_state['vibe_rating'] = 5
if 'convenience_rating' not in st.session_state:
    st.session_state['convenience_rating'] = 5

# Rate an existing coffee shop
coffee_shop = st.selectbox(index=None, placeholder='Select A Coffee Shop', label='Select A Coffee Shop',
                           label_visibility='hidden', options=sorted(
                db_file.return_coffee_shop_table().name + " - " + db_file.return_coffee_shop_table().location))
if coffee_shop:
    coffee_shop, location = coffee_shop.split(' - ', 1)
    coffee_shop_id = db_file.return_coffee_shop_id(coffee_shop, location)
    if db_file.has_user_already_rated_shop(st.session_state['user_id'], coffee_shop_id):
        st.write('You have already rated this coffee shop')
        ratings_df = db_file.return_coffee_shop_ratings_table_w_user_id(st.session_state['user_id'], coffee_shop_id)
        st.session_state['coffee_rating'] = ratings_df.coffee_rating[0]
        st.session_state['food_rating'] = ratings_df.food_rating[0]
        st.session_state['pricing_rating'] = ratings_df.price_rating[0]
        st.session_state['vibe_rating'] = ratings_df.vibe_rating[0]
        st.session_state['convenience_rating'] = ratings_df.convenience_rating[0]
    else:
        st.session_state['coffee_rating'] = 5
        st.session_state['food_rating'] = 5
        st.session_state['pricing_rating'] = 5
        st.session_state['vibe_rating'] = 5
        st.session_state['convenience_rating'] = 5

coffee_rating = st.slider(label='Coffee', min_value=1, max_value=10, value=st.session_state['coffee_rating'])
food_rating = st.slider(label='Food', min_value=1, max_value=10, value=st.session_state['food_rating'])
pricing_rating = st.slider(label='Pricing', min_value=1, max_value=10, value=st.session_state['pricing_rating'])
vibe_rating = st.slider(label='Vibe', min_value=1, max_value=10, value=st.session_state['vibe_rating'])
convenience_rating = st.slider(label='Convenience', min_value=1, max_value=10, value=st.session_state['convenience_rating'])

# submit to push to database
if st.button(label='Submit'):
    coffee_shop_id = db_file.return_coffee_shop_id(coffee_shop, location)
    if db_file.has_user_already_rated_shop(st.session_state['user_id'], coffee_shop_id):
        db_file.overwrite_rating_to_coffee_shop(st.session_state['user_id'], coffee_shop_id, coffee_rating,
                                                food_rating, pricing_rating, vibe_rating, convenience_rating)
        st.write('Rating Updated')
    else:
        db_file.add_rating_to_coffee_shop(st.session_state['user_id'], coffee_shop_id, coffee_rating, food_rating,
                                          pricing_rating, vibe_rating, convenience_rating)
        st.write('Rating Added')

st.divider()
st.header('Add a New Coffee Shop')
new_coffee_shop_name = st.text_input('Coffee Shop Name')
new_coffee_shop_location = st.text_input('Location / Neighborhood')

if db_file.check_if_coffee_shop_already_exists(new_coffee_shop_name, new_coffee_shop_location):
    st.error('Coffee Shop Already Exists')
else:
    if st.button('Add New Coffee Shop'):
        db_file.add_a_new_coffee_shop(new_coffee_shop_name, new_coffee_shop_location)
        st.write('Coffee Shop Added')
        st.rerun()

st.subheader('Coffee Shops in Database')
st.dataframe(return_coffee_shop_table(), hide_index=True)

show_logged_in_user()