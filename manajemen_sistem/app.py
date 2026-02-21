import streamlit as st
import sqlite3
from modules.auth import check_login, logout
from modules.navbar import horizontal_navbar
from modules.utils import get_dashboard_stats, get_announcements, add_announcement, get_mahasiswa_tasks, get_pendamping_materials
from database import init_database
import pandas as pd
import plotly.express as px
from datetime import datetime

# Config
st.set_page_config(
    page_title="Dashboard Bintrebusih",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inisialisasi database
init_database()

# Check login
check_login()

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Navigation Bar Horizontal
menu = horizontal_navbar()

# ================== DASHBOARD ==================
if menu == "Dashboard":
    role = st.session_state.get('role', 'Unknown')
    
    if role == "Admin":
        # ========== ADMIN DASHBOARD ==========
        col_title, col_button = st.columns([4, 1])
        with col_title:
            st.title("📊 Dashboard Admin")
        with col_button:
            st.write("")
            st.write("")
            if st.button("🔄 Refresh Data"):
                st.rerun()
        
        # Get stats
        stats = get_dashboard_stats()
        
        # Top Metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("👨‍🎓 Mahasiswa Aktif", f"{stats['mahasiswa_aktif']}", "+5 bulan ini", 
                     delta_color="off")
        
        with col2:
            st.metric("👨‍🏫 Pendamping", f"{stats['total_pendamping']}", "", delta_color="off")
        
        with col3:
            st.metric("🏢 Mitra Kerja", f"{stats['total_mitra']}", "", delta_color="off")
        
        with col4:
            st.metric("✅ Presensi Hari Ini", f"{stats['presensi_hari_ini']}", "", delta_color="off")
        
        with col5:
            st.metric("📋 Laporan Baru", f"{stats['laporan_baru']}", "hari ini", delta_color="off")
        
        st.divider()

        # Quick Actions — interactive cards
        st.markdown("""
            <style>
            .qa-grid { display:flex; gap:12px; flex-wrap:wrap; margin: 8px 0 18px 0; }
            .qa-card { background: linear-gradient(135deg,#0ea5e977,#06b6d477); border-radius:12px; padding:12px 14px; color:white; min-width:140px; text-align:center; box-shadow: 0 8px 30px rgba(2,6,23,0.35); transition: transform .12s ease, box-shadow .12s ease; }
            .qa-card:hover { transform: translateY(-6px); box-shadow: 0 20px 48px rgba(2,6,23,0.45); }
            .qa-emoji { font-size:22px; display:block; }
            .qa-label { margin-top:8px; font-weight:700; font-size:14px; }
            @media (max-width: 900px) { .qa-card { min-width:110px; padding:10px; } }
            </style>
        """, unsafe_allow_html=True)

        col_q1, col_q2, col_q3, col_q4, col_q5, col_q6, col_q7, col_q8 = st.columns(8)

        with col_q1:
            if st.button("📊\nDashboard", key="qa_dashboard", use_container_width=True):
                st.session_state.selected_menu = "Dashboard"
        with col_q2:
            if st.button("👥\nManajemen Data", key="qa_manajemen", use_container_width=True):
                st.session_state.selected_menu = "Manajemen Data"
        with col_q3:
            if st.button("📍\nPresensi", key="qa_presensi", use_container_width=True):
                st.session_state.selected_menu = "Presensi"
        with col_q4:
            if st.button("📚\nPendampingan", key="qa_pendamping", use_container_width=True):
                st.session_state.selected_menu = "Pendampingan"
        with col_q5:
            if st.button("📋\nLaporan", key="qa_laporan", use_container_width=True):
                st.session_state.selected_menu = "Laporan"
        with col_q6:
            if st.button("📢\nPengumuman", key="qa_pengumuman", use_container_width=True):
                st.session_state.selected_menu = "Pengumuman"
        with col_q7:
            if st.button("⚙️\nPengaturan", key="qa_settings", use_container_width=True):
                st.session_state.selected_menu = "Pengaturan"
        with col_q8:
            if st.button("🚪\nLogout", key="qa_logout", use_container_width=True):
                logout()

        # Grafik & Tabel
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📈 Tren Kehadiran 7 Hari Terakhir")
            data = pd.DataFrame({
                'Tanggal': pd.date_range(start='2025-02-12', periods=7),
                'Hadir': [25, 28, 26, 27, 29, 24, 30],
                'Izin': [3, 2, 4, 1, 2, 5, 1],
                'Tidak Hadir': [2, 0, 0, 2, 1, 1, 1]
            })
            fig = px.bar(data, x='Tanggal', y=['Hadir', 'Izin', 'Tidak Hadir'], barmode='stack',
                        color_discrete_map={'Hadir': '#10B981', 'Izin': '#F59E0B', 'Tidak Hadir': '#EF4444'})
            fig.update_layout(height=350, showlegend=True)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📊 Distribusi Mahasiswa per Mitra")
            mitra_data = pd.DataFrame({
                'Mitra': ['PT Telkom', 'PT PLN', 'Bank BCA', 'BUMN Konstruksi'],
                'Jumlah': [12, 15, 10, 8]
            })
            fig = px.pie(mitra_data, values='Jumlah', names='Mitra', hole=0.3)
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # Data Summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("📌 **Ringkasan Cepatnya**")
            from modules.crud import read_all_mahasiswa, read_all_pendamping, read_all_mitra_kerja
            mahasiswas = read_all_mahasiswa()
            pendampings = read_all_pendamping()
            mitras = read_all_mitra_kerja()
            st.write(f"- Total Mahasiswa: **{len(mahasiswas)}**")
            st.write(f"- Total Pendamping: **{len(pendampings)}**")
            st.write(f"- Total Mitra: **{len(mitras)}**")
        
        with col2:
            st.warning("⚠️ **Perlu Perhatian**")
            st.write("- Mahasiswa belum hadir: **3**")
            st.write("- Laporan tertunda: **2**")
            st.write("- Presensi kurang: **5**")
        
        with col3:
            st.success("✅ **Status Baik**")
            st.write("- Target presensi tercapai: **95%**")
            st.write("- Materi terisi: **100%**")
            st.write("- Sistem running: **Normal**")
    
    elif role == "Pendamping":
        # ========== PENDAMPING DASHBOARD ==========
        col_title, col_button = st.columns([4, 1])
        with col_title:
            st.title("📊 Dashboard Pendamping")
        with col_button:
            st.write("")
            st.write("")
            if st.button("🔄 Refresh Data", key="refresh_pendamping"):
                st.rerun()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📚 Materi Uploaded", "5", "+2 minggu ini", delta_color="off")
        
        with col2:
            st.metric("📋 Laporan Submitted", "12", "tahun ini", delta_color="off")
        
        with col3:
            st.metric("👨‍🎓 Mahasiswa Dibimbing", "6", "aktif", delta_color="off")
        
        with col4:
            st.metric("⏳ Jadwal Minggu Ini", "4", "sesi", delta_color="off")
        
        st.divider()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📋 Aktivitas Terakhir")
            
            activity = pd.DataFrame({
                'Aktivitas': [
                    '✅ Upload Materi: Database Design',
                    '📤 Submit Laporan: Minggu Ke-5',
                    '✏️ Edit Materi: SQL Basics',
                    '👨‍🎓 Bimbing: Budi Santoso',
                    '📊 Update Progress: Siti Nurhaliza'
                ],
                'Waktu': ['2 jam lalu', '1 hari lalu', '3 hari lalu', '1 minggu lalu', '10 hari lalu']
            })
            st.dataframe(activity, use_container_width=True, hide_index=True)
        
        with col2:
            st.subheader("👥 Mahasiswa Bimbing")
            mahasiswa = pd.DataFrame({
                'Nama': ['Budi Santoso', 'Siti Nurhaliza', 'Ahmad Rifqi', 'Dewi Lestari', 'Rini Wijaya', 'Hardi Pratama'],
                'Progress': [85, 90, 75, 88, 92, 78]
            })
            
            for idx, row in mahasiswa.iterrows():
                col_text, col_progress = st.columns([3, 2])
                with col_text:
                    st.write(f"**{row['Nama']}**")
                with col_progress:
                    st.progress(row['Progress']/100)
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📅 Jadwal Minggu Ini")
            jadwal = pd.DataFrame({
                'Hari': ['Senin', 'Selasa', 'Rabu', 'Kamis'],
                'Jam': ['10:00', '14:00', '09:00', '15:00'],
                'Materi': ['Database Design', 'Web Development', 'Testing', 'Security']
            })
            st.dataframe(jadwal, use_container_width=True, hide_index=True)
        
        with col2:
            st.subheader("📊 Kategori Laporan")
            laporan_data = pd.DataFrame({
                'Kategori': ['Laporan Rutin', 'Laporan Khusus', 'Evaluasi'],
                'Jumlah': [8, 2, 2]
            })
            fig = px.bar(laporan_data, x='Kategori', y='Jumlah', 
                        color='Kategori',
                        color_discrete_sequence=['#3B82F6', '#8B5CF6', '#EC4899'])
            fig.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    elif role == "Mahasiswa":
        # ========== MAHASISWA DASHBOARD ==========
        username = st.session_state.get('username', 'Mahasiswa')
        
        col_title, col_button = st.columns([4, 1])
        with col_title:
            st.title(f"👋 Selamat datang, {username}!")
        with col_button:
            st.write("")
            st.write("")
            if st.button("🔄 Refresh", key="refresh_mhs"):
                st.rerun()
        
        # Top Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
                <div style="background-color:#10B981; padding:20px; border-radius:10px; text-align:center">
                    <h3 style="color:white; margin:0">📤 Tugas</h3>
                    <h1 style="color:white; margin:10px 0">8/10</h1>
                    <p style="color:white; margin:0">Dikumpulkan</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div style="background-color:#F59E0B; padding:20px; border-radius:10px; text-align:center">
                    <h3 style="color:white; margin:0">⏳ Tertunda</h3>
                    <h1 style="color:white; margin:10px 0">2</h1>
                    <p style="color:white; margin:0">Menunggu Submit</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
                <div style="background-color:#3B82F6; padding:20px; border-radius:10px; text-align:center">
                    <h3 style="color:white; margin:0">📚 Materi</h3>
                    <h1 style="color:white; margin:10px 0">15</h1>
                    <p style="color:white; margin:0">Tersedia</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
                <div style="background-color:#8B5CF6; padding:20px; border-radius:10px; text-align:center">
                    <h3 style="color:white; margin:0">💯 Nilai</h3>
                    <h1 style="color:white; margin:10px 0">85</h1>
                    <p style="color:white; margin:0">Rata-rata</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📋 Tugas Mendatang")
            
            tasks = pd.DataFrame({
                'No': [1, 2, 3],
                'Tugas': ['Laporan Database Design', 'Quiz SQL', 'Implementasi Web App'],
                'Deadline': ['23 Feb 2026', '25 Feb 2026', '28 Feb 2026'],
                'Status': ['⏳ Belum Dikumpulkan', '⏳ Belum Dikerjakan', '⏳ Belum Dikerjakan']
            })
            st.dataframe(tasks, use_container_width=True, hide_index=True)
            
            if st.button("📤 Upload Tugas Sekarang"):
                st.switch_page("pages/mahasiswa.py")
        
        with col2:
            st.subheader("📅 Kalender")
            
            from datetime import datetime, timedelta
            today = datetime.now()
            
            # Simple calendar view
            st.write(f"**Bulan: {today.strftime('%B %Y')}**")
            
            # Next upcoming dates
            st.write("**Deadline Dekat:**")
            for i in range(1, 4):
                date = today + timedelta(days=i)
                st.write(f"- {date.strftime('%d %b')}: Tugas {i}")
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Progress Pembelajaran")
            
            subjects = pd.DataFrame({
                'Mata Pelajaran': ['Database', 'Web Development', 'Security', 'Testing'],
                'Progress': [85, 70, 75, 80]
            })
            
            for idx, row in subjects.iterrows():
                st.write(f"**{row['Mata Pelajaran']}**")
                st.progress(row['Progress']/100)
                st.write("")
        
        with col2:
            st.subheader("📚 Materi Terbaru")
            
            materi = pd.DataFrame({
                'Judul': [
                    'Database Design Patterns',
                    'REST API Development',
                    'SQL Performance',
                    'Web Security Basics'
                ],
                'Tipe': ['PDF', 'Video', 'PDF', 'Video'],
                'Tanggal': ['19 Feb 2026', '18 Feb 2026', '17 Feb 2026', '16 Feb 2026']
            })
            
            for idx, row in materi.iterrows():
                with st.container():
                    col_icon, col_info, col_btn = st.columns([0.5, 3, 1])
                    with col_icon:
                        icon = "📹" if row['Tipe'] == "Video" else "📄"
                        st.write(icon)
                    with col_info:
                        st.write(f"**{row['Judul']}**")
                        st.caption(f"{row['Tipe']} • {row['Tanggal']}")
                    with col_btn:
                        st.write("📥")
    
    else:
        # ========== MITRA KERJA DASHBOARD ==========
        st.title("📊 Dashboard Mitra Kerja")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("👨‍🎓 Mahasiswa", "5", "aktif")
        
        with col2:
            st.metric("📊 Laporan", "3", "bulan ini")
        
        with col3:
            st.metric("✅ Rating", "4.8/5", "dari mahasiswa")
        
        st.divider()
        
        st.subheader("📋 Daftar Mahasiswa di Perusahaan")
        
        mahasiswa_mitra = pd.DataFrame({
            'Nama': ['Budi Santoso', 'Siti Nurhaliza', 'Ahmad Rifqi', 'Dewi Lestari', 'Rini Wijaya'],
            'NIM': ['20230101', '20230102', '20230103', '20230104', '20230105'],
            'Departemen': ['IT', 'HR', 'Finance', 'IT', 'Marketing'],
            'Status': ['Aktif', 'Aktif', 'Aktif', 'Cuti', 'Aktif'],
            'Supervisor': ['Bapak Adi', 'Ibu Tina', 'Bapak Adi', 'Ibu Rini', 'Bapak Hendra']
        })
        st.dataframe(mahasiswa_mitra, use_container_width=True, hide_index=True)


