import streamlit as st
from datetime import datetime
import urllib.parse
import requests
import io

# Menambahkan logo di bagian atas aplikasi
st.set_page_config(page_title="Aplikasi Absensi Atlet JMS JUARA", page_icon="🏃‍♂️")
   st.image("LOGO.png", width=200)  # Ganti dengan path absolut ke file logo Anda

st.title("Aplikasi Absensi Atlet JMS JUARA")

programs_by_category = {
    "Badminton": [
        "Footwork Drill Circuit",
        "Smash Practice 100 reps",
        "Net Play Technique",
        "Doubles Strategy Session",
        "Agility Ladder Training"
    ],
    "Sprinter": [
        "30m Acceleration Drill 10x",
        "Flying 50m Sprints 6x",
        "Explosive Start Practice",
        "Block Start Technique",
        "Resisted Sprint with Parachute"
    ],
    "Middle Distance": [
        "800m Interval 5x",
        "1000m Tempo Run",
        "1200m Repeats 4x",
        "400m Recovery Jog",
        "1500m Time Trial"
    ],
    "Long Distance": [
        "5km Endurance Run",
        "10km Steady Pace",
        "Interval Hill Runs",
        "Tempo Long Runs",
        "Marathon Pace Practice"
    ],
}

if 'selected_category' not in st.session_state:
    st.session_state.selected_category = "Sprinter"

def select_category(category):
    st.session_state.selected_category = category

# Buat dua kolom utama: kiri untuk tombol kategori, kanan untuk formulir
col_left, col_right = st.columns([1, 3])

with col_left:
    st.markdown("### Pilih Kategori Program")
    if st.button("Program Badminton"):
        select_category("Badminton")
    if st.button("Program Sprinter"):
        select_category("Sprinter")
    if st.button("Program Middle Distance"):
        select_category("Middle Distance")
    if st.button("Program Long Distance"):
        select_category("Long Distance")

with col_right:
    st.markdown(f"### Kategori Terpilih: {st.session_state.selected_category}")
    program_list = programs_by_category[st.session_state.selected_category]

    with st.form(key='absensi_form'):
        nama_atlet = st.text_input("Nama Atlet")
        program = st.selectbox("Pilih Program Lari/Olahraga", program_list)
        tanggal_absen = st.date_input("Tanggal Absen", datetime.today())
        status_absen = st.selectbox("Status Absen", ["Hadir", "Tidak Hadir", "Izin"])
        foto = st.camera_input("Ambil Foto Atlet")

        submit_button = st.form_submit_button(label="Kirim")

        # Tampilkan foto yang diambil jika tersedia
        if foto is not None:
            st.image(foto, caption="Foto Atlet", use_container_width=True)  # Menggunakan use_container_width

def upload_to_imgur(image):
    client_id = '677f3d0e9999a04'  # Ganti dengan Client ID Imgur Anda
    headers = {'Authorization': f'Client-ID {client_id}'}
    
    # Mengupload gambar ke Imgur
    response = requests.post("https://api.imgur.com/3/image", headers=headers, files={'image': image})
    
    if response.status_code == 200:
        return response.json()['data']['link']  # Mengembalikan URL gambar
    else:
        st.error("Gagal mengupload gambar ke Imgur.")
        st.error(f"Status Code: {response.status_code}, Response: {response.text}")  # Menampilkan status dan respons
        return None

def create_whatsapp_link(nama, program, tanggal, status, foto_url):
    message = (
        f"Absensi Atlet JMS Juara\n"
        f"Nama Atlet: {nama}\n"
        f"Program: {program}\n"
        f"Tanggal Absen: {tanggal}\n"
        f"Status Absen: {status}\n"
        f"Foto: {foto_url}\n"
    )
    encoded_message = urllib.parse.quote(message)
    return f"https://api.whatsapp.com/send?text={encoded_message}"

if submit_button:
    if not nama_atlet.strip():
        st.error("Nama atlet tidak boleh kosong.")
    elif tanggal_absen > datetime.today().date():
        st.error("Tanggal absen tidak boleh di masa depan.")
    elif foto is None:
        st.error("Foto atlet harus diambil.")
    else:
        # Simpan foto ke buffer
        foto_buffer = io.BytesIO(foto.getbuffer())

        # Upload foto ke Imgur dan dapatkan URL-nya
        foto_url = upload_to_imgur(foto_buffer)

        if foto_url:
            whatsapp_url = create_whatsapp_link(
                nama_atlet.strip(),
                program,
                tanggal_absen.strftime("%Y-%m-%d"),
                status_absen,
                foto_url
            )
            st.success("Data siap dikirim melalui WhatsApp!")
            st.markdown(f'''
                <a href="{whatsapp_url}" target="_blank" 
                style="background-color:#25D366;color:white;padding:12px 24px;
                border-radius:6px;font-weight:bold;text-decoration:none;display:inline-block;">
                Kirim ke WhatsApp
                </a>
            ''', unsafe_allow_html=True)
