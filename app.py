import streamlit as st
import requests
import json

st.set_page_config(page_title="Generator Dongeng Anak", page_icon="🧚")
st.title("🧚 Generator Dongeng Anak")

# --- SETUP API KEY ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    api_key = st.text_input("Masukkan Google AI API Key:", type="password")

# --- FUNGSI REQUEST LANGSUNG (JALUR STABIL V1) ---
def generate_story_direct(api_key, prompt):
    # PERBAIKAN UTAMA: Menggunakan 'v1' (bukan v1beta) agar tidak 404
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    # Kirim request
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"ERROR {response.status_code}: {response.text}"

# --- INPUT PENGGUNA ---
nama_anak = st.text_input("Nama Anak", placeholder="Misal: Budi")
tema = st.text_input("Tema/Hobi", placeholder="Misal: Berenang")
usia = st.selectbox("Usia", ["Balita (1-3 Th)", "Prasekolah (3-5 Th)", "Sekolah (6-9 Th)"])
gender = st.selectbox("Gender", ["Laki-laki", "Perempuan"])
pesan_moral = st.text_area("Pesan Moral", placeholder="Misal: Malas makan")

# --- TOMBOL ---
if st.button("✨ Buat Cerita"):
    if not api_key:
        st.error("API Key kosong!")
    elif not nama_anak or not tema:
        st.warning("Isi nama dan tema dulu ya.")
    else:
        with st.spinner('Sedang membuat cerita...'):
            prompt = f"Buatkan dongeng anak Indonesia. Anak: {nama_anak} ({gender}, {usia}). Tema: {tema}. Moral: {pesan_moral}. Bahasa ceria & mudah."
            
            hasil = generate_story_direct(api_key, prompt)
            
            if "ERROR" in hasil:
                st.error("Gagal:")
                st.code(hasil)
                # SARAN TERAKHIR JIKA MASIH ERROR
                st.warning("Jika masih 400/404: API Key kamu mungkin rusak/kadaluwarsa. Silakan buat Key BARU di aistudio.google.com")
            else:
                st.success("Selesai!")
                st.write(hasil)