# ================== UPLOAD TUGAS (MAHASISWA) ==================
elif menu == "Upload Tugas":
    st.title("📤 Upload Tugas Anda")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Tugas yang Harus Dikumpulkan")
        
        tasks = pd.DataFrame({
            'No': [1, 2, 3],
            'Judul Tugas': ['Bagian 1: Setup Lingkungan', 'Bagian 2: CRUD Operations', 'Bagian 3: API Testing'],
            'Deadline': ['18 Feb 2026', '25 Feb 2026', '04 Mar 2026'],
            'Status': ['Belum Dikumpulkan', 'Belum Dikumpulkan', 'Belum Dikumpulkan']
        })
        st.dataframe(tasks, use_container_width=True, hide_index=True)
        
        st.write("---")
        st.subheader("Upload Tugas")
        
        task_select = st.selectbox("Pilih Tugas", ["Bagian 1: Setup Lingkungan", "Bagian 2: CRUD Operations", "Bagian 3: API Testing"])
        
        col_file, col_note = st.columns([1, 1])
        
        with col_file:
            uploaded_file = st.file_uploader("📎 Upload File Tugas", type=["pdf", "docx", "zip", "rar"])
        
        with col_note:
            catatan = st.text_area("Catatan (opsional)")
        
        if st.button("✅ Kirim Tugas", use_container_width=True):
            if uploaded_file:
                st.success(f"✅ Tugas '{task_select}' berhasil dikumpulkan!")
                st.balloons()
            else:
                st.error("❌ Pilih file terlebih dahulu")
    
    with col2:
        st.subheader("📋 Panduan Upload")
        st.info("""
        Sebelum upload:
        - Pastikan semua file lengkap
        - Format: PDF, DOCX, ZIP, RAR
        - Max size: 50MB
        - Kirim sebelum deadline
        """)


