import streamlit as st
import re
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, StopWordRemover, ArrayDictionary
import csv

def cek_kalimatsentimen():
    st.title("Cek Kalimat Sentimen")

    # Text input for sentiment analysis
    sentimen = st.text_input("Cek Kalimat Sentimen")

    if st.button("Cek Sentimen"):
        # ====================================== PRE PROCESSING ========================================
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

        cleaned_text = clean_data(sentimen)
        
        # STEMMING ===================================================================
        cleaned_text = cleaned_text.lower()
        
        # NORMALIZING DATA ===================================================================
        norm = {
            "udh":"sudah",
            "dikit":"sedikit",
            "sesedikit":"sedikit",
            "sampek":"sampai",
            "safety":"aman",
            "cefaatt":"cepat",
            "gapernah":"tidak pernah",
            "pwoll":"banget",
            "love":"suka",
            "bgt":"banget",
            "baanget":"banget",
            "lagilagi":"lagi lagi",
            "ga":"tidak",
        }

        def normalisasi(str_text):
            for i in norm:
                str_text = str_text.replace(i, norm[i])
            return str_text

        normalized_text = normalisasi(cleaned_text)
    
        # TOKENIZING ===================================================================
        tokenized = normalized_text.split()
        
        # STOPWORD ===================================================================
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
        tokenized_as_string = ' '.join(tokenized)

        # Menerapkan fungsi stopword pada kalimat
        clean_text = stopword(tokenized_as_string)
        
        # ========================== KLASIFIKASI/PELABELAN SENTIMEN ALGORITMA LEXICON ======================
        
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
                    score -= lexicon_negative[word]  # Mengurangi score dengan bobot negatif
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
        sentiment_score, sentiment_polarity = analisis_sentimen(clean_text)
        
        # HASIL ANALISIS SENTIMEN
        st.subheader("Hasil Analisis Sentimen")
        st.write(f"Kalimat Sentimen = '{sentimen}'")
        st.write(f"Score: {sentiment_score}")
        st.write(f"Sentiment Polarity: {sentiment_polarity}")
