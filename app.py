import streamlit as st
from groq import Groq

# --- 1. KONFIGURASI HALAMAN & CSS ---
st.set_page_config(page_title="Dunia Dongeng Ajaib", page_icon="🦄", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #FFF9C4; color: #4E342E; }
    h1 { color: #FF6F00; text-align: center; font-family: 'Comic Sans MS', sans-serif; text-shadow: 2px 2px #FFD54F; }
    
    /* Tombol Utama (Buat Cerita) */
    .stButton>button {
        background-color: #FF9800; color: white; border-radius: 20px; 
        height: 3em; width: 100%; font-weight: bold; border: 2px solid #F57C00;
    }
    .stButton>button:hover { background-color: #FB8C00; border-color: #E65100; }
    
    /* Input Style */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea {
        background-color: #FFFFFF; border-radius: 10px; color: #333;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. FUNGSI RESET (Untuk Tombol 'Buat Cerita Lain') ---
def reset_app():
    # Mengosongkan semua state input
    st.session_state["nama_anak"] = ""
    st.session_state["usia"] = None
    st.session_state["gender"] = None
    st.session_state["hobi"] = ""
    st.session_state["tema"] = ""
    st.session_state["pesan_moral"] = ""

# --- 3. JUDUL ---
st.title("🦄 Generator Dongeng Ajaib")
st.markdown("<p style='text-align: center;'>Masukan data si kecil, dan biarkan keajaiban terjadi! ✨</p>", unsafe_allow_html=True)

# --- 4. SETUP API KEY ---
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    st.error("⚠️ API Key belum dipasang di Secrets Streamlit!")
    st.stop()

# --- 5. INPUT PENGGUNA (Dengan Session State Keys) ---
# Kita tambahkan parameter 'key' agar bisa di-reset oleh tombol nanti
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        nama_anak = st.text_input("👤 Nama Panggilan Anak", placeholder="Tulis nama...", key="nama_anak")
        usia = st.selectbox("🎂 Usia", ["Balita (1-3 Th)", "TK (4-6 Th)", "SD (7-10 Th)"], index=None, placeholder="Pilih Usia...", key="usia")
        gender = st.selectbox("⚧ Jenis Kelamin", ["Laki-laki", "Perempuan"], index=None, placeholder="Pilih Gender...", key="gender")

    with col2:
        hobi = st.text_input("⚽ Hobi / Kesukaan", placeholder="Contoh: Main Bola", key="hobi")
        tema = st.text_input("🌟 Tema Cerita", placeholder="Contoh: Petualangan ke Bulan", key="tema")

    pesan_moral = st.text_area("💖 Pesan Moral", placeholder="Contoh: Agar rajin sikat gigi", key="pesan_moral")

# --- 6. LOGIKA UTAMA ---
# Tombol Eksekusi
if st.button("✨ Buat Dongeng Seru! ✨"):
    
    # Validasi Input
    if not nama_anak or not tema or not gender or not usia:
        st.warning("⚠️ Bunda/Ayah, tolong lengkapi Nama, Usia, Gender, dan Tema dulu ya!")
    else:
        try:
            client = Groq(api_key=api_key)
            
            with st.spinner('🧚 Peri sedang menulis cerita panjang untukmu...'):
                
                # Prompt Engineering (Sesuai request: Panjang 5-7 Paragraf)
                prompt_system = """
                Kamu adalah penulis dongeng anak profesional.
                Gunakan bahasa Indonesia yang deskriptif, ceria, dan mendidik.
                Struktur: Judul Menarik -> Pengenalan -> Konflik -> Klimaks -> Penyelesaian -> Pesan Moral.
                PENTING: Buatlah cerita PANJANG dan MENDETAIL (Minimal 5-7 Paragraf).
                """
                
                prompt_user = f"""
                Buatkan dongeng untuk anak.
                - Nama: {nama_anak} ({gender}, {usia})
                - Hobi: {hobi} (Gunakan hobi ini sebagai elemen penting dalam cerita)
                - Tema: {tema}
                - Pesan Moral: {pesan_moral}
                """

                # Request API (Model Terbaru)
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": prompt_system},
                        {"role": "user", "content": prompt_user}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.7,
                    max_tokens=2500, 
                )
                
                cerita = chat_completion.choices[0].message.content
                
                # Tampilkan Hasil
                st.balloons()
                st.success("Hore! Cerita selesai!")
                
                st.markdown("---")
                st.markdown(f"<div style='background-color: #FFFFFF; padding: 25px; border-radius: 15px; border: 3px dashed #FF9800; color: #333; line-height: 1.6;'>{cerita}</div>", unsafe_allow_html=True)
                
                st.markdown("---")
                
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

# --- 7. TOMBOL RESET (Ditaruh di luar blok 'if' agar selalu muncul setelah proses selesai) ---
# Tombol ini akan membersihkan semua isian form
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔄 Buat Cerita Lain (Reset Form)", on_click=reset_app):
    # Tidak perlu isi kode di sini, karena 'on_click' sudah menjalankan fungsi reset_app
    pass
