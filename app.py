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

# --- FUNGSI REQUEST LANGSUNG (ANTI-RIBET) ---
def generate_story_direct(api_key, prompt):
    # KITA UBAH URL KE 'gemini-pro' (Versi paling standar)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    
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
        # Menangkap pesan error spesifik
        return f"ERROR {response.status_code}: {response.text}"

# --- INPUT PENGGUNA ---
col1, col2 = st.columns(2)

with col1:
    nama_anak = st.text_input("Nama Anak", placeholder="Misal: Budi")
    usia = st.selectbox("Usia", ["Balita (1-3 Th)", "Prasekolah (3-5 Th)", "Sekolah (6-9 Th)"])

with col2:
    tema = st.text_input("Tema/Hobi", placeholder="Misal: Dinosaurus, Berenang")
    gender = st.selectbox("Gender", ["Laki-laki", "Perempuan"])

pesan_moral = st.text_area("Pesan Moral / Masalah", placeholder="Misal: Malas gosok gigi")

# --- TOMBOL ---
if st.button("✨ Buat Cerita"):
    if not api_key:
        st.error("API Key belum dimasukkan!")
    elif not nama_anak or not tema:
        st.warning("Mohon isi Nama Anak dan Tema.")
    else:
        with st.spinner('Sedang menghubungi Google...'):
            # Prompt
            prompt_lengkap = f"""
            Buatkan dongeng anak bahasa Indonesia.
            Anak: {nama_anak} ({gender}, {usia}).
            Tema: {tema}.
            Pesan Moral: {pesan_moral}.
            Cerita harus seru, mendidik, dan bahasa mudah dipahami.
            """
            
            # Eksekusi
            hasil = generate_story_direct(api_key, prompt_lengkap)
            
            # Cek Hasil
            if "ERROR" in hasil:
                st.error("Gagal lagi. Detail Error dari Google:")
                st.code(hasil, language='json')
                st.info("Jika masih 404, berarti API Key ini benar-benar tidak memiliki akses ke model apapun (mungkin perlu buat Project baru di Google AI Studio).")
            else:
                st.success("Berhasil!")
                st.markdown("---")
                st.markdown(hasil)
