import streamlit as st
import extra_streamlit_components as stx
from groq import Groq
from gtts import gTTS
import io
import datetime

# --- 1. SETUP HALAMAN ---
st.set_page_config(page_title="Cerita Ajaib Kita", page_icon="🎈", layout="centered")

# --- 2. CSS & STYLE ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@300;400;600&family=Patrick+Hand&display=swap');
    .stApp { background-color: #FFF9C4; color: #4E342E; }
    
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #FFF3E0; border-right: 2px dashed #FFB74D; }

    /* Typography */
    h1 { font-family: 'Fredoka', sans-serif; color: #FF6F00 !important; font-size: 3.5rem !important; text-align: center; text-shadow: 3px 3px 0px #FFD54F; margin-bottom: -10px; }
    .subtitle { font-family: 'Patrick Hand', cursive; font-size: 1.5rem; text-align: center; margin-bottom: 30px; color: #5D4037; }
    label { font-family: 'Fredoka', sans-serif !important; color: #BF360C !important; font-size: 1.1rem !important; }

    /* Input Fields */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div {
        border-radius: 15px !important; border: 2px solid #FFB74D !important;
        background-color: #FFFFFF !important; color: #000000 !important;
        font-family: 'Patrick Hand', cursive !important; font-size: 1.1rem !important;
        box-shadow: none !important;
    }
    div[data-baseweb="select"] span { color: #000000 !important; }

    /* Buttons */
    .stButton>button {
        font-family: 'Fredoka', sans-serif !important; font-size: 1.4rem !important;
        background-image: linear-gradient(to bottom, #FF9800, #F57C00) !important;
        color: white !important; border-radius: 30px !important; border: none !important;
        padding: 12px 25px !important; box-shadow: 0px 5px 0px #E65100 !important;
        margin-top: 10px; width: 100%; transition: all 0.1s;
    }
    .stButton>button:active { transform: translateY(5px); box-shadow: 0px 0px 0px #E65100 !important; }
    
    /* Audio Button Container */
    .tombol-audio-container button {
        background-image: linear-gradient(to bottom, #29B6F6, #039BE5) !important;
        box-shadow: 0px 5px 0px #0277BD !important;
        color: white !important;
    }
    .tombol-audio-container button p { color: white !important; }

    /* Result Box */
    .kertas-cerita {
        background-color: #FFF; padding: 35px; border-radius: 20px;
        border: 3px dashed #FFB74D; font-family: 'Patrick Hand', cursive;
        font-size: 1.3rem; line-height: 1.7; color: #3E2723;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.05); margin-bottom: 20px;
    }
    .kotak-pesan {
        background-color: #E1F5FE; border-radius: 15px; padding: 20px;
        margin-top: 10px; border: 2px solid #81D4FA;
        color: #01579B; font-family: 'Fredoka', sans-serif;
    }
    audio { background-color: #E1F5FE !important; border-radius: 10px !important; width: 100%; border: 2px solid #81D4FA; }
</style>
""", unsafe_allow_html=True)

# --- 3. GATEKEEPER TANPA PASSWORD (CUMA TOMBOL) ---
if "enter_app" not in st.session_state:
    st.session_state.enter_app = False

def show_landing_page():
    # TAMPILAN HALAMAN DEPAN (WARNING)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #FF6F00;'>🔐 Area Member Premium</h1>", unsafe_allow_html=True)
    
    # PERINGATAN KERAS (Text Jelas dengan Box Custom HTML)
    st.markdown("""
    <div style="background-color: #FFEBEE; border: 2px solid #FFCDD2; padding: 25px; border-radius: 15px; color: #3E2723; line-height: 1.6; font-family: sans-serif;">
        <div style="font-weight: bold; font-size: 1.2rem; display: flex; align-items: center; gap: 10px; margin-bottom: 15px; color: #B71C1C;">
            <span>⛔</span> PERINGATAN KEAMANAN
        </div>
        Sistem mendeteksi IP Address perangkat Anda.<br><br>
        Dilarang keras membagikan Link Akses ini kepada orang lain.
        Jika sistem mendeteksi penggunaan tidak wajar (Login dari banyak lokasi berbeda),<br>
        <span style="font-weight: bold; text-decoration: underline; color: #B71C1C;">Akses akan diblokir permanen tanpa pengembalian dana.</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # TOMBOL AKSES
    col_spacer, col_btn, col_spacer2 = st.columns([1, 2, 1])
    with col_btn:
        if st.button("🚀 AKSES GENERATOR SEKARANG"):
            st.session_state.enter_app = True
            st.rerun()
            
    st.markdown("<p style='text-align: center; color: #5D4037; margin-top: 20px; font-size: 0.9rem;'>Butuh bantuan? Email: 1986labs@gmail.com</p>", unsafe_allow_html=True)

# JIKA BELUM KLIK MASUK, TAMPILKAN LANDING PAGE & STOP
if not st.session_state.enter_app:
    show_landing_page()
    st.stop()

# ==========================================
# JIKA SUDAH KLIK TOMBOL, MASUK KE APLIKASI
# ==========================================

# --- 4. MANAJEMEN COOKIE ---
cookie_manager = stx.CookieManager(key="cookie_mgr")
st.write("") 

# Batas Kuota
MAX_QUOTA_TEXT = 10
MAX_QUOTA_AUDIO = 3

# Ambil nilai dari Cookie Browser User
cookie_cerita = cookie_manager.get(cookie="quota_cerita")
cookie_suara = cookie_manager.get(cookie="quota_suara")

# LOGIKA INIT
if cookie_cerita is None:
    expires = datetime.datetime.now() + datetime.timedelta(days=1)
    cookie_manager.set("quota_cerita", MAX_QUOTA_TEXT, expires_at=expires, key="init_cerita")
    sisa_cerita = MAX_QUOTA_TEXT
else:
    sisa_cerita = int(cookie_cerita)

if cookie_suara is None:
    expires = datetime.datetime.now() + datetime.timedelta(days=1)
    cookie_manager.set("quota_suara", MAX_QUOTA_AUDIO, expires_at=expires, key="init_suara")
    sisa_suara = MAX_QUOTA_AUDIO
else:
    sisa_suara = int(cookie_suara)

# --- 5. SIDEBAR INFO ---
with st.sidebar:
    st.title("📊 Kuota Harian")
    st.markdown("---")
    
    st.write(f"📖 **Cerita:** Sisa {sisa_cerita} dari {MAX_QUOTA_TEXT}")
    st.progress(sisa_cerita / MAX_QUOTA_TEXT)
    
    st.write("") 
    
    st.write(f"🔊 **Suara:** Sisa {sisa_suara} dari {MAX_QUOTA_AUDIO}")
    st.progress(sisa_suara / MAX_QUOTA_AUDIO)
    
    st.markdown("---")
    st.caption("ℹ️ Kuota akan reset otomatis 24 jam dari sekarang.")

# --- 6. JUDUL & API ---
st.markdown("<h1>🎈 CERITA AJAIB KITA 🎈</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Bikin cerita ajaib & dengarkan suaranya!</p>", unsafe_allow_html=True)

try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    st.error("⚠️ Ups, Kunci API belum dipasang!")
    st.stop()

# --- 7. STATE UNTUK CERITA ---
if "cerita_ready" not in st.session_state:
    st.session_state.cerita_ready = False
    st.session_state.cerita_text = ""
    st.session_state.diskusi_text = ""
    st.session_state.nama_anak = ""

def reset_form_only():
    keys = ["nama_input", "usia", "gender", "hobi", "tema", "pesan_moral"]
    for key in keys:
        st.session_state[key] = "" if key not in ["usia", "gender"] else None
    st.session_state.cerita_ready = False

# --- 8. INPUT FORM ---
with st.container():
    st.markdown("<div style='background-color: rgba(255,255,255,0.85); padding: 25px; border-radius: 25px;'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        nama_anak = st.text_input("Nama Panggilan", placeholder="Contoh: Budi", key="nama_input")
        usia = st.selectbox("Umur Berapa?", ["Balita (1-3 Th)", "TK (4-6 Th)", "SD (7-10 Th)"], index=None, placeholder="Pilih Umur...", key="usia")
        gender = st.selectbox("Laki/Perempuan?", ["Laki-laki", "Perempuan"], index=None, placeholder="Pilih...", key="gender")
    with col2:
        hobi = st.text_input("Hobinya Apa?", placeholder="Contoh: Main Bola", key="hobi")
        tema = st.text_input("Mau Cerita Apa?", placeholder="Contoh: Petualangan ke Bulan", key="tema")
    pesan_moral = st.text_area("Pesan Kebaikan (Moral)", placeholder="Contoh: Harus rajin sikat gigi", key="pesan_moral")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 9. LOGIKA TOMBOL GENERATE ---
st.markdown("<br>", unsafe_allow_html=True)

if st.button("✨ SULAP JADI CERITA! ✨"):
    # Cek Kuota
    if sisa_cerita <= 0:
        st.error("🛑 Yah, Kuota Cerita habis! Kembali lagi besok ya Bun (Tunggu 24 Jam).")
    elif not nama_anak or not tema or not gender or not usia:
        st.warning("⚠️ Bunda/Ayah, isi dulu data di atas ya!")
    else:
        try:
            client = Groq(api_key=api_key)
            with st.spinner('🧚 Peri sedang menulis cerita... Tunggu ya!'):
                prompt_system = "Kamu adalah pendongeng TK yang ceria. Tulis Cerita Anak (Min 5 Paragraf) Bahasa Indonesia. JUDUL KAPITAL di baris pertama tanpa simbol. Akhiri dengan 3 Pertanyaan Diskusi."
                prompt_user = f"Anak: {nama_anak} ({gender}, {usia}). Hobi: {hobi}. Tema: {tema}. Moral: {pesan_moral}. Format: JUDUL\n(Isi...)\n---BATAS---\n[OBROLAN SERU]\n1..."
                
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "system", "content": prompt_system}, {"role": "user", "content": prompt_user}],
                    model="llama-3.3-70b-versatile", temperature=0.7, max_tokens=3000, 
                )
                full_response = chat_completion.choices[0].message.content.replace('*', '').replace('#', '')

                if "---BATAS---" in full_response:
                    parts = full_response.split("---BATAS---")
                    st.session_state.cerita_text = parts[0].strip()
                    st.session_state.diskusi_text = parts[1].strip()
                else:
                    st.session_state.cerita_text = full_response
                    st.session_state.diskusi_text = "Yuk ngobrol sama si kecil!"
                
                st.session_state.nama_anak = nama_anak
                st.session_state.cerita_ready = True
                
                # --- UPDATE COOKIE (KURANGI KUOTA) ---
                new_quota = sisa_cerita - 1
                expires = datetime.datetime.now() + datetime.timedelta(days=1)
                cookie_manager.set("quota_cerita", new_quota, expires_at=expires, key="reduce_cerita")
                
                st.rerun()

        except Exception as e:
            st.error(f"Error: {e}")

# --- 10. HASIL & AUDIO ---
if st.session_state.cerita_ready:
    st.balloons()
    
    st.markdown(f"<div class='kertas-cerita'>{st.session_state.cerita_text.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)

    # TOMBOL AUDIO
    st.markdown('<div class="tombol-audio-container">', unsafe_allow_html=True)
    if st.button("🔊 BACA DENGAN SUARA (Klik Disini)", help="Klik untuk mendengarkan dongeng"):
        if sisa_suara <= 0:
            st.error("🛑 Yah, Kuota Suara habis! Besok lagi ya.")
        else:
            with st.spinner("Sedang memproses suara..."):
                try:
                    tts = gTTS(text=st.session_state.cerita_text, lang='id', slow=False)
                    sound_file = io.BytesIO()
                    tts.write_to_fp(sound_file)
                    st.audio(sound_file, format='audio/mp3', start_time=0)
                    
                    # --- UPDATE COOKIE AUDIO ---
                    new_quota_audio = sisa_suara - 1
                    expires = datetime.datetime.now() + datetime.timedelta(days=1)
                    cookie_manager.set("quota_suara", new_quota_audio, expires_at=expires, key="reduce_suara")
                    
                except Exception as e:
                    st.error("Gagal memuat suara.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"<div class='kotak-pesan'><strong>💡 Obrolan Seru:</strong><br>{st.session_state.diskusi_text.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 BIKIN CERITA BARU", on_click=reset_form_only):
        pass
