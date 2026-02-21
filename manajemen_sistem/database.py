import sqlite3
import os
from datetime import datetime

DB_PATH = "data/bintrebusih.db"

def init_database():
    """Inisialisasi database dengan tabel-tabel utama"""
    os.makedirs("data", exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Tabel Users (Admin, Pendamping, Mitra, Viewer)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT NOT NULL,
            nama_lengkap TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabel Pendamping
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pendamping (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            nip TEXT UNIQUE,
            email TEXT,
            no_hp TEXT,
            alamat TEXT,
            user_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    
    # Tabel Mahasiswa
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mahasiswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            nim TEXT UNIQUE NOT NULL,
            email TEXT,
            no_hp TEXT,
            asal_provinsi TEXT,
            unit TEXT,
            status TEXT DEFAULT 'aktif',
            pendamping_id INTEGER,
            mitra_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(pendamping_id) REFERENCES pendamping(id),
            FOREIGN KEY(mitra_id) REFERENCES mitra_kerja(id)
        )
    ''')
    
    # Tabel Mitra Kerja
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mitra_kerja (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_organisasi TEXT NOT NULL,
            lokasi TEXT,
            penanggung_jawab TEXT,
            kontak_email TEXT,
            kontak_hp TEXT,
            perjanjian_kerjasama TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabel Presensi Mahasiswa
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS presensi_mahasiswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mahasiswa_id INTEGER NOT NULL,
            tanggal DATE NOT NULL,
            status TEXT DEFAULT 'hadir',
            keterangan TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(mahasiswa_id) REFERENCES mahasiswa(id)
        )
    ''')
    
    # Tabel Presensi Pendamping
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS presensi_pendamping (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pendamping_id INTEGER NOT NULL,
            tanggal DATE NOT NULL,
            status TEXT DEFAULT 'hadir',
            lokasi TEXT,
            aktivitas TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(pendamping_id) REFERENCES pendamping(id)
        )
    ''')
    
    # Tabel Laporan Pendamping
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS laporan_pendamping (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pendamping_id INTEGER NOT NULL,
            jenis_laporan TEXT,
            judul TEXT,
            isi TEXT,
            file_path TEXT,
            tanggal_laporan DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(pendamping_id) REFERENCES pendamping(id)
        )
    ''')
    
    # Tabel Materi Pendampingan
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS materi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pendamping_id INTEGER NOT NULL,
            mahasiswa_id INTEGER,
            mitra_id INTEGER,
            judul TEXT NOT NULL,
            file_path TEXT,
            deskripsi TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(pendamping_id) REFERENCES pendamping(id),
            FOREIGN KEY(mahasiswa_id) REFERENCES mahasiswa(id),
            FOREIGN KEY(mitra_id) REFERENCES mitra_kerja(id)
        )
    ''')
    
    # Tabel Jadwal Pendampingan
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jadwal_pendampingan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pendamping_id INTEGER NOT NULL,
            mahasiswa_id INTEGER,
            mitra_id INTEGER,
            tanggal DATE NOT NULL,
            jam_mulai TIME,
            jam_selesai TIME,
            lokasi TEXT,
            topik TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(pendamping_id) REFERENCES pendamping(id),
            FOREIGN KEY(mahasiswa_id) REFERENCES mahasiswa(id),
            FOREIGN KEY(mitra_id) REFERENCES mitra_kerja(id)
        )
    ''')
    
    # Tabel Pengumuman (untuk Admin, Pendamping, Mahasiswa)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pengumuman (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            judul TEXT NOT NULL,
            isi TEXT NOT NULL,
            dibuat_oleh TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabel Tugas Mahasiswa
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tugas_mahasiswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mahasiswa_id INTEGER NOT NULL,
            judul TEXT NOT NULL,
            deskripsi TEXT,
            deadline DATE,
            diperintahkan_oleh TEXT,
            status TEXT DEFAULT 'belum_dikumpulkan',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(mahasiswa_id) REFERENCES mahasiswa(id)
        )
    ''')
    
    # Tabel Pengumpulan Tugas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pengumpulan_tugas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tugas_id INTEGER NOT NULL,
            mahasiswa_id INTEGER NOT NULL,
            file_path TEXT,
            catatan TEXT,
            dikumpulkan_pada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'diterima',
            FOREIGN KEY(tugas_id) REFERENCES tugas_mahasiswa(id),
            FOREIGN KEY(mahasiswa_id) REFERENCES mahasiswa(id)
        )
    ''')
    
    # Tabel Materi Pembelajaran
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS materi_pembelajaran (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            judul TEXT NOT NULL,
            deskripsi TEXT,
            file_path TEXT,
            uploaded_by TEXT NOT NULL,
            kategori TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database berhasil diinisialisasi!")

def get_connection():
    """Dapatkan koneksi ke database"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

if __name__ == "__main__":
    init_database()
