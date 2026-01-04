import streamlit as st
from groq import Groq
from gtts import gTTS
import io

# --- 1. SETUP HALAMAN & IMPORT FONT ---
st.set_page_config(page_title="Cerita Ajaib Kita", page_icon="🎈", layout="centered")

# --- INJEKSI CSS & ORNAMEN ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@300;400;600&family=Patrick+Hand&display=swap');

    /* BACKGROUND & WARNA */
    .stApp { background-color: #FFF9C4; color: #4E342E; }

    /* SIDEBAR STYLE */
    [data-testid="stSidebar"] {
        background-color: #FFF3E0;
        border-right: 2px dashed #FFB74D;
    }

    /* ORNAMEN (SVG ICONS) */
    .main .block-container { position: relative; z-index: 1; }
    .ornament { position: fixed; opacity: 0.15; z-index: 0; pointer-events: none; }
    .orn-dino { top: 20px; left: 20px; width: 120px; }
    .orn-astro { top: 30px; right: 30px; width: 100px; transform: rotate(15deg); }
    .orn-flower { bottom: 20px; left: 20px; width: 90px; }
    .orn-ball { bottom: 20px; right: 20px; width: 80px; }

    /* TYPOGRAPHY */
    h1 { font-family: 'Fredoka', sans-serif; color: #FF6F00 !important; font-size: 3.5rem !important; text-align: center; text-shadow: 3px 3px 0px #FFD54F; margin-bottom: -10px; }
    .subtitle { font-family: 'Patrick Hand', cursive; font-size: 1.5rem; text-align: center; margin-bottom: 30px; color: #5D4037; }
    label { font-family: 'Fredoka', sans-serif !important; color: #BF360C !important; font-size: 1.1rem !important; }

    /* INPUT STYLES (Clean) */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div {
        border-radius: 15px !important; border: 2px solid #FFB74D !important;
        background-color: #FFFFFF !important; color: #000000 !important;
        font-family: 'Patrick Hand', cursive !important; font-size: 1.1rem !important;
        box-shadow: none !important;
    }
    div[data-baseweb="select"] span { color: #000000 !important; }

    /* TOMBOL JELLY */
    .stButton>button {
        font-family: 'Fredoka', sans-serif !important; font-size: 1.4rem !important;
        background-image: linear-gradient(to bottom, #FF9800, #F57C00) !important;
        color: white !important; border-radius: 30px !important; border: none !important;
        padding: 12px 25px !important; box-shadow: 0px 5px 0px #E65100 !important;
        transition: all 0.1s; margin-top: 10px; width: 100%;
    }
    .stButton>button:active { transform: translateY(5px); box-shadow: 0px 0px 0px #E65100 !important; }
    
    /* TOMBOL AUDIO */
    .tombol-audio-container button {
        background-image: linear-gradient(to bottom, #29B6F6, #039BE5) !important;
        box-shadow: 0px 5px 0px #0277BD !important;
        color: white !important;
    }
    .tombol-audio-container button p { color: white !important; }

    /* KOTAK HASIL */
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

<img class="ornament orn-dino" src="https://cdn-icons-png.flaticon.com/512/3069/3069187.png">
<img class="ornament orn-astro" src="https://cdn-icons-png.flaticon.com/512/2026/2026534.png">
<img class="ornament orn-flower" src="https://cdn-icons-png.flaticon.com/512/2926/2926756.png">
<img class="ornament orn-ball" src="https://cdn-icons-png.flaticon.com/512/3076/3076882.png">
""", unsafe_allow_html=True)

# --- 2. SISTEM LOGIN SEDERHANA ---
def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets["APP_PASSWORD"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.markdown("<h1 style='text-align: center; color: #FF6F00;'>🔐 Masuk Dulu Yuk!</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Masukkan Kode Akses yang sudah Bunda beli:</p>", unsafe_allow_html=True)
        st.text_input("Kode Akses", type="password", on_change=password_entered, key="password", placeholder="Ketik kode di sini...")
        st.info("💡 Belum punya kode? Hubungi Admin via WhatsApp untuk membeli.")
        return False
    elif not st.session_state["password_correct"]:
        st.markdown("<h1 style='text-align: center; color: #FF6F00;'>🔐 Masuk Dulu Yuk!</h1>", unsafe_allow_html=True)
        st.text_input("Kode Akses", type="password", on_change=password_entered, key="password", placeholder="Ketik kode di sini...")
        st.error("😕 Yah, kodenya salah. Coba cek lagi ya Bun!")
        return False
    else:
        return True

if not check_password():
    st.stop()

# --- 3. INIT STATE & KUOTA ---
# Setting Kuota Awal
MAX_QUOTA_TEXT = 10
MAX_QUOTA_AUDIO = 3

if "quota_cerita" not in st.session_state:
    st.session_state.quota_cerita = MAX_QUOTA_TEXT
if "quota_suara" not in st.session_state:
    st.session_state.quota_suara = MAX_QUOTA_AUDIO

if "cerita_ready" not in st.session_state:
    st.session_state.cerita_ready = False
    st.session_state.cerita_text = ""
    st.session_state.diskusi_text = ""
    st.session_state.nama_anak = ""

def reset_app():
    keys = ["nama_input", "usia", "gender", "hobi", "tema", "pesan_moral"]
    for key in keys:
        st.session_state[key] = "" if key not in ["usia", "gender"] else None
    st.session_state.cerita_ready = False

# --- 4. SIDEBAR INFO KUOTA ---
with st.sidebar:
    st.title("📊 Kuota Harian")
    st.markdown("---")
    
    # Progress Bar Text
    sisa_txt = st.session_state.quota_cerita
    st.write(f"📖 **Cerita:** Sisa {sisa_txt} dari {MAX_QUOTA_TEXT}")
    st.progress(sisa_txt / MAX_QUOTA_TEXT)
    
    st.write("") # Spasi
    
    # Progress Bar Audio
    sisa_aud = st.session_state.quota_suara
    st.write(f"🔊 **Suara:** Sisa {sisa_aud} dari {MAX_QUOTA_AUDIO}")
    st.progress(sisa_aud / MAX_QUOTA_AUDIO)
    
    st.markdown("---")
    st.caption("ℹ️ Kuota akan reset otomatis besok (atau saat browser direfresh).")

# --- 5. HEADER ---
st.markdown("<h1>🎈 CERITA AJAIB KITA 🎈</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Bikin cerita ajaib & dengarkan suaranya!</p>", unsafe_allow_html=True)

try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    st.error("⚠️ Ups, Kunci API belum dipasang!")
    st.stop()

# --- 6. INPUT FORM ---
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

# --- 7. LOGIKA GENERATE CERITA ---
st.markdown("<br>", unsafe_allow_html=True)

if st.button("✨ SULAP JADI CERITA! ✨"):
    # Cek Kuota Dulu
    if st.session_state.quota_cerita <= 0:
        st.error("🛑 Yah, Kuota Cerita harian Bunda sudah habis! Besok main lagi ya, atau refresh halaman untuk reset (Khusus Beta).")
    elif not nama_anak or not tema or not gender or not usia:
        st.warning("⚠️ Bunda/Ayah, isi dulu data di atas ya!")
    else:
        # Jika Kuota Aman & Data Lengkap
        try:
            client = Groq(api_key=api_key)
            with st.spinner('🧚 Peri sedang menulis cerita... Tunggu ya!'):
                prompt_system = """
                Kamu adalah pendongeng TK yang ceria. 
                Tugas: 
                1. Tulis Cerita Anak (Min 5 Paragraf) dalam Bahasa Indonesia.
                2. PENTING: Tulis JUDUL CERITA dengan HURUF KAPITAL SAJA di baris pertama. JANGAN gunakan tanda bintang (*) atau pagar (#).
                3. Buat 3 Pertanyaan Diskusi di akhir.
                Gunakan bahasa yang santai & seru.
                """
                prompt_user = f"""
                Anak: {nama_anak} ({gender}, {usia}). Hobi: {hobi}. Tema: {tema}. Moral: {pesan_moral}
                Format:
                JUDUL KAPITAL (Tanpa tanda baca)
                (Isi Cerita...)
                ---BATAS---
                [OBROLAN SERU]
                1... 2... 3...
                """
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "system", "content": prompt_system}, {"role": "user", "content": prompt_user}],
                    model="llama-3.3-70b-versatile", temperature=0.7, max_tokens=3000, 
                )
                full_response = chat_completion.choices[0].message.content
                
                # Bersihkan asterisk (*) dan pagar (#)
                full_response = full_response.replace('*', '').replace('#', '')

                if "---BATAS---" in full_response:
                    parts = full_response.split("---BATAS---")
                    st.session_state.cerita_text = parts[0].strip()
                    st.session_state.diskusi_text = parts[1].strip()
                else:
                    st.session_state.cerita_text = full_response
                    st.session_state.diskusi_text = "Yuk ngobrol sama si kecil!"
                
                st.session_state.nama_anak = nama_anak
                st.session_state.cerita_ready = True
                
                # KURANGI KUOTA CERITA
                st.session_state.quota_cerita -= 1
                
                st.rerun()

        except Exception as e:
            st.error(f"Error: {e}")

# --- 8. TAMPILAN HASIL ---
if st.session_state.cerita_ready:
    st.balloons()
    
    st.markdown(f"""
    <div class='kertas-cerita'>
        {st.session_state.cerita_text.replace(chr(10), '<br>')}
    </div>
    """, unsafe_allow_html=True)

    # LOGIKA TOMBOL AUDIO (CEK KUOTA)
    st.markdown('<div class="tombol-audio-container">', unsafe_allow_html=True)
    if st.button("🔊 BACA DENGAN SUARA (Klik Disini)", help="Klik untuk mendengarkan dongeng"):
        if st.session_state.quota_suara <= 0:
            st.error("🛑 Yah, Kuota Suara habis! Besok dengar lagi ya.")
        else:
            with st.spinner("Sedang memproses suara..."):
                try:
                    tts = gTTS(text=st.session_state.cerita_text, lang='id', slow=False)
                    sound_file = io.BytesIO()
                    tts.write_to_fp(sound_file)
                    st.audio(sound_file, format='audio/mp3', start_time=0)
                    
                    # KURANGI KUOTA AUDIO
                    st.session_state.quota_suara -= 1
                    # Kita pakai st.rerun() opsional agar sidebar update, tapi agar audio tidak hilang, 
                    # kita biarkan saja sidebar update di klik berikutnya atau manual update state
                    
                except Exception as e:
                    st.error("Gagal memuat suara.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class='kotak-pesan'>
        <strong>💡 Obrolan Seru Sebelum Tidur:</strong><br>
        {st.session_state.diskusi_text.replace(chr(10), '<br>')}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 BIKIN CERITA BARU", on_click=reset_app):
        pass
