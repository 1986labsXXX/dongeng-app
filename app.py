import streamlit as st
from groq import Groq

# --- 1. SETUP HALAMAN & IMPORT FONT KHUSUS ---
st.set_page_config(page_title="Dunia Dongeng", page_icon="🎈", layout="centered")

# Kita import font lucu dari Google Fonts agar tidak kaku
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@300;400;600&family=Patrick+Hand&display=swap');

    /* --- BACKGROUND GRADASI PERMEN --- */
    .stApp {
        background: linear-gradient(180deg, #E0F7FA 0%, #F8BBD0 100%);
        background-attachment: fixed;
    }

    /* --- JUDUL BESAR MEMBULAT --- */
    h1 {
        font-family: 'Fredoka', sans-serif;
        color: #E91E63 !important; /* Pink Tua */
        font-size: 3.5rem !important;
        text-align: center;
        text-shadow: 4px 4px 0px #FFFFFF; /* Bayangan Putih */
        margin-bottom: -20px;
    }
    
    /* Sub-judul */
    .subtitle {
        font-family: 'Patrick Hand', cursive;
        font-size: 1.5rem;
        color: #880E4F;
        text-align: center;
        margin-bottom: 30px;
    }

    /* --- INPUT FORM YANG LUCU --- */
    label {
        font-family: 'Fredoka', sans-serif !important;
        color: #0097A7 !important; /* Biru Laut */
        font-size: 1.2rem !important;
    }
    
    /* Kotak Input jadi Bulat & Border Tebal */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div {
        border-radius: 20px !important;
        border: 3px solid #4DD0E1 !important; /* Border Biru Cerah */
        background-color: #FFFFFF !important;
        color: #5D4037 !important; /* Teks Coklat (mirip pensil) */
        font-family: 'Patrick Hand', cursive !important; /* Font Tulis Tangan */
        font-size: 1.2rem !important;
        box-shadow: 2px 2px 0px rgba(0,0,0,0.1);
    }
    
    /* Fokus saat diketik */
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #FF4081 !important; /* Berubah jadi Pink saat diklik */
    }

    /* --- TOMBOL UTAMA (JELLY BUTTON) --- */
    .stButton>button {
        font-family: 'Fredoka', sans-serif !important;
        font-size: 1.5rem !important;
        background-image: linear-gradient(to right, #FF9800, #F57C00) !important;
        color: white !important;
        border-radius: 50px !important; /* Sangat Bulat */
        border: none !important;
        padding: 15px 30px !important;
        box-shadow: 0px 6px 0px #E65100 !important; /* Efek 3D Tebal */
        transition: all 0.1s;
        margin-top: 10px;
    }
    
    /* Efek saat tombol ditekan (mendelep) */
    .stButton>button:active {
        transform: translateY(6px);
        box-shadow: 0px 0px 0px #E65100 !important;
    }

    /* Tombol Download (Hijau Mint) */
    div[data-testid="stDownloadButton"] > button {
        background-image: linear-gradient(to right, #66BB6A, #43A047) !important;
        box-shadow: 0px 6px 0px #2E7D32 !important;
    }
    div[data-testid="stDownloadButton"] > button:active {
        transform: translateY(6px);
        box-shadow: 0px 0px 0px #2E7D32 !important;
    }

    /* --- KOTAK CERITA (KERTAS BUKU) --- */
    .kertas-cerita {
        background-color: #FFF;
        padding: 40px;
        border-radius: 20px;
        border: 4px dashed #FF8A65; /* Garis putus-putus oranye */
        font-family: 'Patrick Hand', cursive;
        font-size: 1.3rem;
        line-height: 1.8;
        color: #3E2723;
        position: relative;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    /* Hiasan Pin Kertas */
    .pin {
        width: 20px; height: 20px; border-radius: 50%;
        background-color: #FF4081; position: absolute;
        top: 15px; left: 50%; transform: translateX(-50%);
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }

    /* Kotak Pesan Moral (Awan Biru) */
    .kotak-pesan {
        background-color: #E1F5FE;
        border-radius: 20px;
        padding: 20px;
        margin-top: 20px;
        border: 3px solid #81D4FA;
        color: #0277BD;
        font-family: 'Fredoka', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. LOGIKA RESET ---
def reset_app():
    keys = ["nama_anak", "usia", "gender", "hobi", "tema", "pesan_moral"]
    for key in keys:
        st.session_state[key] = "" if key not in ["usia", "gender"] else None

# --- 3. JUDUL & HEADER ---
st.markdown("<h1>🎈 Dunia Dongeng 🎈</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Bikin cerita ajaib buat si kecil, yuk!</p>", unsafe_allow_html=True)

# --- 4. API KEY ---
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    st.error("⚠️ Ups, Kunci API belum dipasang!")
    st.stop()

# --- 5. INPUT FORM (Wadah Putih Transparan) ---
with st.container():
    st.markdown("<div style='background-color: rgba(255,255,255,0.6); padding: 20px; border-radius: 20px;'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        nama_anak = st.text_input("Nama Panggilan", placeholder="Contoh: Budi", key="nama_anak")
        usia = st.selectbox("Umur Berapa?", ["Balita (1-3 Th)", "TK (4-6 Th)", "SD (7-10 Th)"], index=None, placeholder="Pilih Umur...", key="usia")
        gender = st.selectbox("Laki/Perempuan?", ["Laki-laki", "Perempuan"], index=None, placeholder="Pilih...", key="gender")
    with col2:
        hobi = st.text_input("Hobinya Apa?", placeholder="Contoh: Main Bola, Dinosaurus", key="hobi")
        tema = st.text_input("Mau Cerita Apa?", placeholder="Contoh: Petualangan ke Bulan", key="tema")
    
    pesan_moral = st.text_area("Pesan Kebaikan (Moral)", placeholder="Contoh: Harus rajin sikat gigi", key="pesan_moral")
    
    st.markdown("</div>", unsafe_allow_html=True)

# --- 6. TOMBOL AKSI ---
st.markdown("<br>", unsafe_allow_html=True)
if st.button("✨ SULAP JADI CERITA! ✨"):
    if not nama_anak or not tema or not gender or not usia:
        st.warning("⚠️ Bunda/Ayah, isi dulu data di atas ya!")
    else:
        try:
            client = Groq(api_key=api_key)
            
            with st.spinner('🧚 Peri sedang menulis cerita... Tunggu ya!'):
                
                # Prompt Engineering
                prompt_system = """
                Kamu adalah pendongeng TK yang sangat ceria.
                Tugas:
                1. Tulis Cerita Anak (Min 5 Paragraf) yang seru & lucu.
                2. Buat 3 Pertanyaan Diskusi.
                Gunakan bahasa Indonesia yang santai, akrab, dan mudah dimengerti anak kecil.
                """
                
                prompt_user = f"""
                Anak: {nama_anak} ({gender}, {usia})
                Hobi: {hobi}
                Tema: {tema}
                Moral: {pesan_moral}
                
                Format:
                [JUDUL CERIA]
                (Isi Cerita...)
                
                ---BATAS---
                
                [OBROLAN SERU]
                1. ...
                2. ...
                3. ...
                """

                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": prompt_system},
                        {"role": "user", "content": prompt_user}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.7,
                    max_tokens=3000, 
                )
                
                full_response = chat_completion.choices[0].message.content
                
                # Splitting
                if "---BATAS---" in full_response:
                    parts = full_response.split("---BATAS---")
                    cerita_text = parts[0].strip()
                    diskusi_text = parts[1].strip()
                else:
                    cerita_text = full_response
                    diskusi_text = "Yuk ajak ngobrol si kecil tentang cerita tadi!"

                # --- HASIL ---
                st.balloons() # Balon wajib keluar!
                
                # Tampilan Kertas Cerita
                st.markdown(f"""
                <div class='kertas-cerita'>
                    <div class='pin'></div>
                    {cerita_text.replace(chr(10), '<br>')}
                </div>
                """, unsafe_allow_html=True)
                
                # Tampilan Kotak Pesan
                st.markdown(f"""
                <div class='kotak-pesan'>
                    <strong>💡 Obrolan Seru Sebelum Tidur:</strong><br>
                    {diskusi_text.replace(chr(10), '<br>')}
                </div>
                """, unsafe_allow_html=True)

                # Download Button
                text_download = f"DONGENG UNTUK {nama_anak.upper()}\n\n{cerita_text}\n\n----------------\n{diskusi_text}"
                
                st.markdown("<br>", unsafe_allow_html=True)
                col_dl, col_reset = st.columns([1, 1])
                with col_dl:
                    st.download_button("📥 SIMPAN CERITA", text_download, f"Dongeng_{nama_anak}.txt")

        except Exception as e:
            st.error(f"Yah, peri lagi istirahat: {e}")

# --- RESET ---
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔄 BIKIN CERITA BARU", on_click=reset_app):
    pass
