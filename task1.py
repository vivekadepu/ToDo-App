# main.py
import streamlit as st
import bcrypt
import sqlite3
from datetime import datetime
from task import task1_page

conn = sqlite3.connect('users.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    date_joined TIMESTAMP
)
''')
conn.commit()

def register_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    c.execute('INSERT INTO users (username, password, date_joined) VALUES (?, ?, ?)', 
              (username, hashed_password, datetime.now()))
    conn.commit()

def check_login(username, password):
    c.execute('SELECT password FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    if user and bcrypt.checkpw(password.encode(), user[0]):
        return True
    return False


def registration_page():
    st.title('User Registration')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    confirm_password = st.text_input('Confirm Password', type='password')
    if st.button('Register'):
        if password == confirm_password:
            try:
                register_user(username, password)
                st.success('User registered successfully!')
            except sqlite3.IntegrityError:
                st.error('Username already exists')
        else:
            st.error('Passwords do not match')
def login_page():
    st.title('User Login')
    login_username = st.text_input('Username', key='login_username')
    login_password = st.text_input('Password', type='password', key='login_password')
    if st.button('Login'):
        if check_login(login_username, login_password):
            st.success('Login successful!')
            st.session_state['logged_in'] = True
            st.session_state['username'] = login_username
            st.experimental_rerun()
       
def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state['logged_in']:
        task1_page()  # Call the ai_page function when logged in
    else:
        action = st.sidebar.selectbox('Choose Action', ['Register', 'Login'])
        if action == 'Register':
            registration_page()
        else:
            login_page()

if __name__ == "__main__":
    main()