# ================== TUGAS SAYA (MAHASISWA) ==================
elif menu == "Tugas Saya":
    st.title("📭 Tugas Saya")
    
    tab1, tab2 = st.tabs(["Dikumpulkan", "Nilai"])
    
    with tab1:
        submitted = pd.DataFrame({
            'No': [1, 2],
            'Tugas': ['Bagian 1: Setup Lingkungan', 'Bagian 2: CRUD Operations'],
            'Dikumpulkan': ['15 Feb 2026', '22 Feb 2026'],
            'Diterima': ['16 Feb 2026', '23 Feb 2026'],
            'Status': ['Diterima', 'Diterima']
        })
        st.dataframe(submitted, use_container_width=True, hide_index=True)
    
    with tab2:
        grades = pd.DataFrame({
            'Tugas': ['Bagian 1: Setup Lingkungan', 'Bagian 2: CRUD Operations'],
            'Nilai': ['90', '85'],
            'Feedback': ['Excellent work!', 'Good, needs improvement on error handling']
        })
        st.dataframe(grades, use_container_width=True, hide_index=True)


# ================== MATERI PEMBELAJARAN (MAHASISWA) ==================
elif menu == "Materi Pembelajaran":
    st.title("📚 Materi Pembelajaran")
    
    materials = get_pendamping_materials()
    
    if len(materials) > 0:
        col1, col2 = st.columns([3, 1])
        
        with col2:
            st.subheader("Kategori")
            kategori = st.multiselect("Filter", ["Semua", "Video", "Document", "Code"])
        
        with col1:
            st.subheader("Daftar Materi")
        
        # Dummy materials
        for i in range(1, 6):
            col_icon, col_info, col_btn = st.columns([0.5, 3, 1])
            
            with col_icon:
                st.write("📄")
            
            with col_info:
                st.write(f"**Materi {i}: Database Design & Optimization**")
                st.caption("Di-upload oleh: Ibu Sita Dewi | 5 Feb 2026")
            
            with col_btn:
                if st.button("📥 Download", key=f"download_{i}"):
                    st.success("Download started!")
    else:
        st.info("📭 Belum ada materi pembelajaran")


