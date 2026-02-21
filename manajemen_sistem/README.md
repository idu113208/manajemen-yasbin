# Dashboard Bintrebusih - Sistem Manajemen Pendampingan Mahasiswa Papua

## 📋 Deskripsi Proyek

Dashboard Admin untuk **Yayasan Bintrebusih** - Sistem manajemen pendampingan mahasiswa Papua di berbagai mitra kerja.

Sistem ini dirancang untuk mendukung:
- ✅ Pendampingan mahasiswa di mitra kerja
- ✅ Manajemen presensi (mahasiswa & pendamping)
- ✅ Upload materi pembelajaran dan laporan
- ✅ Analitik dan reportase pendampingan
- ✅ Kelola data stakeholder (mahasiswa, pendamping, mitra)

---

## 🚀 Fitur Utama

### 1. **Dashboard** 📊
- Statistik real-time (mahasiswa aktif, pendamping, mitra kerja)
- Grafik tren kehadiran & distribusi mahasiswa
- Alert mahasiswa yang belum presensi
- Reminder laporan tertunda

### 2. **Manajemen Data** 👥
- CRUD Mahasiswa (biodata, kontrak, unit, mitra)
- CRUD Pendamping (profil, area pendampingan)
- CRUD Mitra Kerja (organisasi, PJ, kontak, SOP)
- Manajemen User & Role Sistem

### 3. **Presensi** 📝
- Input presensi mahasiswa harian
- Input presensi pendamping
- Rekap presensi dengan filter & export PDF/Excel
- Grafik kehadiran per mitra & unit

### 4. **Pendampingan** 📚
- Upload materi pembelajaran (PDF, PPT, video)
- Manajemen jadwal pendampingan
- Catatan perkembangan per mahasiswa

### 5. **Laporan** 📋
- Laporan harian/mingguan pendamping
- Laporan bulanan & evaluasi
- Analitik efektivitas pendampingan
- Export laporan PDF/Excel

### 6. **Pengaturan** ⚙️
- Konfigurasi jam presensi
- Manajemen struktur unit/kelas
- Role & permission management
- Sistem notifikasi (email/WhatsApp)

---

## 📁 Struktur Folder

```
Dashboard_Bintrebusih/
├── app.py                 # Main Streamlit application
├── database.py            # Database setup & initialization
├── requirements.txt       # Python dependencies
├── README.md             # This file
│
├── data/
│   └── bintrebusih.db    # SQLite database (auto-created)
│
├── modules/
│   ├── __init__.py
│   ├── auth.py           # Authentication & login
│   └── utils.py          # Utility functions
│
└── pages/               # Future: Individual page modules

```

---

## 📦 Instalasi & Setup

### 1. **Clone/Download Project**
```bash
cd C:\Users\yohan\Downloads\Dashboard_Bintrebusih
```

### 2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 3. **Inisialisasi Database**
```bash
python database.py
```

### 4. **Jalankan Aplikasi**
```bash
streamlit run app.py
```

Aplikasi akan membuka di browser: `http://localhost:8501`

---

## 🔐 Demo Login

Untuk testing, gunakan akun berikut:

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Admin |
| pendamping1 | pass123 | Pendamping |
| mitra1 | pass123 | Mitra Kerja |

---

## 🗄️ Database Schema

### Tabel Utama:
- **users** - User sistem & authentication
- **mahasiswa** - Data mahasiswa yang didampingi
- **pendamping** - Data pembimbing/mentor
- **mitra_kerja** - Data organisasi/perusahaan mitra
- **presensi_mahasiswa** - Log kehadiran mahasiswa
- **presensi_pendamping** - Log kehadiran pendamping
- **laporan_pendamping** - Laporan dari pendamping
- **materi** - File materi pembelajaran
- **jadwal_pendampingan** - Schedule pendampingan

---

## 🎯 Alur Kerja Pendamping

1. **Login** → Masuk dengan username & password
2. **Cek Dashboard** → Lihat overview & jadwal hari ini
3. **Input Presensi** → Catat kehadiran mahasiswa
4. **Upload Materi** → Share materi pembelajaran (jika ada)
5. **Upload Laporan** → Isi laporan harian/mingguan
6. **Lihat Analitik** → Review progress mahasiswa
7. **Logout** → Keluar sistem

---

## 🔄 Development Roadmap

- [x] Database schema & setup
- [x] Authentication & login page
- [x] Dashboard main page
- [x] Data management (CRUD)
- [x] Presensi management
- [x] Pendampingan features
- [x] Laporan & reporting
- [ ] Export PDF/Excel (integrasi reportlab, openpyxl)
- [ ] Email/WhatsApp notifikasi (integrasi Twilio/SendGrid)
- [ ] File upload storage (cloud: AWS S3/Google Drive)
- [ ] Mobile responsive optimization
- [ ] Real-time notifications
- [ ] API endpoints (untuk integrasi eksternal)

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit 1.28.1
- **Backend**: Python 3.8+
- **Database**: SQLite3
- **Charting**: Plotly Express
- **Data Processing**: Pandas, NumPy
- **Export**: openpyxl (Excel), python-pptx (PowerPoint)

---

## 📞 Support & Kontribusi

Untuk issues, suggestions, atau kontribusi:
- Email: support@bintrebusih.or.id
- Dokumentasi: [Bintrebusih Wiki](https://wiki.bintrebusih.or.id)

---

## 📄 Lisensi

© 2025 Yayasan Bintrebusih. All rights reserved.

---

**Happy Coding! 🚀**

Last Updated: February 19, 2025
