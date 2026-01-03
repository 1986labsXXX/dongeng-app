import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Cek Model", page_icon="🔍")
st.title("🔍 Alat Cek Model Google")

# 1. Ambil API Key dari Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    st.success("✅ API Key terdeteksi.")
except Exception as e:
    st.error("❌ API Key belum disetting di Secrets.")
    st.stop()

# 2. Tombol untuk List Model
if st.button("Tampilkan Daftar Model Saya"):
    try:
        st.info("Sedang menghubungi server Google...")
        available_models = []
        
        # Minta daftar model ke Google
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        
        if available_models:
            st.success("🎉 BERHASIL! Berikut model yang tersedia untuk Anda:")
            # Tampilkan daftar model
            for model_name in available_models:
                st.code(model_name)
            st.info("👆 Copy salah satu nama di atas (misal: models/gemini-pro) untuk dipakai di aplikasi utama.")
        else:
            st.warning("⚠️ Koneksi berhasil, tapi Google bilang tidak ada model yang tersedia. Coba buat API Key baru di Project baru.")
            
    except Exception as e:
        st.error("❌ GAGAL TERHUBUNG.")
        st.write("Pesan Error Detail:")
        st.code(e)
