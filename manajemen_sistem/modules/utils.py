import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import sqlite3

def get_connection():
    """Dapatkan koneksi database"""
    conn = sqlite3.connect("data/bintrebusih.db")
    conn.row_factory = sqlite3.Row
    return conn

def get_dashboard_stats():
    """Dapatkan statistik dashboard utama"""
    conn = get_connection()
    cursor = conn.cursor()
    
    stats = {}
    
    # Total mahasiswa aktif
    cursor.execute("SELECT COUNT(*) as count FROM mahasiswa WHERE status='aktif'")
    stats['mahasiswa_aktif'] = cursor.fetchone()['count'] or 0
    
    # Total pendamping
    cursor.execute("SELECT COUNT(*) as count FROM pendamping")
    stats['total_pendamping'] = cursor.fetchone()['count'] or 0
    
    # Total mitra kerja
    cursor.execute("SELECT COUNT(*) as count FROM mitra_kerja")
    stats['total_mitra'] = cursor.fetchone()['count'] or 0
    
    # Presensi hari ini
    hari_ini = datetime.now().date()
    cursor.execute("SELECT COUNT(*) as count FROM presensi_mahasiswa WHERE tanggal=? AND status='hadir'", (hari_ini,))
    stats['presensi_hari_ini'] = cursor.fetchone()['count'] or 0
    
    # Laporan baru hari ini
    cursor.execute("SELECT COUNT(*) as count FROM laporan_pendamping WHERE DATE(created_at)=?", (hari_ini,))
    stats['laporan_baru'] = cursor.fetchone()['count'] or 0
    
    conn.close()
    return stats

def get_presensi_data():
    """Dapatkan data presensi mahasiswa"""
    conn = get_connection()
    
    query = """
    SELECT 
        m.nama, 
        m.nim, 
        p.nama as pendamping,
        mk.nama_organisasi as mitra,
        COUNT(*) as total_kehadiran,
        SUM(CASE WHEN pm.status='hadir' THEN 1 ELSE 0 END) as hadir,
        SUM(CASE WHEN pm.status='izin' THEN 1 ELSE 0 END) as izin,
        SUM(CASE WHEN pm.status='tidak_hadir' THEN 1 ELSE 0 END) as tidak_hadir
    FROM mahasiswa m
    LEFT JOIN pendamping p ON m.pendamping_id = p.id
    LEFT JOIN mitra_kerja mk ON m.mitra_id = mk.id
    LEFT JOIN presensi_mahasiswa pm ON m.id = pm.mahasiswa_id
    GROUP BY m.id
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def sidebar_menu():
    """Sidebar navigasi utama"""
    with st.sidebar:
        st.title("🎓 Bintrebusih")
        st.write(f"Logged in as: **{st.session_state.get('username', 'Unknown')}**")
        st.write(f"Role: **{st.session_state.get('role', 'Unknown')}**")
        st.divider()
        
        role = st.session_state.get('role', 'Unknown')
        
        # Menu dinamis berdasarkan role
        if role == "Admin":
            menu_options = [
                "📊 Dashboard",
                "👥 Manajemen Data",
                "� Presensi",
                "📚 Pendampingan",
                "📋 Laporan",
                "📢 Pengumuman",
                "⚙️ Pengaturan",
                "🚪 Logout"
            ]
        elif role == "Pendamping":
            menu_options = [
                "📊 Dashboard",
                "📥 Upload Materi",
                "📤 Upload Laporan",
                "📢 Pengumuman",
                "⚙️ Pengaturan",
                "🚪 Logout"
            ]
        elif role == "Mahasiswa":
            menu_options = [
                "📊 Dashboard",
                "📤 Upload Tugas",
                "📭 Tugas Saya",
                "📚 Materi Pembelajaran",
                "📢 Pengumuman",
                "🚪 Logout"
            ]
        else:  # Mitra Kerja
            menu_options = [
                "📊 Dashboard",
                "📋 Daftar Mahasiswa",
                "📢 Pengumuman",
                "🚪 Logout"
            ]
        
        menu = st.radio(
            "📋 Menu Utama",
            menu_options
        )
        
        return menu

def format_currency(value):
    """Format angka ke format currency"""
    return f"Rp {value:,.0f}"

def get_last_7_days_attendance():
    """Dapatkan data kehadiran 7 hari terakhir"""
    conn = get_connection()
    
    # Generate 7 hari terakhir
    dates = [datetime.now().date() - timedelta(days=i) for i in range(7)]
    dates.reverse()
    
    query = """
    SELECT 
        tanggal,
        COUNT(*) as total,
        SUM(CASE WHEN status='hadir' THEN 1 ELSE 0 END) as hadir
    FROM presensi_mahasiswa
    WHERE tanggal IN ({})
    GROUP BY tanggal
    """.format(','.join(['?' for _ in dates]))
    
    df = pd.read_sql_query(query, conn, params=dates)
    conn.close()
    
    return df

def get_announcements():
    """Dapatkan semua pengumuman"""
    conn = get_connection()
    
    query = """
    SELECT id, judul, isi, dibuat_oleh, created_at 
    FROM pengumuman 
    ORDER BY created_at DESC 
    LIMIT 10
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def add_announcement(judul, isi):
    """Tambah pengumuman baru"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO pengumuman (judul, isi, dibuat_oleh, created_at)
            VALUES (?, ?, ?, ?)
        """, (judul, isi, st.session_state.get('username'), datetime.now()))
        
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error: {e}")
        return False
    finally:
        conn.close()

def get_mahasiswa_tasks(mahasiswa_id):
    """Dapatkan daftar tugas mahasiswa"""
    conn = get_connection()
    
    query = """
    SELECT id, judul, diperintahkan_oleh, deadline, status, created_at
    FROM tugas_mahasiswa
    WHERE mahasiswa_id = ?
    ORDER BY created_at DESC
    """
    
    df = pd.read_sql_query(query, conn, params=(mahasiswa_id,))
    conn.close()
    return df

def get_pendamping_materials():
    """Dapatkan materi yang di-upload pendamping"""
    conn = get_connection()
    
    query = """
    SELECT id, judul, file_path, uploaded_by, created_at
    FROM materi_pembelajaran
    ORDER BY created_at DESC
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_student_info(username):
    """Dapatkan informasi mahasiswa berdasarkan username"""
    conn = get_connection()
    
    query = """
    SELECT id, nim, nama, email, pendamping_id, mitra_id, status
    FROM mahasiswa
    ORDER BY nama
    LIMIT 1
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.iloc[0] if len(df) > 0 else None
