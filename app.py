import streamlit as st
from groq import Groq

# --- 1. SETUP HALAMAN & IMPORT FONT ---
st.set_page_config(page_title="Dunia Dongeng", page_icon="🎈", layout="centered")

# --- INJEKSI CSS & ORNAMEN ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@300;400;600&family=Patrick+Hand&display=swap');

    /* --- BACKGROUND & WARNA UTAMA (KEMBALI KE KUNING) --- */
    .stApp {
        background-color: #FFF9C4; /* Kuning Pastel */
        color: #4E342E; /* Coklat Tua */
    }

    /* --- ORNAMEN BACKGROUND (SVG ICONS) --- */
    /* Agar ornamen ada di belakang konten */
    .main .block-container {
        position: relative;
        z-index: 1;
    }
    .ornament {
        position: fixed;
        opacity: 0.15; /* Transparan samar */
        z-index: 0; /* Di belakang layer utama */
        pointer-events: none; /* Agar tidak bisa diklik */
    }
    /* Posisi Ornamen */
    .orn-dino { top: 20px; left: 20px; width: 120px; }
    .orn-astro { top: 30px; right: 30px; width: 100px; transform: rotate(15deg); }
    .orn-flower { bottom: 20px; left: 20px; width: 90px; }
    .orn-ball { bottom: 20px; right: 20px; width: 80px; }

    /* --- TYPOGRAPHY --- */
    h1 {
        font-family: 'Fredoka', sans-serif;
        color: #FF6F00 !important; /* Oranye Terang */
        font-size: 3.5rem !important;
        text-align: center;
        text-shadow: 3px 3px 0px #FFD54F;
        margin-bottom: -10px;
    }
    .subtitle {
        font-family: 'Patrick Hand', cursive;
        font-size: 1.5rem;
        text-align: center;
        margin-bottom: 30px;
        color: #5D4037;
    }
    label {
        font-family: 'Fredoka', sans-serif !important;
        color: #BF360C !important; /* Coklat Kemerahan */
        font-size: 1.1rem !important;
    }

    /* --- INPUT STYLES (Bulat & Jelas) --- */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div {
        border-radius: 15px !important;
        border: 2px solid #FFB74D !important; /* Border Oranye */
        background-color: #FFFFFF !important;
        color: #000000 !important; /* Teks Hitam Pekat */
        font-family: 'Patrick Hand', cursive !important;
        font-size: 1.1rem !important;
        box-shadow: 2px 2px 0px rgba(0,0,0,0.05);
    }
    /* Fokus */
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #FF6F00 !important;
    }
    /* Dropdown Text */
    div[data-baseweb="select"] span { color: #000000 !important; }

    /* --- TOMBOL JELLY --- */
    .stButton>button {
        font-family: 'Fredoka', sans-serif !important;
        font-size: 1.4rem !important;
        background-image: linear-gradient(to bottom, #FF9800, #F57C00) !important;
        color: white !important;
        border-radius: 30px !important;
        border: none !important;
        padding: 12px 25px !important;
        box-shadow: 0px 5px 0px #E65100 !important; /* Efek 3D */
        transition: all 0.1s;
        margin-top: 10px;
    }
    .stButton>button:active {
        transform: translateY(5px); /* Efek membal saat ditekan */
        box-shadow: 0px 0px 0px #E65100 !important;
    }
    
    /* Tombol Download (Hijau) */
    div[data-testid="stDownloadButton"] > button {
        background-image: linear-gradient(to bottom, #66BB6A, #43A047) !important;
        box-shadow: 0px 5px 0px #2E7D32 !important;
    }
    div[data-testid="stDownloadButton"] > button:active { transform: translateY(5px); box-shadow: 0px 0px 0px !important; }

    /* --- KOTAK HASIL --- */
    .kertas-cerita {
        background-color: #FFF; padding: 35px; border-radius: 20px;
        border: 3px dashed #FFB74D; font-family: 'Patrick Hand', cursive;
        font-size: 1.3rem; line-height: 1.7; color: #3E2723;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.05);
    }
    .kotak-pesan {
        background-color: #E1F5FE; border-radius: 15px; padding: 20px;
        margin-top: 20px; border: 2px solid #81D4FA;
        color: #01579B; font-family: 'Fredoka', sans-serif;
    }
</style>

<img class="ornament orn-dino" src="https://cdn-icons-png.flaticon.com/512/3069/3069187.png">
<img class="ornament orn-astro" src="https://cdn-icons-png.flaticon.com/512/2026/2026534.png">
<img class="ornament orn-flower" src="https://cdn-icons-png.flaticon.com/512/2926/2926756.png">
<img class="ornament orn-ball" src="https://cdn-icons-png.flaticon.com/512/3076/3076882.png">

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

# --- 5. INPUT FORM (Wadah Putih Transparan Agar Tulisan Jelas) ---
with st.container():
    # Menambahkan background putih transparan di area form agar tidak bertabrakan dengan ornamen
    st.markdown("<div style='background-color: rgba(255,255,255,0.85); padding: 25px; border-radius: 25px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);'>", unsafe_allow_html=True)
    
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
                
                # Prompt Engineering (Meminta Cerita + Pertanyaan)
                prompt_system = """
                Kamu adalah pendongeng TK yang sangat ceria.
                Tugas:
                1. Tulis Cerita Anak (Min 5 Paragraf) yang seru & lucu.
                2. Buat 3 Pertanyaan Diskusi/Pemantik setelah cerita.
                Gunakan bahasa Indonesia yang santai, akrab, dan mudah dimengerti anak kecil.
                """
                
                prompt_user = f"""
                Anak: {nama_anak} ({gender}, {usia})
                Hobi: {hobi}
                Tema: {tema}
                Moral: {pesan_moral}
                
                Format Wajib:
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
                
                # Splitting (Memisahkan Cerita dan Pertanyaan)
                if "---BATAS---" in full_response:
                    parts = full_response.split("---BATAS---")
                    cerita_text = parts[0].strip()
                    diskusi_text = parts[1].strip()
                else:
                    cerita_text = full_response
                    diskusi_text = "Yuk ajak ngobrol si kecil tentang cerita tadi!"

                # --- HASIL ---
                st.balloons() # Efek Balon
                
                # 1. Tampilan Kertas Cerita
                st.markdown(f"""
                <div class='kertas-cerita'>
                    {cerita_text.replace(chr(10), '<br>')}
                </div>
                """, unsafe_allow_html=True)
                
                # 2. Tampilan Kotak Pesan (Pertanyaan Pemantik)
                st.markdown(f"""
                <div class='kotak-pesan'>
                    <strong>💡 Obrolan Seru Sebelum Tidur:</strong><br>
                    {diskusi_text.replace(chr(10), '<br>')}
                </div>
                """, unsafe_allow_html=True)

                # 3. Download Button (Teks Gabungan)
                text_download = f"DONGENG UNTUK {nama_anak.upper()}\n\n{cerita_text}\n\n----------------\n{diskusi_text}\n\nDibuat oleh Dunia Dongeng"
                
                st.markdown("<br>", unsafe_allow_html=True)
                col_dl, col_reset = st.columns([1, 1])
                with col_dl:
                    st.download_button("📥 SIMPAN TEKS CERITA", text_download, f"Dongeng_{nama_anak}.txt")

        except Exception as e:
            st.error(f"Yah, peri lagi istirahat: {e}")

# --- RESET ---
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔄 BIKIN CERITA BARU", on_click=reset_app):
    pass
