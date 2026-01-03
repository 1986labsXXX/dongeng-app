import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Generator Dongeng Anak", page_icon="🌙")

# --- FITUR KEAMANAN (Cek Password Pembeli) ---
def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        if st.session_state["password"] == st.secrets["APP_PASSWORD"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Hapus password dari session agar aman
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # Tampilkan input password pertama kali
        st.text_input(
            "Masukkan Kode Akses (Dari Admin):", type="password", on_change=password_entered, key="password"
        )
        st.info("Silakan masukkan kode akses yang Anda dapatkan setelah pembayaran.")
        return False
    elif not st.session_state["password_correct"]:
        # Password salah
        st.text_input(
            "Masukkan Kode Akses (Dari Admin):", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Kode akses salah. Cek kembali WhatsApp admin.")
        return False
    else:
        # Password benar
        return True

if check_password():
    # --- JIKA PASSWORD BENAR, APLIKASI DI BAWAH INI AKAN JALAN ---
    
    # --- FUNGSI PDF ---
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 15)
            self.cell(0, 10, 'Dongeng Islami Spesial', 0, 1, 'C')
            self.ln(5)
        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Halaman {self.page_no()}', 0, 0, 'C')

    def create_pdf(text, judul, nama):
        pdf = PDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", "B", 16)
        pdf.multi_cell(0, 10, judul, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", "", 12)
        # Sanitasi teks agar kompatibel dengan FPDF
        clean_text = text.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 7, clean_text)
        return pdf.output(dest='S').encode('latin-1')

    # --- UI UTAMA ---
    st.title("🌙 Generator Dongeng Anak Islami")
    st.success("✅ Akses Diterima. Silakan buat cerita sepuasnya!")

    # Mengambil API Key dari Secrets (Server)
    MY_API_KEY = st.secrets["GEMINI_API_KEY"]

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
        try:
            genai.configure(api_key=MY_API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            with st.spinner("Sedang mengarang cerita..."):
                prompt = f"""
                Buat cerita anak Islami pendek (400-600 kata).
                Anak: {nama_anak} ({gender}, {usia}).
                Tema: {tema}.
                Masalah: {masalah}.
                Aturan: Bahasa Indonesia ceria, hindari emoji, struktur: Judul - Isi - Pesan Moral - Doa.
                Output langsung cerita. Baris pertama adalah JUDUL.
                """
                response = model.generate_content(prompt)
                full_text = response.text
                
                # Parsing Judul
                lines = full_text.split('\n')
                judul = lines[0].replace('JUDUL:', '').replace('*', '').strip()
                isi = "\n".join(lines[1:])
                
                st.subheader(judul)
                st.write(isi)
                
                # Download PDF
                pdf_data = create_pdf(isi, judul, nama_anak)
                st.download_button("📥 Download PDF", data=pdf_data, file_name=f"{nama_anak}.pdf", mime="application/pdf")
                
        except Exception as e:
            st.error(f"Error: {e}")