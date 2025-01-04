import streamlit as st
import sys
import os
import pandas as pd

st.logo("Images/Brew'd-logo.png")
st.set_page_config(page_title="Brew'd", page_icon=':coffee',layout='wide')

# Add the parent directory to the Python path

from DATA.auth import get_user_credentials, user_login_check, show_logged_in_user
from DATA.calcs import get_user_top_shops, return_coffee_shop_ratings_table, return_coffee_shop_table, \
    return_all_ratings, return_weighted_rating_for_a_coffee_shop, return_weighted_rating_for_all_coffee_shops
from DATA.database import  return_coffee_shop_id

# --------------PAGE CODE------------------- #
st.logo("Images/Brew'd-logo.png", size='large')
user_login_check()
st.title("Ratings Summary Page")

st.subheader('Coffee Shop Rankings')

event = st.dataframe(return_coffee_shop_ratings_table(), column_config={
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
}, selection_mode='single-row', on_select='rerun', hide_index=True)
if event['selection']['rows'] != []:
    df = return_coffee_shop_ratings_table()
    shop = df.iloc[event.selection['rows'][0]]['Shop']
    location = df.iloc[event.selection['rows'][0]]['Location']
    shop_id = return_coffee_shop_id(shop, location)
    all_coffee_shops_weighted_average_df = return_weighted_rating_for_all_coffee_shops()
    coffee_shop_weighted_rating_df = return_weighted_rating_for_a_coffee_shop(int(shop_id))

    try:
        weighted_rating = coffee_shop_weighted_rating_df['Score'][0]
        coffee_rating = coffee_shop_weighted_rating_df['Coffee'][0]
        vibe_rating = coffee_shop_weighted_rating_df['Vibe'][0]
        price_rating = coffee_shop_weighted_rating_df['Price'][0]
        food_rating = coffee_shop_weighted_rating_df['Food'][0]
        convenience_rating = coffee_shop_weighted_rating_df['Convenience'][0]
    except KeyError as e:
        st.error(f"KeyError: {e}. No data available for the selected coffee shop.")
        st.stop()

    # region All Coffee Shop Metrics
    all_shops_weighted_rating = all_coffee_shops_weighted_average_df['Score'][0]
    all_shops_coffee_rating = all_coffee_shops_weighted_average_df['Coffee'][0]
    all_shops_vibe_rating = all_coffee_shops_weighted_average_df['Vibe'][0]
    all_shops_price_rating = all_coffee_shops_weighted_average_df['Price'][0]
    all_shops_food_rating = all_coffee_shops_weighted_average_df['Food'][0]
    all_shops_convenience_rating = all_coffee_shops_weighted_average_df['Convenience'][0]
    # endregion

    # region Difference from averages
    weighted_rating_difference_from_average = (weighted_rating - all_shops_weighted_rating) / all_shops_weighted_rating
    coffee_rating_difference_from_average = (coffee_rating - all_shops_coffee_rating) / all_shops_coffee_rating
    vibe_rating_difference_from_average = (vibe_rating - all_shops_vibe_rating) / all_shops_vibe_rating
    price_rating_difference_from_average = (price_rating - all_shops_price_rating) / all_shops_price_rating
    food_rating_difference_from_average = (food_rating - all_shops_food_rating) / all_shops_food_rating
    convenience_rating_difference_from_average = (convenience_rating - all_shops_convenience_rating) / all_shops_convenience_rating
    # endregion

    st.subheader(f'**{shop} - {location}** (*vs Average*)')

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.metric("Score", round(weighted_rating, 1), f"{weighted_rating_difference_from_average:.0%}")
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

st.write('**Default Weighting**: 40% vibe | 30% coffee | 10% convenience | 10% food | 10% price')

st.divider()

st.subheader('Your Top Rated Coffee Shops')
number_of_shops_to_show = st.selectbox('Number of Shops to Show', index=2, options=list(range(1, 11)))
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
