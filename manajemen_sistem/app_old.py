import streamlit as st
import sqlite3
from modules.auth import check_login, logout
from modules.utils import sidebar_menu, get_dashboard_stats
from database import init_database
import pandas as pd
import plotly.express as px
from datetime import datetime

# Config
# (page config moved to app.py - keep single global config there)

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

# Sidebar Menu
menu = sidebar_menu()

# ================== DASHBOARD PAGE ==================
if menu == "📊 Dashboard":
    st.title("📊 Dashboard Utama")
    
    # Get stats
    stats = get_dashboard_stats()
    
    # Top Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("👨‍🎓 Mahasiswa Aktif", stats['mahasiswa_aktif'], "+5 bulan ini")
    
    with col2:
        st.metric("👨‍🏫 Pendamping", stats['total_pendamping'], "")
    
    with col3:
        st.metric("🏢 Mitra Kerja", stats['total_mitra'], "")
    
    with col4:
        st.metric("✅ Presensi Hari Ini", stats['presensi_hari_ini'], "")
    
    with col5:
        st.metric("📋 Laporan Baru", stats['laporan_baru'], "hari ini")
    
    st.divider()
    
    # Grafik & Tabel
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📈 Tren Kehadiran 7 Hari Terakhir")
        
        # Dummy data
        data = pd.DataFrame({
            'Tanggal': pd.date_range(start='2025-02-12', periods=7),
            'Hadir': [25, 28, 26, 27, 29, 24, 30],
            'Izin': [3, 2, 4, 1, 2, 5, 1],
            'Tidak Hadir': [2, 0, 0, 2, 1, 1, 1]
        })
        
        fig = px.bar(data, x='Tanggal', y=['Hadir', 'Izin', 'Tidak Hadir'], 
                     title="", barmode='stack')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Distribusi Mahasiswa per Mitra")
        
        # Dummy data
        mitra_data = pd.DataFrame({
            'Mitra': ['PT Telkom', 'PT PLN', 'Bank BCA', 'BUMN Konstruksi'],
            'Jumlah': [12, 15, 10, 8]
        })
        
        fig = px.pie(mitra_data, values='Jumlah', names='Mitra', 
                     title="")
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Tabel Cepat
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("⚠️ Mahasiswa Belum Presensi")
        not_present = pd.DataFrame({
            'Nama': ['Budi Santoso', 'Siti Nurhaliza', 'Ahmad Rifqi'],
            'NIM': ['20230101', '20230102', '20230103'],
            'Mitra': ['PT Telkom', 'Bank BCA', 'PT PLN']
        })
        st.dataframe(not_present, use_container_width=True, hide_index=True)
    
    with col2:
        st.subheader("📋 Laporan Tertunda")
        pending = pd.DataFrame({
            'Pendamping': ['Ibu Sita', 'Pak Budi', 'Ibu Dewi'],
            'Tipe': ['Laporan Minggu Ini', 'Laporan Bulanan', 'Laporan Harian'],
            'Deadline': ['2 hari', '1 hari', '4 hari']
        })
        st.dataframe(pending, use_container_width=True, hide_index=True)

