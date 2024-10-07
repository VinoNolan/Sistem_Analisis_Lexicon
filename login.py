import streamlit as st
import sqlite3


def get_all_admin_data():
    with sqlite3.connect('sentimen.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM admin')
        return c.fetchall()

def validate_login(username, password):
    admins = get_all_admin_data()
    for admin in admins:
        if admin[2] == username and admin[3] == password:
            return True
    return False

# Inisialisasi session state untuk login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title("Login Admin")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if validate_login(username, password):
            st.success("Login berhasil!")
            st.session_state.logged_in = True
        else:
            st.error("Login gagal. Silakan coba lagi.")

def logout():
    st.success("Berhasil Logout")
    st.session_state.logged_in = False
if __name__ == '__main__':
    login()