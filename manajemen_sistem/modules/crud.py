"""
Module untuk operasi CRUD Database
Menyediakan fungsi-fungsi umum untuk Create, Read, Update, Delete
"""

import sqlite3
from datetime import datetime
from database import get_connection

# ==================== MAHASISWA CRUD ====================

def create_mahasiswa(nama, nim, email, no_hp, asal_provinsi, unit, pendamping_id=None, mitra_id=None):
    """Create mahasiswa baru"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO mahasiswa (nama, nim, email, no_hp, asal_provinsi, unit, pendamping_id, mitra_id, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'aktif')
        ''', (nama, nim, email, no_hp, asal_provinsi, unit, pendamping_id, mitra_id))
        
        conn.commit()
        return {"success": True, "message": "Mahasiswa berhasil ditambahkan"}
    except sqlite3.IntegrityError as e:
        return {"success": False, "message": f"Error: {str(e)}"}
    finally:
        conn.close()

def read_all_mahasiswa():
    """Read semua mahasiswa"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT m.*, p.nama as pendamping_nama, mk.nama_organisasi as mitra_nama 
        FROM mahasiswa m
        LEFT JOIN pendamping p ON m.pendamping_id = p.id
        LEFT JOIN mitra_kerja mk ON m.mitra_id = mk.id
        ORDER BY m.created_at DESC
    ''')
    
    data = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return data

def read_mahasiswa_by_id(mahasiswa_id):
    """Read mahasiswa berdasarkan ID"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT m.*, p.nama as pendamping_nama, mk.nama_organisasi as mitra_nama 
        FROM mahasiswa m
        LEFT JOIN pendamping p ON m.pendamping_id = p.id
        LEFT JOIN mitra_kerja mk ON m.mitra_id = mk.id
        WHERE m.id = ?
    ''', (mahasiswa_id,))
    
    data = dict(cursor.fetchone() or {})
    conn.close()
    return data

