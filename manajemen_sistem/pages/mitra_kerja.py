"""
Halaman CRUD Mitra Kerja
"""
import streamlit as st
import pandas as pd
from modules.crud import (
    read_all_mitra_kerja,
    read_mitra_kerja_by_id,
    create_mitra_kerja,
    update_mitra_kerja,
    delete_mitra_kerja
)
from modules.auth import check_login
from modules.navbar import horizontal_navbar

# Check login
check_login()

# Navigation Bar
horizontal_navbar()

st.title("🏢 Manajemen Mitra Kerja")

# Tab untuk Create dan View
tab1, tab2 = st.tabs(["📋 Data Mitra Kerja", "➕ Tambah Mitra Kerja"])

# ==================== TAB 2: TAMBAH MITRA KERJA ====================
with tab2:
    st.subheader("Tambah Mitra Kerja Baru")
    
    col1, col2 = st.columns(2)
    
    with col1:
        nama_organisasi = st.text_input("Nama Organisasi *")
        lokasi = st.text_input("Lokasi")
        penanggung_jawab = st.text_input("Penanggung Jawab")
    
    with col2:
        kontak_email = st.text_input("Email Kontak")
        kontak_hp = st.text_input("No. HP Kontak")
        perjanjian_kerjasama = st.text_input("Referensi Perjanjian Kerjasama")
    
    if st.button("💾 Simpan Mitra Kerja", type="primary", use_container_width=True):
        if not nama_organisasi:
            st.error("Nama Organisasi tidak boleh kosong!")
        else:
            result = create_mitra_kerja(
                nama_organisasi=nama_organisasi,
                lokasi=lokasi if lokasi else None,
                penanggung_jawab=penanggung_jawab if penanggung_jawab else None,
                kontak_email=kontak_email if kontak_email else None,
                kontak_hp=kontak_hp if kontak_hp else None,
                perjanjian_kerjasama=perjanjian_kerjasama if perjanjian_kerjasama else None
            )
            
            if result['success']:
                st.success(result['message'])
                st.rerun()
            else:
                st.error(result['message'])

# ==================== TAB 1: DATA MITRA KERJA ====================
with tab1:
    st.subheader("Data Mitra Kerja Terdaftar")
    
    # Refresh button
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()
    
    # Get data
    mitras = read_all_mitra_kerja()
    
    if not mitras:
        st.info("Belum ada data mitra kerja")
    else:
        # Display as table
        df = pd.DataFrame(mitras)
        df = df[['id', 'nama_organisasi', 'lokasi', 'penanggung_jawab', 'kontak_email', 'total_mahasiswa']]
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Management section
        st.divider()
        st.subheader("⚙️ Kelola Mitra Kerja")
        
        col1, col2 = st.columns(2)
        
        with col1:
            selected_nama = st.selectbox(
                "Pilih Mitra Kerja",
                options=[m['nama_organisasi'] for m in mitras]
            )
            selected_mitra = [m for m in mitras if m['nama_organisasi'] == selected_nama][0]
        
        with col2:
            action = st.radio("Pilih Aksi", ["👁️ Lihat Detail", "✏️ Edit", "🗑️ Hapus"], horizontal=True)
        
        # ===== VIEW DETAIL =====
        if action == "👁️ Lihat Detail":
            st.info("Detail Mitra Kerja")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Nama Organisasi:** {selected_mitra['nama_organisasi']}")
                st.write(f"**Lokasi:** {selected_mitra['lokasi'] or '-'}")
                st.write(f"**Penanggung Jawab:** {selected_mitra['penanggung_jawab'] or '-'}")
            with col2:
                st.write(f"**Email Kontak:** {selected_mitra['kontak_email'] or '-'}")
                st.write(f"**No. HP Kontak:** {selected_mitra['kontak_hp'] or '-'}")
                st.write(f"**Total Mahasiswa:** {selected_mitra['total_mahasiswa']}")
                st.write(f"**Perjanjian Kerjasama:** {selected_mitra.get('perjanjian_kerjasama', '-')}")
        
        # ===== EDIT =====
        elif action == "✏️ Edit":
            st.warning("Edit Data Mitra Kerja")
            
            col1, col2 = st.columns(2)
            
            with col1:
                nama_organisasi_edit = st.text_input("Nama Organisasi", value=selected_mitra['nama_organisasi'])
                lokasi_edit = st.text_input("Lokasi", value=selected_mitra['lokasi'] or "")
                penanggung_jawab_edit = st.text_input("Penanggung Jawab", value=selected_mitra['penanggung_jawab'] or "")
            
            with col2:
                kontak_email_edit = st.text_input("Email Kontak", value=selected_mitra['kontak_email'] or "")
                kontak_hp_edit = st.text_input("No. HP Kontak", value=selected_mitra['kontak_hp'] or "")
                perjanjian_kerjasama_edit = st.text_input("Referensi Perjanjian Kerjasama", value=selected_mitra.get('perjanjian_kerjasama') or "")
            
            if st.button("💾 Simpan Perubahan", type="primary", use_container_width=True):
                result = update_mitra_kerja(
                    selected_mitra['id'],
                    nama_organisasi=nama_organisasi_edit,
                    lokasi=lokasi_edit if lokasi_edit else None,
                    penanggung_jawab=penanggung_jawab_edit if penanggung_jawab_edit else None,
                    kontak_email=kontak_email_edit if kontak_email_edit else None,
                    kontak_hp=kontak_hp_edit if kontak_hp_edit else None,
                    perjanjian_kerjasama=perjanjian_kerjasama_edit if perjanjian_kerjasama_edit else None
                )
                
                if result['success']:
                    st.success(result['message'])
                    st.rerun()
                else:
                    st.error(result['message'])
        
        # ===== DELETE =====
        elif action == "🗑️ Hapus":
            st.danger(f"⚠️ Anda akan menghapus: **{selected_mitra['nama_organisasi']}**")
            st.warning("Tindakan ini tidak dapat dibatalkan!")
            
            if st.button("🗑️ Ya, Hapus Mitra Kerja Ini", type="primary", use_container_width=True):
                result = delete_mitra_kerja(selected_mitra['id'])
                if result['success']:
                    st.success(result['message'])
                    st.rerun()
                else:
                    st.error(result['message'])
