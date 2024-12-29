import pg8000
import streamlit as st
import bcrypt
import pg8000
import pg8000.exceptions

# Database credentials
DB_HOST = '34.58.9.59'
DB_PORT = 5432
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = 'A[*d(Q0Nkup`[xlI'

# Create a connection to the PostgreSQL database
def get_connection():
    return pg8000.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# Check if the user is logged in
def user_login_check():
    if not st.session_state.get("logged_in", False):
        st.error("You must log in to view this page.")
        st.stop()

# Check if the user is logged out (e.g., for logout page)
def user_login_check_logout_page():
    if not st.session_state.get("logged_in", False):
        st.write('Logged Out')
        st.stop()

# Show the logged-in user's username
def show_logged_in_user():
    if st.session_state.get('logged_in', False):
        st.markdown(
            f"""
            <div style="text-align:right; color:gray; font-size:12px;">
                Logged in as: <b>{st.session_state['username']}</b>
            </div>
            """,
            unsafe_allow_html=True
        )

# Fetch the hashed password for a specific user
def get_user_credentials(username):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        return result[0] if result else None  # Returns hashed password in BYTEA format
    except Exception as e:
        st.error(f"Error: {e}")
        return None
    finally:
        conn.close()

# Validate the username and password
def validate_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()

        if result:
            stored_hashed_password = result[0]  # BYTEA format
            # Verify the password
            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        st.error(f"Error: {e}")
        return False
    finally:
        conn.close()

# Add a new user
def new_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        # Insert the user into the database
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, pg8000.Binary(hashed_password)))
        conn.commit()
        st.write("User Added")
    except Exception as e:
        st.error(f"User May Already Exist: {e}")
    finally:
        cursor.close()
        conn.close()