def update_mahasiswa(mahasiswa_id, **kwargs):
    """Update data mahasiswa"""
    conn = get_connection()
    cursor = conn.cursor()
    
    allowed_fields = ['nama', 'email', 'no_hp', 'asal_provinsi', 'unit', 'pendamping_id', 'mitra_id', 'status']
    update_fields = {k: v for k, v in kwargs.items() if k in allowed_fields}
    
    if not update_fields:
        return {"success": False, "message": "Tidak ada field yang diupdate"}
    
    set_clause = ', '.join([f"{k} = ?" for k in update_fields.keys()])
    values = list(update_fields.values()) + [mahasiswa_id]
    
    try:
        cursor.execute(f'UPDATE mahasiswa SET {set_clause} WHERE id = ?', values)
        conn.commit()
        return {"success": True, "message": "Mahasiswa berhasil diupdate"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
    finally:
        conn.close()

def delete_mahasiswa(mahasiswa_id):
    """Delete mahasiswa"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('DELETE FROM mahasiswa WHERE id = ?', (mahasiswa_id,))
        conn.commit()
        return {"success": True, "message": "Mahasiswa berhasil dihapus"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
    finally:
        conn.close()

# ==================== PENDAMPING CRUD ====================

def create_pendamping(nama, nip=None, email=None, no_hp=None, alamat=None, user_id=None):
    """Create pendamping baru"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO pendamping (nama, nip, email, no_hp, alamat, user_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nama, nip, email, no_hp, alamat, user_id))
        
        conn.commit()
        return {"success": True, "message": "Pendamping berhasil ditambahkan"}
    except sqlite3.IntegrityError as e:
        return {"success": False, "message": f"Error: {str(e)}"}
    finally:
        conn.close()

def read_all_pendamping():
    """Read semua pendamping"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT p.*, COUNT(m.id) as total_mahasiswa
        FROM pendamping p
        LEFT JOIN mahasiswa m ON p.id = m.pendamping_id
        GROUP BY p.id
        ORDER BY p.created_at DESC
    ''')
    
    data = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return data

def read_pendamping_by_id(pendamping_id):
    """Read pendamping berdasarkan ID"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM pendamping WHERE id = ?', (pendamping_id,))
    data = dict(cursor.fetchone() or {})
    conn.close()
    return data

def update_pendamping(pendamping_id, **kwargs):
    """Update data pendamping"""
    conn = get_connection()
    cursor = conn.cursor()
    
    allowed_fields = ['nama', 'nip', 'email', 'no_hp', 'alamat']
    update_fields = {k: v for k, v in kwargs.items() if k in allowed_fields}
    
    if not update_fields:
        return {"success": False, "message": "Tidak ada field yang diupdate"}
    
    set_clause = ', '.join([f"{k} = ?" for k in update_fields.keys()])
    values = list(update_fields.values()) + [pendamping_id]
    
    try:
        cursor.execute(f'UPDATE pendamping SET {set_clause} WHERE id = ?', values)
        conn.commit()
        return {"success": True, "message": "Pendamping berhasil diupdate"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
    finally:
        conn.close()

def delete_pendamping(pendamping_id):
    """Delete pendamping"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('DELETE FROM pendamping WHERE id = ?', (pendamping_id,))
        conn.commit()
        return {"success": True, "message": "Pendamping berhasil dihapus"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
    finally:
        conn.close()

# ==================== MITRA KERJA CRUD ====================

def create_mitra_kerja(nama_organisasi, lokasi=None, penanggung_jawab=None, kontak_email=None, kontak_hp=None, perjanjian_kerjasama=None):
    """Create mitra kerja baru"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO mitra_kerja (nama_organisasi, lokasi, penanggung_jawab, kontak_email, kontak_hp, perjanjian_kerjasama)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nama_organisasi, lokasi, penanggung_jawab, kontak_email, kontak_hp, perjanjian_kerjasama))
        
        conn.commit()
        return {"success": True, "message": "Mitra Kerja berhasil ditambahkan"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
    finally:
        conn.close()

def read_all_mitra_kerja():
    """Read semua mitra kerja"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT mk.*, COUNT(m.id) as total_mahasiswa
        FROM mitra_kerja mk
        LEFT JOIN mahasiswa m ON mk.id = m.mitra_id
        GROUP BY mk.id
        ORDER BY mk.created_at DESC
    ''')
    
    data = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return data

def read_mitra_kerja_by_id(mitra_id):
    """Read mitra kerja berdasarkan ID"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM mitra_kerja WHERE id = ?', (mitra_id,))
    data = dict(cursor.fetchone() or {})
    conn.close()
    return data

def update_mitra_kerja(mitra_id, **kwargs):
    """Update data mitra kerja"""
    conn = get_connection()
    cursor = conn.cursor()
    
    allowed_fields = ['nama_organisasi', 'lokasi', 'penanggung_jawab', 'kontak_email', 'kontak_hp', 'perjanjian_kerjasama']
    update_fields = {k: v for k, v in kwargs.items() if k in allowed_fields}
    
    if not update_fields:
        return {"success": False, "message": "Tidak ada field yang diupdate"}
    
    set_clause = ', '.join([f"{k} = ?" for k in update_fields.keys()])
    values = list(update_fields.values()) + [mitra_id]
    
    try:
        cursor.execute(f'UPDATE mitra_kerja SET {set_clause} WHERE id = ?', values)
        conn.commit()
        return {"success": True, "message": "Mitra Kerja berhasil diupdate"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
    finally:
        conn.close()

def delete_mitra_kerja(mitra_id):
    """Delete mitra kerja"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('DELETE FROM mitra_kerja WHERE id = ?', (mitra_id,))
        conn.commit()
        return {"success": True, "message": "Mitra Kerja berhasil dihapus"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
    finally:
        conn.close()

# ==================== PRESENSI CRUD ====================

def create_presensi_mahasiswa(mahasiswa_id, tanggal, status='hadir', keterangan=None):
    """Create presensi mahasiswa baru"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO presensi_mahasiswa (mahasiswa_id, tanggal, status, keterangan)
            VALUES (?, ?, ?, ?)
        ''', (mahasiswa_id, tanggal, status, keterangan))
        
        conn.commit()
        return {"success": True, "message": "Presensi berhasil ditambahkan"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
    finally:
        conn.close()

def read_presensi_by_mahasiswa(mahasiswa_id, limit=30):
    """Read presensi mahasiswa"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM presensi_mahasiswa 
        WHERE mahasiswa_id = ?
        ORDER BY tanggal DESC
        LIMIT ?
    ''', (mahasiswa_id, limit))
    
    data = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return data

def update_presensi_mahasiswa(presensi_id, status=None, keterangan=None):
    """Update presensi mahasiswa"""
    conn = get_connection()
    cursor = conn.cursor()
    
    update_fields = {}
    if status:
        update_fields['status'] = status
    if keterangan:
        update_fields['keterangan'] = keterangan
    
    if not update_fields:
        return {"success": False, "message": "Tidak ada field yang diupdate"}
    
    set_clause = ', '.join([f"{k} = ?" for k in update_fields.keys()])
    values = list(update_fields.values()) + [presensi_id]
    
    try:
        cursor.execute(f'UPDATE presensi_mahasiswa SET {set_clause} WHERE id = ?', values)
        conn.commit()
        return {"success": True, "message": "Presensi berhasil diupdate"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
    finally:
        conn.close()

def delete_presensi_mahasiswa(presensi_id):
    """Delete presensi mahasiswa"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('DELETE FROM presensi_mahasiswa WHERE id = ?', (presensi_id,))
        conn.commit()
        return {"success": True, "message": "Presensi berhasil dihapus"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
    finally:
        conn.close()

# ==================== HELPER FUNCTIONS ====================

def get_pendamping_list():
    """Dapatkan list pendamping untuk dropdown"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nama FROM pendamping ORDER BY nama')
    data = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return data

def get_mitra_list():
    """Dapatkan list mitra kerja untuk dropdown"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nama_organisasi FROM mitra_kerja ORDER BY nama_organisasi')
    data = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return data