# ================== MANAJEMEN DATA ==================
elif menu == "👥 Manajemen Data":
    st.title("👥 Manajemen Data")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Data Mahasiswa",
        "👨‍🏫 Data Pendamping", 
        "🏢 Data Mitra Kerja",
        "👥 Data User"
    ])
    
    with tab1:
        st.subheader("Data Mahasiswa")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            search = st.text_input("🔍 Cari mahasiswa (nama/NIM)")
        with col2:
            if st.button("➕ Tambah Mahasiswa", key="add_mhs"):
                st.session_state.show_form_mhs = True
        
        # Dummy data
        mahasiswa_data = pd.DataFrame({
            'Nama': ['Budi Santoso', 'Siti Nurhaliza', 'Ahmad Rifqi', 'Dewi Lestari'],
            'NIM': ['20230101', '20230102', '20230103', '20230104'],
            'Email': ['budi@email.com', 'siti@email.com', 'ahmad@email.com', 'dewi@email.com'],
            'Mitra': ['PT Telkom', 'Bank BCA', 'PT PLN', 'Bank BCA'],
            'Status': ['Aktif', 'Aktif', 'Aktif', 'Aktif'],
            'Aksi': ['Edit', 'Edit', 'Edit', 'Edit']
        })
        
        st.dataframe(mahasiswa_data, use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("Data Pendamping")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            search = st.text_input("🔍 Cari pendamping (nama/NIP)")
        with col2:
            if st.button("➕ Tambah Pendamping"):
                st.session_state.show_form_pendamping = True
        
        # Dummy data
        pendamping_data = pd.DataFrame({
            'Nama': ['Ibu Sita Dewi', 'Pak Budi Herman', 'Ibu Dewi Kusuma'],
            'NIP': ['19850315', '19800728', '19900101'],
            'Email': ['sita@bintrebusih.or.id', 'budi@bintrebusih.or.id', 'dewi@bintrebusih.or.id'],
            'No HP': ['081234567890', '082345678901', '081345678902'],
            'Mahasiswa Bimbing': [5, 6, 4]
        })
        
        st.dataframe(pendamping_data, use_container_width=True, hide_index=True)
    
    with tab3:
        st.subheader("Data Mitra Kerja")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            search = st.text_input("🔍 Cari mitra (nama organisasi)")
        with col2:
            if st.button("➕ Tambah Mitra"):
                st.session_state.show_form_mitra = True
        
        # Dummy data
        mitra_data = pd.DataFrame({
            'Organisasi': ['PT Telkom', 'Bank BCA', 'PT PLN', 'BUMN Konstruksi'],
            'Lokasi': ['Jakarta Pusat', 'Jakarta Selatan', 'Bandung', 'Surabaya'],
            'PJ': ['A Suryanto', 'Rini Wijaya', 'Budi Setiawan', 'Ahmad Gunawan'],
            'Mahasiswa': [12, 10, 15, 8],
            'Kontak': ['021-1234567', '021-2345678', '022-3456789', '031-4567890']
        })
        
        st.dataframe(mitra_data, use_container_width=True, hide_index=True)
    
    with tab4:
        st.subheader("Data User & Role Sistem")
        
        if st.button("➕ Tambah User"):
            st.session_state.show_form_user = True
        
        # Dummy data
        user_data = pd.DataFrame({
            'Username': ['admin', 'pendamping1', 'mitra1', 'viewer1'],
            'Nama': ['Admin Bintrebusih', 'Ibu Sita', 'PT Telkom', 'Viewer General'],
            'Email': ['admin@bintrebusih.or.id', 'sita@bintrebusih.or.id', 'telkom@pt.or.id', 'viewer@bintrebusih.or.id'],
            'Role': ['Admin', 'Pendamping', 'Mitra Kerja', 'Viewer'],
            'Status': ['Aktif', 'Aktif', 'Aktif', 'Aktif']
        })
        
        st.dataframe(user_data, use_container_width=True, hide_index=True)

# ================== PRESENSI ==================
elif menu == "📝 Presensi":
    st.title("📝 Presensi")
    
    tab1, tab2, tab3 = st.tabs([
        "👨‍🎓 Presensi Mahasiswa",
        "👨‍🏫 Presensi Pendamping",
        "📊 Rekap Presensi"
    ])
    
    with tab1:
        st.subheader("Presensi Mahasiswa")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_mitra = st.selectbox("Filter Mitra", ['Semua', 'PT Telkom', 'Bank BCA', 'PT PLN'])
        with col2:
            filter_unit = st.selectbox("Filter Unit", ['Semua', 'Unit 1', 'Unit 2', 'Unit 3'])
        with col3:
            filter_bulan = st.selectbox("Filter Bulan", ['Februari 2025', 'Januari 2025', 'Desember 2024'])
        
        # Dummy presensi data
        presensi = pd.DataFrame({
            'Nama': ['Budi S.', 'Siti N.', 'Ahmad R.', 'Dewi L.', 'Rudi P.'],
            'NIM': ['20230101', '20230102', '20230103', '20230104', '20230105'],
            'Mitra': ['PT Telkom', 'Bank BCA', 'PT PLN', 'Bank BCA', 'PT Telkom'],
            'Hadir': [24, 25, 23, 24, 25],
            'Izin': [1, 0, 1, 1, 0],
            'Tidak Hadir': [0, 0, 1, 0, 0],
            'Persentase': ['96%', '100%', '92%', '96%', '100%']
        })
        
        st.dataframe(presensi, use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("Presensi Pendamping")
        
        filter_status = st.selectbox("Filter Status", ['Semua', 'Hadir', 'Izin', 'Tidak Hadir'])
        
        # Dummy presensi pendamping
        presensi_pd = pd.DataFrame({
            'Nama': ['Ibu Sita', 'Pak Budi', 'Ibu Dewi', 'Pak Ahmad'],
            'Tanggal': ['19 Feb 2025', '19 Feb 2025', '19 Feb 2025', '19 Feb 2025'],
            'Status': ['Hadir', 'Hadir', 'Izin', 'Hadir'],
            'Lokasi': ['PT Telkom', 'Bank BCA', 'Kantor', 'PT PLN'],
            'Aktivitas': ['Monitoring', 'Mentoring', 'Paid Leave', 'Monitoring']
        })
        
        st.dataframe(presensi_pd, use_container_width=True, hide_index=True)
    
    with tab3:
        st.subheader("Rekap Presensi")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Statistik Kehadiran**")
            recap_stats = pd.DataFrame({
                'Status': ['Hadir', 'Izin', 'Tidak Hadir', 'Total'],
                'Jumlah': [115, 8, 2, 125]
            })
            st.dataframe(recap_stats, use_container_width=True, hide_index=True)
        
        with col2:
            col_export1, col_export2 = st.columns(2)
            with col_export1:
                if st.button("📥 Export PDF"):
                    st.success("✅ PDF berhasil didownload!")
            with col_export2:
                if st.button("📥 Export Excel"):
                    st.success("✅ Excel berhasil didownload!")

# ================== PENDAMPINGAN ==================
elif menu == "📚 Pendampingan":
    st.title("📚 Pendampingan & Materi")
    
    tab1, tab2 = st.tabs(["📤 Upload Materi", "📅 Jadwal Pendampingan"])
    
    with tab1:
        st.subheader("Upload Materi Pendampingan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            pilih_mahasiswa = st.multiselect("Pilih Mahasiswa", 
                ['Budi Santoso', 'Siti Nurhaliza', 'Ahmad Rifqi', 'Dewi Lestari'])
        
        with col2:
            pilih_mitra = st.multiselect("Pilih Mitra (opsional)",
                ['PT Telkom', 'Bank BCA', 'PT PLN'])
        
        judul_materi = st.text_input("Judul Materi")
        deskripsi = st.text_area("Deskripsi Materi", height=100)
        
        uploaded_file = st.file_uploader("Upload File (PDF/PPT/Video)", 
                                         type=['pdf', 'pptx', 'mp4', 'avi'])
        
        if st.button("📤 Upload Materi"):
            if judul_materi and uploaded_file:
                st.success("✅ Materi berhasil diupload!")
            else:
                st.error("❌ Lengkapi data dahulu!")
    
    with tab2:
        st.subheader("Jadwal Pendampingan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("➕ Buat Jadwal"):
                st.session_state.show_jadwal_form = True
        
        with col2:
            filter_bulan = st.selectbox("Filter Bulan", ['Februari 2025', 'Januari 2025'])
        
        # Dummy jadwal
        jadwal = pd.DataFrame({
            'Tanggal': ['19 Feb 2025', '20 Feb 2025', '21 Feb 2025', '24 Feb 2025'],
            'Jam': ['09:00-11:00', '14:00-16:00', '09:00-11:00', '10:00-12:00'],
            'Pendamping': ['Ibu Sita', 'Pak Budi', 'Ibu Dewi', 'Pak Ahmad'],
            'Mahasiswa': ['5 orang', '4 orang', '6 orang', '5 orang'],
            'Lokasi': ['PT Telkom', 'Bank BCA', 'Kantor', 'PT PLN'],
            'Topik': ['Leadership', 'Financial Planning', 'Marketing', 'Technical Skills']
        })
        
        st.dataframe(jadwal, use_container_width=True, hide_index=True)

# ================== LAPORAN ==================
elif menu == "📋 Laporan":
    st.title("📋 Laporan Pendamping")
    
    tab1, tab2, tab3 = st.tabs([
        "📝 Laporan Harian",
        "📊 Laporan Bulanan",
        "📈 Analitik & Insights"
    ])
    
    with tab1:
        st.subheader("Laporan Harian/Mingguan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            pilih_pendamping = st.selectbox("Pendamping", 
                ['Ibu Sita', 'Pak Budi', 'Ibu Dewi', 'Pak Ahmad'])
        
        with col2:
            pilih_periode = st.selectbox("Periode", ['Harian', 'Mingguan'])
        
        if st.button("➕ Buat Laporan Baru"):
            st.session_state.show_laporan_form = True
        
        st.write("---")
        
        # Dummy laporan
        laporan = pd.DataFrame({
            'Tanggal': ['18 Feb 2025', '18 Feb 2025', '17 Feb 2025', '17 Feb 2025'],
            'Pendamping': ['Ibu Sita', 'Pak Budi', 'Ibu Dewi', 'Pak Ahmad'],
            'Mahasiswa Bimbing': ['5', '4', '6', '5'],
            'File': ['laporan_sita_18feb.pdf', 'laporan_budi_18feb.pdf', 'laporan_dewi_17feb.pdf', 'laporan_ahmad_17feb.pdf'],
            'Status': ['✅ Diterima', '✅ Diterima', '⏳ Pending', '✅ Diterima']
        })
        
        st.dataframe(laporan, use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("Laporan Bulanan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            pilih_bulan = st.selectbox("Pilih Bulan/Tahun", 
                ['Februari 2025', 'Januari 2025', 'Desember 2024'])
        
        with col2:
            if st.button("📥 Export Laporan Bulanan"):
                st.success("✅ Laporan bulanan berhasil didownload!")
        
        st.write("---")
        
        # Ringkasan bulanan
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("👨‍🎓 Mahasiswa Dibimbing", 20, "+3 dari bulan lalu")
        
        with col2:
            st.metric("✅ Pertemuan Berhasil", 52, "+8 dari bulan lalu")
        
        with col3:
            st.metric("📋 Laporan Terkirim", 20, "100% On Time")
    
    with tab3:
        st.subheader("Analitik & Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Efektivitas Pendampingan**")
            effectiveness = pd.DataFrame({
                'Pendamping': ['Ibu Sita', 'Pak Budi', 'Ibu Dewi'],
                'Skor Efektivitas': [95, 88, 92],
                'Mahasiswa Terlatih': [18, 16, 20]
            })
            st.dataframe(effectiveness, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("**Kompetensi Mahasiswa**")
            kompetensi = pd.DataFrame({
                'Kompetensi': ['Leadership', 'Technical', 'Communication', 'Problem Solving'],
                'Meningkat': ['85%', '78%', '92%', '81%']
            })
            st.dataframe(kompetensi, use_container_width=True, hide_index=True)

# ================== PENGATURAN ==================
elif menu == "⚙️ Pengaturan":
    st.title("⚙️ Pengaturan Sistem")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "⏰ Jam Presensi",
        "🎯 Struktur Unit",
        "👥 Role & Permission",
        "🔔 Notifikasi"
    ])
    
    with tab1:
        st.subheader("Pengaturan Jam Presensi")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Jam Presensi Masuk**")
            jam_masuk = st.time_input("Jam Masuk", value=datetime.strptime("08:00", "%H:%M").time())
        
        with col2:
            st.write("**Jam Presensi Pulang**")
            jam_pulang = st.time_input("Jam Pulang", value=datetime.strptime("17:00", "%H:%M").time())
        
        if st.button("💾 Simpan Pengaturan Jam"):
            st.success("✅ Pengaturan jam berhasil disimpan!")
    
    with tab2:
        st.subheader("Struktur Kelas/Unit Pembelajaran")
        
        if st.button("➕ Tambah Unit"):
            st.session_state.show_unit_form = True
        
        st.write("---")
        
        # Dummy unit
        units = pd.DataFrame({
            'Unit': ['Unit 1', 'Unit 2', 'Unit 3', 'Unit 4'],
            'Nama': ['Manajemen Puncak', 'Teknis Lapangan', 'Marketing & Sales', 'Finance & Accounting'],
            'Jumlah Mahasiswa': [8, 12, 7, 6],
            'PJ': ['Pak Budi', 'Ibu Sita', 'Ibu Dewi', 'Pak Ahmad']
        })
        
        st.dataframe(units, use_container_width=True, hide_index=True)
    
    with tab3:
        st.subheader("Role & Permission")
        
        col1, col2 = st.columns(2)
        
        with col1:
            role_selected = st.selectbox("Pilih Role", 
                ['Admin', 'Pendamping', 'Mitra Kerja', 'Viewer'])
        
        st.write("---")
        
        # Permission checklist
        st.write(f"**Permission untuk: {role_selected}**")
        
        perms = {
            'Admin': ['View Dashboard', 'Manage Users', 'Manage Data', 'View Reports', 'Export Data', 'System Settings'],
            'Pendamping': ['View Dashboard', 'Input Presensi', 'Upload Materi', 'Upload Laporan', 'View Reports'],
            'Mitra Kerja': ['View Dashboard', 'View Mahasiswa', 'View Presensi', 'Give Feedback'],
            'Viewer': ['View Dashboard', 'View Reports']
        }
        
        for perm in perms.get(role_selected, []):
            st.checkbox(perm, value=True)
        
        if st.button("💾 Simpan Permission"):
            st.success("✅ Permission berhasil diperbarui!")
    
    with tab4:
        st.subheader("Sistem Notifikasi")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Email Notifications**")
            st.checkbox("Laporan Baru", value=True)
            st.checkbox("Presensi Terlambat", value=True)
            st.checkbox("User Baru Registrasi", value=False)
        
        with col2:
            st.write("**WhatsApp Notifications**")
            st.checkbox("Alert Presensi", value=True)
            st.checkbox("Reminder Laporan", value=True)
            st.checkbox("System Updates", value=False)
        
        if st.button("💾 Simpan Notifikasi"):
            st.success("✅ Pengaturan notifikasi berhasil disimpan!")

# ================== LOGOUT ==================
elif menu == "🚪 Logout":
    logout()
