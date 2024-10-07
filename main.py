import streamlit as st
from streamlit_option_menu import option_menu
from guest_analisis import analisis_sentimen
from model_kamus import kamus
from cekkalimat_sentimen import cek_kalimatsentimen

# Inisialisasi session state untuk login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Sidebar untuk navigasi antar menu
with st.sidebar:
    selected = option_menu(
        menu_title="Menu",
        options=["Analisis Sentimen", "Cek Kalimat Sentimen", "Kamus Inset Lexicon"],
        icons=["clipboard-data-fill", "clipboard-data", "blockquote-left"],
        menu_icon="menu-button-fill",
        default_index=0
    )

if selected == "Analisis Sentimen":
    analisis_sentimen()

if selected == "Cek Kalimat Sentimen":
    cek_kalimatsentimen()
    
if selected == "Kamus Inset Lexicon":
    kamus()


