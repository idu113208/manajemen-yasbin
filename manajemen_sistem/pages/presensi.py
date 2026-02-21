"""
Halaman CRUD Presensi Mahasiswa
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from modules.crud import (
    read_all_mahasiswa,
    read_presensi_by_mahasiswa,
    create_presensi_mahasiswa,
    update_presensi_mahasiswa,
    delete_presensi_mahasiswa
)
from modules.auth import check_login
from modules.navbar import horizontal_navbar

# Check login
check_login()

# Navigation Bar
horizontal_navbar()

st.title("📍 Manajemen Presensi Mahasiswa")

# Tab untuk Create dan View
tab1, tab2 = st.tabs(["📋 Data Presensi", "➕ Tambah Presensi"])

# ==================== TAB 2: TAMBAH PRESENSI ====================
with tab2:
    st.subheader("Tambah Presensi Baru")
    
    mahasiswas = read_all_mahasiswa()
    
    if not mahasiswas:
        st.warning("Belum ada data mahasiswa. Silakan tambahkan mahasiswa terlebih dahulu.")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            mahasiswa_names = [m['nama'] + ' (' + m['nim'] + ')' for m in mahasiswas]
            selected_mahasiswa_idx = st.selectbox("Pilih Mahasiswa", range(len(mahasiswas)), format_func=lambda x: mahasiswa_names[x])
            selected_mahasiswa_id = mahasiswas[selected_mahasiswa_idx]['id']
            
            tanggal = st.date_input("Tanggal Presensi", value=datetime.now().date())
        
        with col2:
            status = st.selectbox("Status Presensi", ["hadir", "izin", "tidak hadir", "sakit"])
            keterangan = st.text_area("Keterangan")
        
        if st.button("💾 Simpan Presensi", type="primary", use_container_width=True):
            result = create_presensi_mahasiswa(
                mahasiswa_id=selected_mahasiswa_id,
                tanggal=tanggal,
                status=status,
                keterangan=keterangan if keterangan else None
            )
            
            if result['success']:
                st.success(result['message'])
                st.rerun()
            else:
                st.error(result['message'])

# ==================== TAB 1: DATA PRESENSI ====================
with tab1:
    st.subheader("Data Presensi Mahasiswa")
    
    mahasiswas = read_all_mahasiswa()
    
    if not mahasiswas:
        st.warning("Belum ada data mahasiswa")
    else:
        # Filter by mahasiswa
        mahasiswa_names = [m['nama'] + ' (' + m['nim'] + ')' for m in mahasiswas]
        selected_mahasiswa_idx = st.selectbox("Pilih Mahasiswa", range(len(mahasiswas)), format_func=lambda x: mahasiswa_names[x], key="filter_mahasiswa")
        selected_mahasiswa = mahasiswas[selected_mahasiswa_idx]
        
        # Get presensi data
        presensis = read_presensi_by_mahasiswa(selected_mahasiswa['id'], limit=100)
        
        if not presensis:
            st.info(f"Belum ada data presensi untuk {selected_mahasiswa['nama']}")
        else:
            # Display as table
            df = pd.DataFrame(presensis)
            df = df[['id', 'tanggal', 'status', 'keterangan']]
            
            # Reorder columns
            df = df.sort_values('tanggal', ascending=False)
            
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Statistics
            st.divider()
            col1, col2, col3, col4 = st.columns(4)
            
            hadir = len([p for p in presensis if p['status'] == 'hadir'])
            izin = len([p for p in presensis if p['status'] == 'izin'])
            tidak_hadir = len([p for p in presensis if p['status'] == 'tidak hadir'])
            sakit = len([p for p in presensis if p['status'] == 'sakit'])
            
            with col1:
                st.metric("✅ Hadir", hadir)
            with col2:
                st.metric("📝 Izin", izin)
            with col3:
                st.metric("❌ Tidak Hadir", tidak_hadir)
            with col4:
                st.metric("🤒 Sakit", sakit)
            
            # Management section
            st.divider()
            st.subheader("⚙️ Kelola Presensi")
            
            if presensis:
                col1, col2 = st.columns(2)
                
                with col1:
                    selected_tanggal = st.selectbox(
                        "Pilih Tanggal",
                        options=[p['tanggal'] for p in presensis],
                        format_func=lambda x: [p for p in presensis if p['tanggal'] == x][0]['tanggal'] + ' - ' + [p for p in presensis if p['tanggal'] == x][0]['status']
                    )
                    selected_presensi = [p for p in presensis if p['tanggal'] == selected_tanggal][0]
                
                with col2:
                    action = st.radio("Pilih Aksi", ["👁️ Lihat Detail", "✏️ Edit", "🗑️ Hapus"], horizontal=True)
                
                # ===== VIEW DETAIL =====
                if action == "👁️ Lihat Detail":
                    st.info("Detail Presensi")
                    st.write(f"**Tanggal:** {selected_presensi['tanggal']}")
                    st.write(f"**Status:** {selected_presensi['status']}")
                    st.write(f"**Keterangan:** {selected_presensi['keterangan'] or '-'}")
                
                # ===== EDIT =====
                elif action == "✏️ Edit":
                    st.warning("Edit Data Presensi")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        status_edit = st.selectbox("Status Presensi", ["hadir", "izin", "tidak hadir", "sakit"], index=["hadir", "izin", "tidak hadir", "sakit"].index(selected_presensi['status']))
                    
                    with col2:
                        keterangan_edit = st.text_area("Keterangan", value=selected_presensi['keterangan'] or "", height=100)
                    
                    if st.button("💾 Simpan Perubahan", type="primary", use_container_width=True):
                        result = update_presensi_mahasiswa(
                            selected_presensi['id'],
                            status=status_edit,
                            keterangan=keterangan_edit if keterangan_edit else None
                        )
                        
                        if result['success']:
                            st.success(result['message'])
                            st.rerun()
                        else:
                            st.error(result['message'])
                
                # ===== DELETE =====
                elif action == "🗑️ Hapus":
                    st.danger(f"⚠️ Anda akan menghapus presensi tanggal **{selected_presensi['tanggal']}** (Status: {selected_presensi['status']})")
                    st.warning("Tindakan ini tidak dapat dibatalkan!")
                    
                    if st.button("🗑️ Ya, Hapus Presensi Ini", type="primary", use_container_width=True):
                        result = delete_presensi_mahasiswa(selected_presensi['id'])
                        if result['success']:
                            st.success(result['message'])
                            st.rerun()
                        else:
                            st.error(result['message'])