# ================== UPLOAD MATERI (PENDAMPING) ==================
elif menu == "Upload Materi":
    st.title("📥 Upload Materi Pembelajaran")
    
    st.subheader("Tambah Materi Baru")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        judul = st.text_input("Judul Materi")
        kategori = st.selectbox("Kategori", ["Video", "Document", "Code", "Presentation"])
    
    with col2:
        deskripsi = st.text_area("Deskripsi")
        file = st.file_uploader("📎 Upload File Materi")
    
    col_submit, col_cancel = st.columns(2)
    
    with col_submit:
        if st.button("✅ Upload Materi", use_container_width=True):
            if judul and file:
                st.success(f"✅ Materi '{judul}' berhasil di-upload!")
                st.balloons()
            else:
                st.error("❌ Lengkapi semua field terlebih dahulu")
    
    with col_cancel:
        if st.button("❌ Batal", use_container_width=True):
            st.info("Dibatalkan")
    
    st.divider()
    st.subheader("Materi Saya")
    
    my_materials = pd.DataFrame({
        'Judul': ['Database Design', 'SQL Basics', 'Web Development'],
        'Kategori': ['Document', 'Video', 'Code'],
        'Di-upload': ['5 Feb 2026', '3 Feb 2026', '1 Feb 2026'],
        'Status': ['Active', 'Active', 'Active']
    })
    st.dataframe(my_materials, use_container_width=True, hide_index=True)


