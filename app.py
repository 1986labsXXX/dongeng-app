import streamlit as st
from groq import Groq

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Generator Dongeng Anak", page_icon="🦁")
st.title("🦁 Generator Dongeng Anak (via Groq)")
st.write("Super cepat & Gratis menggunakan teknologi Llama 3")

# --- SETUP API KEY ---
# Kita ambil kunci dari "Secrets" di Streamlit Cloud
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    # Jika lupa set secrets, munculkan pesan error yang jelas
    st.error("Settingan API Key belum ada. Masukkan GROQ_API_KEY di Secrets Streamlit ya!")
    st.stop()

# --- INPUT USER ---
col1, col2 = st.columns(2)
with col1:
    nama_anak = st.text_input("Nama Anak", "Budi")
    usia = st.selectbox("Usia", ["Balita (1-3 Th)", "TK (4-6 Th)", "SD (7-10 Th)"])
with col2:
    tema = st.text_input("Tema", "Petualangan di Hutan")
    gender = st.selectbox("Gender", ["Laki-laki", "Perempuan"])

pesan_moral = st.text_area("Pesan Moral", "Pentingnya berbagi mainan")

# --- TOMBOL EKSEKUSI ---
if st.button("🚀 Buat Cerita"):
    try:
        # 1. Inisialisasi
        client = Groq(api_key=api_key)
        
        with st.spinner('Sedang mengetik cerita...'):
            # 2. Request ke Groq (Model Llama 3)
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "Kamu adalah pendongeng anak profesional. Gunakan bahasa Indonesia yang ceria, mendidik, dan mudah dipahami anak-anak."
                    },
                    {
                        "role": "user",
                        "content": f"Buatkan cerita pendek. Anak: {nama_anak} ({gender}, {usia}). Tema: {tema}. Moral: {pesan_moral}."
                    }
                ],
                model="llama-3.3-70b-versatile",
            )
            
            # 3. Tampilkan
            cerita = chat_completion.choices[0].message.content
            st.success("Selesai!")
            st.write(cerita)
            
    except Exception as e:
        st.error(f"Terjadi Error: {e}")

