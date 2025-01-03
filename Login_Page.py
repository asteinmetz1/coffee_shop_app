import streamlit as st
import sys
import os
st.logo("Images/Brew'd-logo.png", size='large')
st.set_page_config(page_title="Brew'd", page_icon=':coffee')

# Add the parent directory to the Python path
from DATA.auth import get_user_credentials, new_user, show_logged_in_user, validate_user
import DATA.database as db_file
from DATA.calcs import get_user_top_shops, return_coffee_shop_ratings_table, return_coffee_shop_table, return_all_ratings

col1, col2, col3 = st.columns([1, 2, 1])  # Adjust proportions for alignment

with col2:
    st.image("Images/Brew'd-logo full just text.png", use_container_width=True)

# Initialize session state for login
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None
if 'rerun' not in st.session_state:
    st.session_state['rerun'] = False

def login():
    username = st.session_state['username_input']
    password = st.session_state['password_input']
    if validate_user(username, password):
        st.session_state['logged_in'] = True
        st.session_state['username'] = username
        st.session_state['user_id'] = db_file.return_user_id(username)
        st.success(f"Welcome, {username}!")
        st.session_state['rerun'] = True
    else:
        st.error("Invalid username or password")

if st.session_state['logged_in'] == False:
    st.text_input('Username', key='username_input')
    st.text_input('Password', type='password', key='password_input', on_change=login)
    if st.button("Log In"):
        login()
    with st.popover("Add User"):
        if st.button("Are You Sure?") and st.session_state['username_input'] != "":
            new_user(st.session_state['username_input'], st.session_state['password_input'])
        if st.session_state['username_input'] == "":
            st.write("Username Cannot be Blank")
        if st.session_state['password_input'] == "":
            st.write("Password Cannot be Blank")
else:
    st.success(f'You are logged {st.session_state["username"]}')

if st.session_state['rerun']:
    st.session_state['rerun'] = False
    st.rerun()

show_logged_in_user()