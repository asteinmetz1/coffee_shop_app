import streamlit as st
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from DATA.auth import get_user_credentials, user_login_check, show_logged_in_user
from DATA.calcs import get_user_top_shops, return_coffee_shop_ratings_table, return_coffee_shop_table
from DATA.ui_color import make_it_pretty

# --------------PAGE CODE------------------- #
make_it_pretty()
user_login_check()

st.title("Ratings Summary Page")
st.subheader('List of Rated Coffee Shops')
st.dataframe(return_coffee_shop_table(), hide_index=True)
st.divider()

st.subheader('Coffee Shop Ratings by Category')
st.dataframe(return_coffee_shop_ratings_table(), hide_index=True)
st.write('**Default Weighting**: 40% vibe | 30% coffee | 10% convenience | 10% food | 10% price')

st.divider()

st.subheader('Your Top Rated Coffee Shops')
number_of_shops_to_show = st.selectbox('Number Of Shops to Show', index=2, options=list(range(1, 11)))
with st.expander('Customize Your Weighting'):
    if  st.button("Reset to Default"):
        custom_vibe_weight = 0.4
        custom_coffee_weight = 0.3
        custom_convenience_weight = 0.1
        custom_food_weight = 0.1
        custom_price_weight = 0.1
        st.rerun()

    custom_vibe_weight = st.slider('Vibe', min_value=0, max_value=100, value=40, step=5)/100
    custom_coffee_weight = st.slider('Coffee', min_value=0, max_value=100, value=30, step=5)/100
    custom_convenience_weight = st.slider('Convenience', min_value=0, max_value=100, value=10, step=5)/100
    custom_food_weight = st.slider('Food', min_value=0, max_value=100, value=10, step=5)/100
    custom_price_weight = st.slider('Price', min_value=0, max_value=100, value=10, step=5)/100
    total = sum([custom_vibe_weight, custom_coffee_weight, custom_convenience_weight, custom_food_weight,
                 custom_price_weight])
    st.write(f'Total for Dave: {round(total*100)}')
    if sum([custom_vibe_weight, custom_coffee_weight, custom_convenience_weight, custom_food_weight,
            custom_price_weight]) !=1:
        st.error('Your weights must sum to 100')
st.dataframe(get_user_top_shops(st.session_state['user_id'], limit=number_of_shops_to_show, custom_coffee_weight=custom_coffee_weight, custom_vibe_weight=custom_vibe_weight, custom_food_weight=custom_food_weight, custom_price_weight=custom_price_weight, custom_convenience_weight=custom_convenience_weight), hide_index=True)

if sum([custom_vibe_weight, custom_coffee_weight, custom_convenience_weight, custom_food_weight,
        custom_price_weight]) > 1:
    st.error('Your weights must sum to 100')
st.write(
    f'**Your Weighting**: {round(custom_vibe_weight*100)}% vibe | {round(custom_coffee_weight*100)}% coffee | {round(custom_convenience_weight*100)}% convenience | {round(custom_food_weight*100)}% food | {round(custom_price_weight*100)}% price')
show_logged_in_user()