# ================== UPLOAD LAPORAN (PENDAMPING) ==================
elif menu == "Upload Laporan":
    st.title("📤 Upload Laporan Pendampingan")
    
    st.subheader("Buat Laporan Baru")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        jenis = st.selectbox("Jenis Laporan", ["Laporan Harian", "Laporan Mingguan", "Laporan Bulanan"])
        judul = st.text_input("Judul Laporan")
    
    with col2:
        tanggal = st.date_input("Tanggal Laporan")
        file = st.file_uploader("📎 Upload File Laporan (PDF/Word)")
    
    konten = st.text_area("Konten Laporan", height=200)
    
    col_submit, col_cancel = st.columns(2)
    
    with col_submit:
        if st.button("✅ Kirim Laporan", use_container_width=True):
            if judul and konten:
                st.success(f"✅ Laporan '{judul}' berhasil dikumpulkan!")
                st.balloons()
            else:
                st.error("❌ Lengkapi semua field terlebih dahulu")
    
    with col_cancel:
        if st.button("❌ Batal", use_container_width=True):
            st.info("Dibatalkan")
    
    st.divider()
    st.subheader("Laporan Saya")
    
    my_reports = pd.DataFrame({
        'Judul': ['Laporan Aktivitas Minggu 1', 'Laporan Aktivitas Minggu 2', 'Laporan Bulanan'],
        'Jenis': ['Laporan Mingguan', 'Laporan Mingguan', 'Laporan Bulanan'],
        'Tanggal': ['12 Feb 2026', '19 Feb 2026', '28 Feb 2026'],
        'Status': ['Approved', 'Pending', 'Approved']
    })
    st.dataframe(my_reports, use_container_width=True, hide_index=True)


