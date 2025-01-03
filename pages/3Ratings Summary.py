import streamlit as st
import sys
import os
import pandas as pd

st.logo("Images/Brew'd-logo.png")
st.set_page_config(page_title="Brew'd", page_icon=':coffee')

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from DATA.auth import get_user_credentials, user_login_check, show_logged_in_user
from DATA.calcs import get_user_top_shops, return_coffee_shop_ratings_table, return_coffee_shop_table, \
    return_all_ratings

# --------------PAGE CODE------------------- #
st.logo("Images/Brew'd-logo.png", size='large')
user_login_check()
st.title("Ratings Summary Page")

st.subheader('Coffee Shop Rankings')

st.dataframe(return_coffee_shop_ratings_table(), column_config={
    "Image": st.column_config.ImageColumn(
        label="",  # Header for the column
        width="small",  # Optional: control the width
        help="",  # Tooltip for the column
    ),    "Score": st.column_config.ProgressColumn(
        min_value=0,  # Minimum value for the progress bar
        max_value=10,  # Maximum value for the progress bar
        width=None,
        format="%.1f"
    )
}, hide_index=True)

st.write('**Default Weighting**: 40% vibe | 30% coffee | 10% convenience | 10% food | 10% price')

st.divider()

st.subheader('Your Top Rated Coffee Shops')
number_of_shops_to_show = st.selectbox('Number Of Shops to Show', index=2, options=list(range(1, 11)))
with st.expander('Customize Your Weighting'):
    if st.button("Reset to Default"):
        custom_vibe_weight = 0.4
        custom_coffee_weight = 0.3
        custom_convenience_weight = 0.1
        custom_food_weight = 0.1
        custom_price_weight = 0.1
        st.rerun()

    custom_vibe_weight = st.slider('Vibe', min_value=0, max_value=100, value=40, step=5) / 100
    custom_coffee_weight = st.slider('Coffee', min_value=0, max_value=100, value=30, step=5) / 100
    custom_convenience_weight = st.slider('Convenience', min_value=0, max_value=100, value=10, step=5) / 100
    custom_food_weight = st.slider('Food', min_value=0, max_value=100, value=10, step=5) / 100
    custom_price_weight = st.slider('Price', min_value=0, max_value=100, value=10, step=5) / 100
    total = sum([custom_vibe_weight, custom_coffee_weight, custom_convenience_weight, custom_food_weight,
                 custom_price_weight])
    st.write(f'Total for Dave: {round(total * 100)}')
    if sum([custom_vibe_weight, custom_coffee_weight, custom_convenience_weight, custom_food_weight,
            custom_price_weight]) != 1:
        st.error('Your weights must sum to 100')
st.dataframe(get_user_top_shops(st.session_state['user_id'], limit=number_of_shops_to_show,
                                custom_coffee_weight=custom_coffee_weight, custom_vibe_weight=custom_vibe_weight,
                                custom_food_weight=custom_food_weight, custom_price_weight=custom_price_weight,
                                custom_convenience_weight=custom_convenience_weight), hide_index=True)

if sum([custom_vibe_weight, custom_coffee_weight, custom_convenience_weight, custom_food_weight,
        custom_price_weight]) > 1:
    st.error('Your weights must sum to 100')
st.write(
    f'**Your Weighting**: {round(custom_vibe_weight * 100)}% vibe | {round(custom_coffee_weight * 100)}% coffee | {round(custom_convenience_weight * 100)}% convenience | {round(custom_food_weight * 100)}% food | {round(custom_price_weight * 100)}% price')

st.divider()
st.subheader('All Ratings')

st.dataframe(return_all_ratings(), hide_index=True)

show_logged_in_user()
