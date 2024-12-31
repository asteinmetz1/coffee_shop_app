import streamlit as st
import sys
import os
st.logo("Images/Brew'd-logo.png")

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from DATA.auth import get_user_credentials, new_user, show_logged_in_user, validate_user
import DATA.database as db_file
from DATA.calcs import get_user_top_shops, return_coffee_shop_ratings_table, return_coffee_shop_table, return_all_ratings


# Initialize session state for login
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None

col1, col2, col3 = st.columns([1, 2, 1])  # Adjust proportions for alignment
with col2:
    st.image("Images/Brew'd-logo full just text.png", use_container_width=True)

if st.session_state['logged_in'] == False:
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button("Log In"):
        if validate_user(username, password):
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.session_state['user_id'] = db_file.return_user_id(username)
            st.success(f"Welcome, {username}!")
            st.switch_page("pages/3Ratings Summary.py")
        else:
            st.error("Invalid username or password")
    with st.popover("Add User"):
        if st.button("Are You Sure?") and username != "":
            new_user(username, password)
        if username == "":
            st.write("Username Cannot be Blank")
        if password == "":
            st.write("Password Cannot be Blank")

else:
    st.write('You are already logged in')

show_logged_in_user()