# ================== PENGUMUMAN (SEMUA USER) ==================
elif menu == "Pengumuman":
    st.title("📢 Pengumuman")
    
    role = st.session_state.get('role', 'Unknown')
    
    # Form tambah pengumuman hanya untuk Admin dan Pendamping
    if role in ["Admin", "Pendamping"]:
        st.subheader("📝 Buat Pengumuman Baru")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            judul = st.text_input("Judul Pengumuman")
        
        with col2:
            # Placeholder untuk priority
            priority = st.selectbox("Prioritas", ["Normal", "Penting", "Urgent"])
        
        isi = st.text_area("Isi Pengumuman", height=150)
        
        col_submit, col_cancel = st.columns(2)
        
        with col_submit:
            if st.button("📤 Posting Pengumuman", use_container_width=True):
                if judul and isi:
                    if add_announcement(judul, isi):
                        st.success("✅ Pengumuman berhasil diposting!")
                        st.rerun()
                    else:
                        st.error("❌ Gagal memposting pengumuman")
                else:
                    st.error("❌ Lengkapi semua field terlebih dahulu")
        
        with col_cancel:
            if st.button("❌ Batal", use_container_width=True):
                st.info("Dibatalkan")
        
        st.divider()
    
    st.subheader("📌 Daftar Pengumuman")
    
    # Dummy announcements
    announcements = [
        {
            'judul': 'Pembaruan Jadwal Pendampingan',
            'isi': 'Jadwal pendampingan telah diperbarui untuk bulan Maret. Silahkan cek email untuk detail lengkapnya.',
            'dibuat_oleh': 'Admin',
            'tanggal': '19 Feb 2026'
        },
        {
            'judul': 'Reminder: Pengumpulan Laporan',
            'isi': 'Mohon segera mengumpulkan laporan mingguan Anda sebelum hari Jumat pukul 17:00.',
            'dibuat_oleh': 'Ibu Sita Dewi',
            'tanggal': '18 Feb 2026'
        },
        {
            'judul': 'Materi Baru: Database Optimization',
            'isi': 'Materi terbaru tentang Database Optimization telah tersedia di menu Materi Pembelajaran.',
            'dibuat_oleh': 'Ibu Sita Dewi',
            'tanggal': '17 Feb 2026'
        }
    ]
    
    for ann in announcements:
        col_title, col_date = st.columns([4, 1])
        
        with col_title:
            st.write(f"**{ann['judul']}**")
        
        with col_date:
            st.caption(ann['tanggal'])
        
        st.write(f"*{ann['isi']}*")
        st.caption(f"📝 Oleh: {ann['dibuat_oleh']}")
        st.divider()


