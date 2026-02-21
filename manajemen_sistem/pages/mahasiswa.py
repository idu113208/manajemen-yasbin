"""
Halaman CRUD Mahasiswa
"""
import streamlit as st
import pandas as pd
from modules.crud import (
    read_all_mahasiswa, 
    read_mahasiswa_by_id,
    create_mahasiswa,
    update_mahasiswa,
    delete_mahasiswa,
    get_pendamping_list,
    get_mitra_list
)
from modules.auth import check_login
from modules.navbar import horizontal_navbar

# Check login
check_login()

# Navigation Bar
horizontal_navbar()

st.title("👨‍🎓 Manajemen Mahasiswa")

# Tab untuk Create dan View
tab1, tab2 = st.tabs(["📋 Data Mahasiswa", "➕ Tambah Mahasiswa"])

# ==================== TAB 2: TAMBAH MAHASISWA ====================
with tab2:
    st.subheader("Tambah Mahasiswa Baru")
    
    col1, col2 = st.columns(2)
    
    with col1:
        nama = st.text_input("Nama Lengkap *")
        nim = st.text_input("NIM *")
        email = st.text_input("Email")
        no_hp = st.text_input("No. HP")
    
    with col2:
        asal_provinsi = st.text_input("Asal Provinsi")
        unit = st.text_input("Unit")
        
        pendamping_list = get_pendamping_list()
        pendamping_names = ["-- Pilih Pendamping --"] + [p['nama'] for p in pendamping_list]
        pendamping_ids = [None] + [p['id'] for p in pendamping_list]
        selected_pendamping = st.selectbox("Pendamping", options=pendamping_names)
        pendamping_id = pendamping_ids[pendamping_names.index(selected_pendamping)]
        
        mitra_list = get_mitra_list()
        mitra_names = ["-- Pilih Mitra Kerja --"] + [m['nama_organisasi'] for m in mitra_list]
        mitra_ids = [None] + [m['id'] for m in mitra_list]
        selected_mitra = st.selectbox("Mitra Kerja", options=mitra_names)
        mitra_id = mitra_ids[mitra_names.index(selected_mitra)]
    
    if st.button("💾 Simpan Mahasiswa", type="primary", use_container_width=True):
        if not nama or not nim:
            st.error("Nama dan NIM tidak boleh kosong!")
        else:
            result = create_mahasiswa(
                nama=nama,
                nim=nim,
                email=email if email else None,
                no_hp=no_hp if no_hp else None,
                asal_provinsi=asal_provinsi if asal_provinsi else None,
                unit=unit if unit else None,
                pendamping_id=pendamping_id,
                mitra_id=mitra_id
            )
            
            if result['success']:
                st.success(result['message'])
                st.rerun()
            else:
                st.error(result['message'])

# ==================== TAB 1: DATA MAHASISWA ====================
with tab1:
    st.subheader("Data Mahasiswa Terdaftar")
    
    # Refresh button
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()
    
    # Get data
    mahasiswas = read_all_mahasiswa()
    
    if not mahasiswas:
        st.info("Belum ada data mahasiswa")
    else:
        # Display as table
        df = pd.DataFrame(mahasiswas)
        df = df[['id', 'nama', 'nim', 'email', 'no_hp', 'unit', 'status']]
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Management section
        st.divider()
        st.subheader("⚙️ Kelola Mahasiswa")
        
        col1, col2 = st.columns(2)
        
        with col1:
            selected_nim = st.selectbox(
                "Pilih Mahasiswa (NIM)",
                options=[m['nim'] for m in mahasiswas],
                format_func=lambda x: [m['nama'] + ' (' + m['nim'] + ')' for m in mahasiswas if m['nim'] == x][0]
            )
            selected_mhs = [m for m in mahasiswas if m['nim'] == selected_nim][0]
        
        with col2:
            action = st.radio("Pilih Aksi", ["👁️ Lihat Detail", "✏️ Edit", "🗑️ Hapus"], horizontal=True)
        
        # ===== VIEW DETAIL =====
        if action == "👁️ Lihat Detail":
            st.info("Detail Mahasiswa")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Nama:** {selected_mhs['nama']}")
                st.write(f"**NIM:** {selected_mhs['nim']}")
                st.write(f"**Email:** {selected_mhs['email']}")
                st.write(f"**No. HP:** {selected_mhs['no_hp']}")
            with col2:
                st.write(f"**Asal Provinsi:** {selected_mhs['asal_provinsi']}")
                st.write(f"**Unit:** {selected_mhs['unit']}")
                st.write(f"**Status:** {selected_mhs['status']}")
                st.write(f"**Pendamping:** {selected_mhs.get('pendamping_nama', '-')}")
                st.write(f"**Mitra Kerja:** {selected_mhs.get('mitra_nama', '-')}")
        
        # ===== EDIT =====
        elif action == "✏️ Edit":
            st.warning("Edit Data Mahasiswa")
            
            col1, col2 = st.columns(2)
            
            with col1:
                nama_edit = st.text_input("Nama Lengkap", value=selected_mhs['nama'])
                email_edit = st.text_input("Email", value=selected_mhs['email'] or "")
                no_hp_edit = st.text_input("No. HP", value=selected_mhs['no_hp'] or "")
            
            with col2:
                asal_provinsi_edit = st.text_input("Asal Provinsi", value=selected_mhs['asal_provinsi'] or "")
                unit_edit = st.text_input("Unit", value=selected_mhs['unit'] or "")
                status_edit = st.selectbox("Status", ["aktif", "nonaktif", "cuti"], index=0 if selected_mhs['status'] == "aktif" else 1)
            
            if st.button("💾 Simpan Perubahan", type="primary", use_container_width=True):
                result = update_mahasiswa(
                    selected_mhs['id'],
                    nama=nama_edit,
                    email=email_edit if email_edit else None,
                    no_hp=no_hp_edit if no_hp_edit else None,
                    asal_provinsi=asal_provinsi_edit if asal_provinsi_edit else None,
                    unit=unit_edit if unit_edit else None,
                    status=status_edit
                )
                
                if result['success']:
                    st.success(result['message'])
                    st.rerun()
                else:
                    st.error(result['message'])
        
        # ===== DELETE =====
        elif action == "🗑️ Hapus":
            st.danger(f"⚠️ Anda akan menghapus: **{selected_mhs['nama']}**")
            st.warning("Tindakan ini tidak dapat dibatalkan!")
            
            if st.button("🗑️ Ya, Hapus Mahasiswa Ini", type="primary", use_container_width=True):
                result = delete_mahasiswa(selected_mhs['id'])
                if result['success']:
                    st.success(result['message'])
                    st.rerun()
                else:
                    st.error(result['message'])
