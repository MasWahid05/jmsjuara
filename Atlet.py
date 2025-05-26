import streamlit as st
from datetime import datetime
import urllib.parse
import requests
import io
import os

# Menambahkan logo di bagian atas aplikasi
st.set_page_config(page_title="Aplikasi Absensi Atlet JMS JUARA", page_icon="🏃‍♂️")
# Path ke gambar
logo_path = "LOGO.png"
# Memeriksa apakah file gambar ada
if os.path.exists(logo_path):
    # Membuat kolom untuk memusatkan logo dan judul
    col1, col2, col3 = st.columns([100, 10, 40])  # Membagi kolom dengan proporsi
    with col2:  # Menggunakan kolom tengah
        st.image(logo_path, width=310)  # Menggunakan st.image untuk menampilkan logo
        st.markdown(
            "<h5 style='text-align: center;'>Aplikasi Absensi Atlet JMS JUARA</h5>",
            unsafe_allow_html=True
        )
else:
    st.error("Gambar logo tidak ditemukan. Pastikan path gambar benar.")

programs_by_category = {
    "Badminton": [
        "Footwork Drill Circuit",
        "Smash Practice 100 reps",
        "Net Play Technique",
        "Doubles Strategy Session",
        "Agility Ladder Training",
        "Serve Accuracy Drill",
        "Clear Shot Consistency",
        "Drive Shot Exercise",
        "Defense Reaction Training",
        "Jump Smash Practice",
        "Mixed Doubles Coordination",
        "Drop Shot Practice",
        "Overhead Clear Drill",
        "Shadow Play Movement",
        "Conditioning Sprints",
        "Backhand Net Shots",
        "Crosscourt Net Play",
        "Smash Recovery Drill",
        "Reaction Time Test",
        "Endurance Rally Training"
    ],
    "Sprinter": [
        "30m Acceleration Drill 10x",
        "Flying 50m Sprints 6x",
        "Explosive Start Practice",
        "Block Start Technique",
        "Resisted Sprint with Parachute",
        "Short Sprints with Recovery",
        "Acceleration Phase Drills",
        "Speed Endurance Runs",
        "Standing Start Sprints",
        "Plyometric Box Jumps",
        "Sprint Technique Analysis",
        "Speed Ladder Drills",
        "Hill Sprints for Power",
        "Reaction Time Sprints",
        "Treadmill Sprints dengan Incline"
    ],
    "Middle Distance": [
        "800m Interval 5x",
        "1000m Tempo Run",
        "1200m Repeats 4x",
        "400m Recovery Jog",
        "1500m Time Trial",
        "600m Speed Endurance",
        "300m Fast Repeats 8x",
        "Long Run (8-10km)",
        "Pyramid Intervals (400m, 800m, 1200m)",
        "Hill Repeats for Strength",
        "Fartlek Training Session",
        "Race Pace Practice",
        "Drills for Running Form",
        "Cooldown Jog (10-15 min)",
        "Dynamic Stretching Routine"
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

def upload_to_imgur(image):
    client_id = '677f3d0e9999a04'  # Ganti dengan Client ID Imgur Anda
    headers = {'Authorization': f'Client-ID {client_id}'}
    
    # Mengupload gambar ke Imgur dengan SSL verification disabled (hanya untuk pengujian)
    response = requests.post("https://api.imgur.com/3/image", headers=headers, files={'image': image}, verify=False)
    
    if response.status_code == 200:
        return response.json()['data']['link']  # Mengembalikan URL gambar
    else:
        st.error("Gagal mengupload gambar ke Imgur.")
        st.error(f"Status Code: {response.status_code}, Response: {response.text}")  # Menampilkan status dan respons
        return None

def create_whatsapp_link(nama, program, tanggal, status, foto_url, alasan=None):
    message = (
        f"Absensi Atlet JMS Juara\n"
        f"Nama Atlet: {nama}\n"
        f"Program: {program}\n"
        f"Tanggal Absen: {tanggal}\n"
        f"Status Absen: {status}\n"
        f"Foto: {foto_url}\n"
    )
    if alasan:
        message += f"Alasan: {alasan}\n"
    
    encoded_message = urllib.parse.quote(message)
    return f"https://api.whatsapp.com/send?text={encoded_message}"

# Buat dua kolom utama: kiri untuk tombol kategori, kanan untuk formulir
col_left, col_right = st.columns([1, 3])

with col_right:
    with st.form(key='absensi_form'):
        status_absen = st.selectbox("Status Absen", ["Pilih Status", "Hadir", "Tidak Hadir"])  # Menambahkan opsi "Pilih Status"
        nama_atlet = st.text_input("Nama Atlet")
        tanggal_absen = st.date_input("Tanggal Absen", datetime.today())

        # Tombol untuk mengonfirmasi pilihan status absen
        submit_status_button = st.form_submit_button(label="Konfirmasi Status")

        # Menampilkan menu kategori program jika status absen adalah "Hadir"
        if submit_status_button:
            if status_absen == "Hadir":
                st.session_state.status = "Hadir"
                st.session_state.program = None  # Reset program
                st.session_state.alasan = None  # Reset alasan
            elif status_absen == "Tidak Hadir":
                st.session_state.status = "Tidak Hadir"
                st.session_state.program = None  # Reset program
                st.session_state.alasan = None  # Reset alasan
            else:
                st.session_state.status = None  # Reset status jika tidak ada pilihan

        # Menampilkan menu kategori program jika status absen adalah "Hadir"
        if 'status' in st.session_state and st.session_state.status == "Hadir":
            st.markdown("### Pilih Kategori Program")
            selected_category = st.selectbox("Pilih Kategori Program", list(programs_by_category.keys()), index=list(programs_by_category.keys()).index(st.session_state.selected_category))
            st.session_state.selected_category = selected_category  # Simpan kategori yang dipilih
            
            # Input program latihan yang akan dilakukan
            program_latihan = st.text_input("Program Latihan yang Dilakukan")  # Input program latihan
            st.session_state.program = program_latihan  # Simpan program latihan yang dimasukkan
        elif 'status' in st.session_state and st.session_state.status == "Tidak Hadir":
            st.session_state.program = None  # Set program ke None jika tidak hadir
            st.session_state.alasan = st.text_input("Alasan Tidak Hadir")  # Input alasan

        # Input foto dan tombol kirim hanya muncul setelah konfirmasi status
        if 'status' in st.session_state and st.session_state.status is not None:
            foto = st.camera_input("Ambil Foto Atlet")
            submit_button = st.form_submit_button(label="Kirim")

            # Tampilkan foto yang diambil jika tersedia
            if foto is not None:
                st.image(foto, caption="Foto Atlet")  # Menghapus use_container_width

            # Logika untuk mengirim data
            if submit_button:
                if not nama_atlet.strip():
                    st.error("Nama atlet tidak boleh kosong.")
                elif tanggal_absen > datetime.today().date():
                    st.error("Tanggal absen tidak boleh di masa depan.")
                elif foto is None:
                    st.error("Foto atlet harus diambil.")
                elif st.session_state.status == "Tidak Hadir" and (st.session_state.alasan is None or not st.session_state.alasan.strip()):
                    st.error("Alasan tidak hadir harus diisi.")
                else:
                    # Simpan foto ke buffer
                    foto_buffer = io.BytesIO(foto.getbuffer())

                    # Upload foto ke Imgur dan dapatkan URL-nya
                    foto_url = upload_to_imgur(foto_buffer)

                    if foto_url:
                        whatsapp_url = create_whatsapp_link(
                            nama_atlet.strip(),
                            st.session_state.program if st.session_state.status == "Hadir" else "Tidak Ada Program",  # Set program ke "Tidak Ada Program" jika tidak hadir
                            tanggal_absen.strftime("%Y-%m-%d"),
                            st.session_state.status,
                            foto_url,
                            st.session_state.alasan.strip() if st.session_state.status == "Tidak Hadir" else None
                        )
                        st.success("Data siap dikirim melalui WhatsApp!")
                        st.markdown(f'''
                            <a href="{whatsapp_url}" target="_blank" 
                            style="background-color:#25D366;color:white;padding:12px 24px;
                            border-radius:6px;font-weight:bold;text-decoration:none;display:inline-block;">
                            Kirim ke WhatsApp
                            </a>
                        ''', unsafe_allow_html=True)
