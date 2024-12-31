import streamlit as st
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from DATA.auth import get_user_credentials, new_user, show_logged_in_user, validate_user
import DATA.database as db_file

# Initialize session state for login
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None

st.title("MKE Coffee")

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