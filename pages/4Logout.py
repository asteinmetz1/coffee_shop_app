import streamlit as st
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from DATA.auth import get_user_credentials, user_login_check, show_logged_in_user, user_login_check_logout_page
from DATA.database import return_coffee_shop_table
from DATA.database import add_rating_to_coffee_shop
import DATA.database as db_file
# --------------PAGE CODE------------------- #
st.logo("Images/Brew'd-logo.png", size='large')

user_login_check_logout_page()

if st.button('Logout'):
    st.session_state['logged_in'] = False
    st.session_state['username'] = None
    st.sidebar.success("You have been logged out.")
    st.rerun()  # Refresh the app to show the login page