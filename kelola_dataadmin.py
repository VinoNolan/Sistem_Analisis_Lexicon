import streamlit as st
import sqlite3

def get_all_admin_data():
    with sqlite3.connect('sentimen.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM admin')
        return c.fetchall()

def save_admin_data(nama, username, password, nomor_hp, ig_link):
    with sqlite3.connect('sentimen.db') as conn:
        c = conn.cursor()
        c.execute('INSERT INTO admin (nama, username, password, nomor_hp, ig_link) VALUES (?, ?, ?, ?, ?)', 
                (nama, username, password, nomor_hp, ig_link))
        conn.commit()

def delete_admin(admin_id):
    with sqlite3.connect('sentimen.db') as conn:
        c = conn.cursor()
        c.execute('DELETE FROM admin WHERE id = ?', (admin_id,))
        conn.commit()

# Fungsi untuk mengedit data admin
def edit_admin(admin_id, nama, username, password, nomor_hp, ig_link):
    with sqlite3.connect('sentimen.db') as conn:
        c = conn.cursor()
        c.execute('''
            UPDATE admin
            SET nama = ?, username = ?, password = ?, nomor_hp = ?, ig_link = ?
            WHERE id = ?
        ''', (nama, username, password, nomor_hp, ig_link, admin_id))
        conn.commit()

def data_admin():
    st.header("Kelola Data Admin")
    st.write('''
    Mohon untuk diperhatikan ketentuan dalam pengisian data untuk menghindari terjadinya error, Terima Kasih.
    ''')
    
    st.subheader("Input Admin Baru")
    # Form untuk menambahkan admin baru
    with st.form("admin_form"):
        nama = st.text_input("Nama")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        nomor_hp = st.text_input("Nomor HP *contoh 6281586xxxx")
        ig_link = st.text_input("Link Instagram *copy link profile IG")
        
        submitted = st.form_submit_button("Tambah Admin")
        if submitted:
            save_admin_data(nama, username, password, nomor_hp, ig_link)
            st.success("Admin berhasil ditambahkan")

    # Menampilkan tabel admin
    st.subheader("Data Admin")
    admin_data = get_all_admin_data()
    for admin in admin_data:
        st.write(f"ID: {admin[0]}")
        st.write(f"Nama: {admin[1]}")
        st.write(f"Username: {admin[2]}")
        st.write(f"Nomor HP: {admin[4]}")
        st.write(f"Link IG: {admin[5]}")
        if st.button(f"Delete Admin {admin[0]}", key=f"delete_{admin[0]}"):
            delete_admin(admin[0])
            st.success(f"Admin dengan ID {admin[0]} berhasil dihapus")

        with st.expander(f"Edit Admin {admin[0]}"):
            with st.form(f"edit_admin_form_{admin[0]}"):
                new_nama = st.text_input("Nama", value=admin[1])
                new_username = st.text_input("Username", value=admin[2])
                new_password = st.text_input("Password", value=admin[3], type="password")
                new_nomor_hp = st.text_input("Nomor HP", value=admin[4])
                new_ig_link = st.text_input("Link Instagram", value=admin[5])
                submitted = st.form_submit_button("Edit Admin")
                if submitted:
                    edit_admin(admin[0], new_nama, new_username, new_password, new_nomor_hp, new_ig_link)
                    st.success(f"Admin dengan ID {admin[0]} berhasil diupdate")