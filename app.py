import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Generator Dongeng Anak", page_icon="🧚")

st.title("🧚 Generator Dongeng Anak")
st.write("Buat cerita anak yang unik dan mendidik dalam hitungan detik!")

# --- SETUP API KEY ---
# Coba ambil API Key dari Streamlit Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    # Jika dijalankan di lokal tanpa secrets, minta input manual (opsional)
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

# --- LOGIKA TOMBOL ---
if st.button("✨ Buat Cerita"):
    if not api_key:
        st.error("API Key belum dimasukkan! Cek secrets atau input manual.")
    elif not nama_anak or not tema:
        st.warning("Mohon isi Nama Anak dan Tema terlebih dahulu.")
    else:
        # Tampilkan loading spinner
        with st.spinner('Sedang mengarang cerita seru...'):
            try:
                # 1. Konfigurasi Model (Versi paling aman)
                genai.configure(api_key=api_key)
                
                # Gunakan 1.5 Flash karena kuota gratisnya besar
                model = genai.GenerativeModel('gemini-1.5-flash')

                # 2. RAKIT PROMPT SECARA MANUAL
                # Kita gabung instruksi sistem ke dalam prompt user agar kompatibel dengan semua versi library
                prompt_lengkap = f"""
                Bertindaklah sebagai penulis cerita anak profesional dan pendongeng yang hangat.
                Tuliskan sebuah dongeng pendek untuk anak dengan detail berikut:
                
                - Nama Anak: {nama_anak}
                - Gender: {gender}
                - Usia: {usia}
                - Tema/Minat: {tema}
                - Pesan Moral/Masalah: {pesan_moral}

                Panduan Cerita:
                1. Gunakan bahasa Indonesia yang baku namun mudah dimengerti anak seusia tersebut.
                2. Cerita harus ceria, aman, dan mendidik.
                3. Jangan terlalu panjang (sekitar 300-500 kata).
                4. Berikan Judul yang menarik di awal.
                """

                # 3. Request ke AI
                response = model.generate_content(prompt_lengkap)
                
                # 4. Tampilkan Hasil
                st.success("Cerita selesai dibuat!")
                st.markdown("---")
                st.markdown(response.text)

            except Exception as e:
                st.error("Terjadi kesalahan sistem:")
                st.error(e)
                st.info("Tips: Jika error '429', berarti kuota habis. Jika error lain, coba refresh halaman.")
