import streamlit as st
import sqlite3
import pandas as pd
import re
import matplotlib.pyplot as plt
        
# Fungsi untuk mendapatkan semua path file dari database
def get_all_file_paths():
    with sqlite3.connect('sentimen.db') as conn:
        c = conn.cursor()
        c.execute('SELECT id, file_path FROM files')
        return c.fetchall()

def analisis_sentimen():
    st.title("Analisis Sentimen Ulasan Pada Toko Online Shopee By And We")
    st.divider()
    st.write("""
    ## Deskripsi
    Selamat datang di website analisis sentimen. Website ini digunakan untuk melakukan analisis sentimen ulasan menggunakan
    algoritma lexicon. Apa itu algoritma lexicon? Algoritma lexicon adalah metode dalam analisis teks yang menggunakan 
    kamus kata (lexicon) yang telah diberi label tertentu, seperti sentimen positif atau negatif. 
    Algoritma ini mencocokkan kata atau frasa dalam teks dengan entri dalam kamus dan memberikan skor berdasarkan label tersebut. 
    Skor dari semua kata atau frasa dijumlahkan untuk menentukan sentimen atau kategori teks. Keunggulan algoritma ini adalah 
    kesederhanaannya dan kecepatan implementasinya. Kamus yang digunakan merupakan InSet Kamus Lexicon Indonesia yang telah disusun oleh
    peneliti Fajri Koto dan Gemala Y. Rahmaningtyas pada penelitian sebelumnya.
    """)

    # Pilih dataset menggunakan selectbox
    selected_dataset = st.file_uploader("Upload *file wajib .csv dan judul kolom sentimen diubah 'full_text'", type=["csv"])

    # Menampilkan dataset
    st.subheader("Dataset")
    if selected_dataset:
        data = pd.read_csv(selected_dataset, sep=";")
        df = data
        st.dataframe(df)


    # ====================================== PRE PROCESSING ========================================
        st.header("Proses Pre Processing")
        st.write("""
        Tahap Pre-Processing pada sistem ini dibagi menjadi 5 tahap yaitu :
        - Cleaning Data
        ===> Untuk membersihkan tanda baca, karakter, angka, dll
        - Stemming Data
        ===> Merubah kata ke huruf kecil 
        - Normalisasi Data
        ===> Menghapus/Mengganti kata-kata tidak penting
        - Tokenisasi Data
        ===> Memisah kata-kata dalam kalimat menjadi sebuah token
        - Stopword
        ===> Menghapus kata-kata yang tidak penting
        """)
        # CLEANING DATA ===================================================================
        def clean_data(text):
            text = re.sub(r'@[A-Za-z0-9_]+', '', text)
            text = re.sub(r'#\w+', '', text)
            text = re.sub(r'RT[\s]+', '', text)
            text = re.sub(r'https?://\S+', '', text)
            text = re.sub(r'[0-9]+', '', text)

            text = re.sub(r'[^A-Za-z0-9 ]', '', text)
            text = re.sub(r'\s+', ' ', text).strip()

            return text

        df['full_text'] = df['full_text'].apply(clean_data)
        st.subheader("Cleaning Data")
        st.dataframe(df['full_text'])
        
        # STEMMING ===================================================================
        df['full_text'] = df['full_text'].str.lower()
        st.subheader("Stemming Data")
        st.dataframe(df['full_text'])
        
        # NORMALIZING DATA ===================================================================
        norm = {
        "udh":"sudah",
        " dikit ":" sedikit ",
        "sesedikit":"sedikit",
        "sampek":"sampai",
        "safety":"aman",
        "cefaatt":"cepat",
        " gapernah ":" tidak pernah ",
        "pwoll":"banget",
        "love":"suka",
        " bgt ":" banget ",
        "baanget":"banget",
        "lagilagi":"lagi lagi",
        " ga ":" tidak ",
        }
        def normalisasi(str_text):
            for i in norm:
                str_text = str_text.replace(i, norm[i])
            return str_text

        df['full_text'] = df['full_text'].apply(lambda x: normalisasi(x))
        st.subheader("Normalisasi Data")
        st.dataframe(df['full_text'])
        
        # TOKENIZING ===================================================================
        tokenized = df['full_text'].apply(lambda x:x.split())
        st.subheader("Tokenisasi Data")
        st.write(df)
        
        # STOPWORD ===================================================================
        # Import Sastrawi
        from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, StopWordRemover, ArrayDictionary

        # Mengambil daftar stopwords dari Sastrawi
        stop_words = StopWordRemoverFactory().get_stop_words()

        # Membuat dictionary untuk stopwords
        new_array = ArrayDictionary(stop_words)
        stop_words_remover_new = StopWordRemover(new_array)

        # Fungsi untuk menghapus stopwords
        def stopword(str_text):
            str_text = stop_words_remover_new.remove(str_text)
            return str_text

        # Menggabungkan token kembali menjadi string
        tokenized_as_string = tokenized.apply(lambda x: ' '.join(x))

        # Menerapkan fungsi stopword pada setiap elemen
        df['clean_text'] = tokenized_as_string.apply(lambda x: stopword(x))
        # ====================================== END PRE PROCESSING ========================================
        
        st.subheader("Data Bersih Stopword + Hasil Pre-Processing")
        st.dataframe(df["clean_text"])
        
        # ========================== KLASIFIKASI/PELABELAN SENTIMEN ALGORITMA LEXICON ======================
        import csv

        # Membaca kamus sentimen positif
        lexicon_positive = dict()
        with open("positive.csv") as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                lexicon_positive[row[0]] = int(row[1])

        # Membaca kamus sentimen negatif
        lexicon_negative = dict()
        with open("negative_baru.csv") as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                lexicon_negative[row[0]] = int(row[1])
        
        # Fungsi untuk menentukan polaritas sentimen
        def analisis_sentimen(text):
            score = 0
            for word in text.split():
                if word in lexicon_negative:
                    score -= lexicon_negative[word]  # Perhatikan perubahan ini untuk mengurangi score dengan bobot negatif
                if word in lexicon_positive:
                    score += lexicon_positive[word]
            polarity = ''
            if score > 0:
                polarity = 'positive'
            elif score < 0:
                polarity = 'negative'
            else:
                polarity = 'neutral'
            return score, polarity
        
        # Menerapkan analisis sentimen
        df['sentiment_score'], df['sentiment_polarity'] = zip(*df['clean_text'].apply(lambda x: analisis_sentimen(x)))
        # ====================================== END KLASIFIKASI DATA LEXICON ========================================
        
        # HASIL ANALISIS SENTIMEN
        st.subheader(f"Hasil Sentimen")
        st.dataframe(df)
        
        # TOTAL SENTIMEN
        st.subheader("Jumlah Sentimen")
        # Menghitung jumlah setiap kategori sentimen
        sentiment_counts = df['sentiment_polarity'].value_counts()
        st.dataframe(sentiment_counts)
        
        # VISUALISASI DATA
        st.subheader("Visualisasi Data")
        def diagram_batang():
            s = pd.value_counts(df['sentiment_polarity'])
            ax = s.plot.bar()
            n = len(df.index) 

            for p in ax.patches:
                ax.annotate(str(round(p.get_height() / n * 100, 2)) + '%', 
                            (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', xytext=(0, 10), textcoords='offset points')

            plt.xlabel('Sentimen Polaritas')
            plt.ylabel('Jumlah')
            plt.title('Distribusi Sentimen Polaritas')
            st.pyplot(plt.gcf())

        st.write(diagram_batang())
    else:
        st.write("Silahkan upload dataset, mohon sesuai ketentuan!")