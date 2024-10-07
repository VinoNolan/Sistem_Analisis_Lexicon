import streamlit as st
from streamlit_option_menu import option_menu
from koneksi_database import setup_database
from kelola_dataadmin import data_admin
from kelola_datasentimen import datasentimen
from login import logout

def master():
    # Setup awal
    setup_database()
    
    # Sidebar untuk navigasi antar menu
    with st.sidebar:
        selected = option_menu(
            menu_title="Menu Admin",
            options=["Kelola Data Admin", "Kelola Data Sentimen", "Logout"],
            icons=["person-badge-fill", "database-fill", "door-closed-fill"],
            menu_icon="menu-button-fill",
            default_index=0
        )

    if selected == "Kelola Data Admin":
        data_admin()

    if selected == "Kelola Data Sentimen":
        datasentimen()
        
    if selected == "Logout":
        logout()
