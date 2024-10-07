import streamlit as st
import os
import sqlite3

# Fungsi untuk mendapatkan nama dataset berikutnya
def get_next_dataset_name():
    with sqlite3.connect('sentimen.db') as conn:
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM files')
        count = c.fetchone()[0]
    return f'dataset_{count + 1}.csv'

# Fungsi untuk menyimpan path file ke database
def save_file_path(file_path):
    with sqlite3.connect('sentimen.db') as conn:
        c = conn.cursor()
        c.execute('INSERT INTO files (file_path) VALUES (?)', (file_path,))
        conn.commit()

# Fungsi untuk mendapatkan semua path file dari database
def get_all_file_paths():
    with sqlite3.connect('sentimen.db') as conn:
        c = conn.cursor()
        c.execute('SELECT id, file_path FROM files')
        return c.fetchall()

# Fungsi untuk menghapus file dan path dari database
def delete_file(file_id, file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    with sqlite3.connect('sentimen.db') as conn:
        c = conn.cursor()
        c.execute('DELETE FROM files WHERE id = ?', (file_id,))
        conn.commit()

def datasentimen():
    st.title('Kelola Data Sentimen')

    # Status untuk mengontrol apakah file telah disimpan atau belum
    file_saved = st.session_state.get('file_saved', False)

    # Upload file
    uploaded_file = st.file_uploader("Upload *file wajib .csv dan judul kolom sentimen diubah 'full_text'", type=["csv"])

    if uploaded_file is not None and not file_saved:
        dataset_name = get_next_dataset_name()
        file_path = os.path.join('dataset', dataset_name)

        if not os.path.exists('dataset'):
            os.makedirs('dataset')

        with open(file_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())

        save_file_path(file_path)
        st.session_state['file_saved'] = True
        st.success(f'File saved as {dataset_name}')

    # Tampilkan daftar file yang sudah diupload
    st.subheader('Dataset')
    file_paths = get_all_file_paths()

    if file_paths:
        for file_id, file_path in file_paths:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(file_path)
            with col2:
                if st.button('Delete', key=f'delete_{file_id}'):
                    delete_file(file_id, file_path)
                    st.success(f'File {file_path} deleted')
    else:
        st.write("No files uploaded yet.")