# ================== MANAJEMEN DATA (ADMIN) ==================
elif menu == "Manajemen Data":
    st.title("👥 Manajemen Data")
    
    st.info("🔗 Gunakan menu sidebar untuk mengakses halaman manajemen data yang lebih lengkap")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("👨‍🎓 Kelola Mahasiswa", use_container_width=True):
            st.switch_page("pages/mahasiswa.py")
    
    with col2:
        if st.button("👨‍🏫 Kelola Pendamping", use_container_width=True):
            st.switch_page("pages/pendamping.py")
    
    with col3:
        if st.button("🏢 Kelola Mitra Kerja", use_container_width=True):
            st.switch_page("pages/mitra_kerja.py")
    
    st.divider()
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Ringkasan",
        "👨‍🎓 Mahasiswa", 
        "👨‍🏫 Pendamping",
        "🏢 Mitra Kerja"
    ])
    
    with tab1:
        st.subheader("📊 Ringkasan Data")
        
        from modules.crud import read_all_mahasiswa, read_all_pendamping, read_all_mitra_kerja
        
        mahasiswas = read_all_mahasiswa()
        pendampings = read_all_pendamping()
        mitras = read_all_mitra_kerja()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("👨‍🎓 Total Mahasiswa", len(mahasiswas))
        with col2:
            st.metric("👨‍🏫 Total Pendamping", len(pendampings))
        with col3:
            st.metric("🏢 Total Mitra Kerja", len(mitras))
    
    with tab2:
        st.subheader("Data Mahasiswa")
        
        mahasiswa_data = read_all_mahasiswa()
        if mahasiswa_data:
            df = pd.DataFrame(mahasiswa_data)
            df = df[['nama', 'nim', 'email', 'unit', 'status']]
            df.columns = ['Nama', 'NIM', 'Email', 'Unit', 'Status']
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada data mahasiswa")
    
    with tab3:
        st.subheader("Data Pendamping")
        
        pendamping_data = read_all_pendamping()
        if pendamping_data:
            df = pd.DataFrame(pendamping_data)
            df = df[['nama', 'nip', 'email', 'no_hp', 'total_mahasiswa']]
            df.columns = ['Nama', 'NIP', 'Email', 'No HP', 'Total Mahasiswa']
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada data pendamping")
    
    with tab4:
        st.subheader("Data Mitra Kerja")
        
        mitra_data = read_all_mitra_kerja()
        if mitra_data:
            df = pd.DataFrame(mitra_data)
            df = df[['nama_organisasi', 'lokasi', 'penanggung_jawab', 'kontak_email', 'total_mahasiswa']]
            df.columns = ['Organisasi', 'Lokasi', 'PJ', 'Email', 'Total Mahasiswa']
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada data mitra kerja")


# ================== PRESENSI (ADMIN) ==================
elif menu == "Presensi":
    st.switch_page("pages/presensi.py")


