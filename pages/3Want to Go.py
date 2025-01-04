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

st.title("Want to Go")

st.write('Coming Soon')



show_logged_in_user()