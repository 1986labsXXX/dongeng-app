import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Generator Dongeng Anak", page_icon="🌙")

# --- FITUR KEAMANAN (PASSWORD) ---
def check_password():
    """Hanya izinkan akses jika password benar."""
    def password_entered():
        if st.session_state["password"] == st.secrets["APP_PASSWORD"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Masukkan Kode Akses:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Masukkan Kode Akses:", type="password", on_change=password_entered, key="password")
        st.error("😕 Kode akses salah.")
        return False
    else:
        return True

# --- FUNGSI PDF ---
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Dongeng Islami Spesial', 0, 1, 'C')
        self.ln(5)

def create_pdf(text, judul, nama):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", "B", 16)
    pdf.multi_cell(0, 10, judul, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    # Sanitasi teks agar aman untuk PDF
    clean_text = text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 7, clean_text)
    return pdf.output(dest='S').encode('latin-1')

# --- PROGRAM UTAMA ---
if check_password():
    st.title("🌙 Generator Dongeng Anak Islami")
    st.success("✅ Akses Diterima. Silakan buat cerita sepuasnya!")

    # Cek API Key
    try:
        MY_API_KEY = st.secrets["GEMINI_API_KEY"]
    except:
        st.error("❌ API Key belum di-setting di Secrets Streamlit.")
        st.stop()

    with st.form("main_form"):
        col1, col2 = st.columns(2)
        with col1:
            nama_anak = st.text_input("Nama Anak")
            usia = st.selectbox("Usia", ["3-5 Th", "6-8 Th", "9-12 Th"])
        with col2:
            tema = st.text_input("Tema/Hobi", placeholder="Misal: Kucing, Robot")
            gender = st.selectbox("Gender", ["Laki-laki", "Perempuan"])
        
        masalah = st.text_area("Pesan Moral / Masalah", placeholder="Contoh: Malas gosok gigi")
        submit = st.form_submit_button("✨ Buat Cerita")

    if submit and nama_anak:
        # --- PERBAIKAN: TRY DAN EXCEPT HARUS SEJAJAR ---
        try:
            genai.configure(api_key=MY_API_KEY)
            
            # Kita pakai model paling standar dulu agar tidak 404
            model = genai.GenerativeModel('gemini-pro')
            
            with st.spinner("Sedang mengarang cerita..."):
                prompt = f"""
                Bertindaklah sebagai penulis cerita anak.
                Buat cerita pendek (400-500 kata) untuk anak bernama {nama_anak} ({gender}, {usia}).
                Tema: {tema}. Masalah: {masalah}.
                Aturan: Bahasa Indonesia ceria, mengandung nilai Islam, JANGAN pakai Emoji.
                Format: Baris pertama adalah JUDUL (tanpa kata 'Judul:'). Sisanya isi cerita.
                """
                
                response = model.generate_content(prompt)
                full_text = response.text
                
                # Memisahkan Judul
                parts = full_text.split('\n', 1)
                if len(parts) > 1:
                    judul = parts[0].replace('*', '').strip()
                    isi = parts[1].strip()
                else:
                    judul = f"Kisah {nama_anak}"
                    isi = full_text
                
                # Tampilkan di Layar
                st.subheader(judul)
                st.write(isi)
                
                # Download PDF
                pdf_data = create_pdf(isi, judul, nama_anak)
                st.download_button("📥 Download PDF", data=pdf_data, file_name=f"{nama_anak}.pdf", mime="application/pdf")

        except Exception as e:
            # INI BAGIAN YANG TADI HILANG/ERROR
            st.error("Terjadi kesalahan saat menghubungi Google AI:")
            st.error(e)
