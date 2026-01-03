import streamlit as st
import requests
import json

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Generator Dongeng Anak", page_icon="🧚")

st.title("🧚 Generator Dongeng Anak")
st.write("Buat cerita anak yang unik dan mendidik dalam hitungan detik!")

# --- SETUP API KEY ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    api_key = st.text_input("Masukkan Google AI API Key:", type="password")

# --- INPUT PENGGUNA ---
col1, col2 = st.columns(2)

with col1:
    nama_anak = st.text_input("Nama Anak", placeholder="Misal: Budi")
    usia = st.selectbox("Usia", ["Balita (1-3 Th)", "Prasekolah (3-5 Th)", "Sekolah (6-9 Th)"])

with col2:
    tema = st.text_input("Tema/Hobi", placeholder="Misal: Dinosaurus, Berenang")
    gender = st.selectbox("Gender", ["Laki-laki", "Perempuan"])

pesan_moral = st.text_area("Pesan Moral / Masalah yang ingin diperbaiki", placeholder="Misal: Malas gosok gigi, takut gelap")

# --- FUNGSI REQUEST LANGSUNG KE GOOGLE (TANPA LIBRARY GENAI) ---
def generate_story_direct(api_key, prompt):
    # Kita pakai model 1.5 Flash lewat URL langsung
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        # Jika error, tampilkan pesan error aslinya
        return f"Error {response.status_code}: {response.text}"

# --- LOGIKA TOMBOL ---
if st.button("✨ Buat Cerita"):
    if not api_key:
        st.error("API Key belum dimasukkan!")
    elif not nama_anak or not tema:
        st.warning("Mohon isi Nama Anak dan Tema terlebih dahulu.")
    else:
        with st.spinner('Sedang mengarang cerita seru...'):
            # Rakit Prompt
            prompt_lengkap = f"""
            Buatkan dongeng anak bahasa Indonesia.
            Anak: {nama_anak} ({gender}, {usia}).
            Tema: {tema}.
            Pesan Moral: {pesan_moral}.
            Cerita harus seru, mendidik, dan bahasa mudah dipahami.
            """
            
            # Panggil Fungsi Manual
            hasil = generate_story_direct(api_key, prompt_lengkap)
            
            # Cek jika hasilnya Error
            if "Error" in hasil:
                st.error("Gagal menghubungi Google:")
                st.code(hasil)
            else:
                st.success("Cerita selesai dibuat!")
                st.markdown("---")
                st.markdown(hasil)