# ================== PENDAMPINGAN (ADMIN) ==================
elif menu == "Pendampingan":
    st.title("📚 Manajemen Pendampingan")
    
    tab1, tab2 = st.tabs(["📅 Jadwal Pendampingan", "📋 Riwayat Pendampingan"])
    
    with tab1:
        st.subheader("Jadwal Pendampingan")
        
        jadwal = pd.DataFrame({
            'Tanggal': ['20 Feb 2026', '21 Feb 2026', '22 Feb 2026'],
            'Jam': ['10:00 - 12:00', '14:00 - 16:00', '09:00 - 11:00'],
            'Pendamping': ['Ibu Sita', 'Pak Budi', 'Ibu Dewi'],
            'Mahasiswa': ['Budi Santoso', 'Siti Nurhaliza', 'Ahmad Rifqi'],
            'Topik': ['Database Design', 'Web Development', 'Testing'],
            'Lokasi': ['Kantor', 'Mitra Kerja', 'Online']
        })
        
        st.dataframe(jadwal, use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("Riwayat Pendampingan")
        
        riwayat = pd.DataFrame({
            'Tanggal': ['19 Feb 2026', '18 Feb 2026', '17 Feb 2026'],
            'Pendamping': ['Ibu Sita', 'Pak Budi', 'Ibu Dewi'],
            'Mahasiswa': ['Budi Santoso', 'Siti Nurhaliza', 'Ahmad Rifqi'],
            'Topik': ['Database Design', 'Web Development', 'Testing'],
            'Durasi': ['2 jam', '2 jam', '1.5 jam'],
            'Status': ['Selesai', 'Selesai', 'Selesai']
        })
        
        st.dataframe(riwayat, use_container_width=True, hide_index=True)


# ================== LAPORAN (ADMIN) ==================
elif menu == "Laporan":
    st.title("📋 Manajemen Laporan")
    
    tab1, tab2, tab3 = st.tabs(["📊 Laporan Pendamping", "📈 Laporan Mahasiswa", "📉 Laporan Mitra"])
    
    with tab1:
        st.subheader("Laporan Pendamping")
        
        laporan = pd.DataFrame({
            'Tanggal': ['19 Feb 2026', '18 Feb 2026', '17 Feb 2026'],
            'Pendamping': ['Ibu Sita', 'Pak Budi', 'Ibu Dewi'],
            'Judul': ['Laporan Minggu Ke-3', 'Laporan Minggu Ke-2', 'Laporan Minggu Ke-1'],
            'Status': ['Approved', 'Pending', 'Approved'],
            'Aksi': ['Lihat', 'Lihat', 'Lihat']
        })
        
        st.dataframe(laporan, use_container_width=True, hide_index=True)
    
    with tab2:
        st.write("📭 Belum ada laporan mahasiswa")
    
    with tab3:
        st.write("📭 Belum ada laporan mitra")


# ================== PENGATURAN ==================
elif menu == "Pengaturan":
    st.title("⚙️ Pengaturan Sistem")
    
    tab1, tab2, tab3 = st.tabs(["👤 Profil", "🔒 Keamanan", "📧 Notifikasi"])
    
    with tab1:
        st.subheader("Profil Pengguna")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            nama = st.text_input("Nama Lengkap", value=st.session_state.get('username', ''))
            email = st.text_input("Email")
        
        with col2:
            no_hp = st.text_input("No. Telepon")
            role = st.text_input("Role", value=st.session_state.get('role', ''), disabled=True)
        
        if st.button("💾 Simpan Perubahan"):
            st.success("✅ Profil berhasil diperbarui!")
    
    with tab2:
        st.subheader("Keamanan Akun")
        
        password_lama = st.text_input("Password Lama", type="password")
        password_baru = st.text_input("Password Baru", type="password")
        password_konfirm = st.text_input("Konfirmasi Password", type="password")
        
        if st.button("🔄 Ubah Password"):
            if password_baru == password_konfirm:
                st.success("✅ Password berhasil diubah!")
            else:
                st.error("❌ Password tidak cocok!")
    
    with tab3:
        st.subheader("Notifikasi")
        
        st.checkbox("Email Notifikasi", value=True)
        st.checkbox("Pengumuman Penting", value=True)
        st.checkbox("Laporan Baru", value=True)
        st.checkbox("Presensi", value=False)


# ================== LOGOUT ==================
elif menu == "Logout":
    logout()
    st.rerun()
