import streamlit as st
import pandas as pd

def kamus():
    kamus_pos = pd.read_csv("positive.csv")
    kamus_neg = pd.read_csv("negative_baru.csv")
    st.header("Kamus Inset Lexicon")
    st.write("""
    Kamus yang digunakan untuk analisis menggunakan algoritma lexicon ini adalah Inset Lexicon Bahasa Indonesia yang disusun oleh
    peneliti Fajri Koto dan Gemal Y. Rahmaningtyas pada penelitian sebelumnya. Inset ini mengandung 3.609 kata positif dan 6.609 kata negatif 
    dalam bentuk Bahasa Indonesia.
    """)
    st.subheader("Kamus Positif")
    st.write(kamus_pos)
    st.subheader("Kamus Negatif")
    st.write(kamus_neg)