"""
Halaman CRUD Pendamping
"""
import streamlit as st
import pandas as pd
from modules.crud import (
    read_all_pendamping,
    read_pendamping_by_id,
    create_pendamping,
    update_pendamping,
    delete_pendamping
)
from modules.auth import check_login
from modules.navbar import horizontal_navbar

# Check login
check_login()

# Navigation Bar
horizontal_navbar()

st.title("👨‍🏫 Manajemen Pendamping")

# Tab untuk Create dan View
tab1, tab2 = st.tabs(["📋 Data Pendamping", "➕ Tambah Pendamping"])

# ==================== TAB 2: TAMBAH PENDAMPING ====================
with tab2:
    st.subheader("Tambah Pendamping Baru")
    
    col1, col2 = st.columns(2)
    
    with col1:
        nama = st.text_input("Nama Lengkap *")
        nip = st.text_input("NIP")
        email = st.text_input("Email")
    
    with col2:
        no_hp = st.text_input("No. HP")
        alamat = st.text_area("Alamat", height=100)
    
    if st.button("💾 Simpan Pendamping", type="primary", use_container_width=True):
        if not nama:
            st.error("Nama tidak boleh kosong!")
        else:
            result = create_pendamping(
                nama=nama,
                nip=nip if nip else None,
                email=email if email else None,
                no_hp=no_hp if no_hp else None,
                alamat=alamat if alamat else None
            )
            
            if result['success']:
                st.success(result['message'])
                st.rerun()
            else:
                st.error(result['message'])

# ==================== TAB 1: DATA PENDAMPING ====================
with tab1:
    st.subheader("Data Pendamping Terdaftar")
    
    # Refresh button
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()
    
    # Get data
    pendampings = read_all_pendamping()
    
    if not pendampings:
        st.info("Belum ada data pendamping")
    else:
        # Display as table
        df = pd.DataFrame(pendampings)
        df = df[['id', 'nama', 'nip', 'email', 'no_hp', 'total_mahasiswa']]
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Management section
        st.divider()
        st.subheader("⚙️ Kelola Pendamping")
        
        col1, col2 = st.columns(2)
        
        with col1:
            selected_nama = st.selectbox(
                "Pilih Pendamping",
                options=[p['nama'] for p in pendampings]
            )
            selected_pdp = [p for p in pendampings if p['nama'] == selected_nama][0]
        
        with col2:
            action = st.radio("Pilih Aksi", ["👁️ Lihat Detail", "✏️ Edit", "🗑️ Hapus"], horizontal=True)
        
        # ===== VIEW DETAIL =====
        if action == "👁️ Lihat Detail":
            st.info("Detail Pendamping")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Nama:** {selected_pdp['nama']}")
                st.write(f"**NIP:** {selected_pdp['nip'] or '-'}")
                st.write(f"**Email:** {selected_pdp['email'] or '-'}")
            with col2:
                st.write(f"**No. HP:** {selected_pdp['no_hp'] or '-'}")
                st.write(f"**Alamat:** {selected_pdp['alamat'] or '-'}")
                st.write(f"**Total Mahasiswa:** {selected_pdp['total_mahasiswa']}")
        
        # ===== EDIT =====
        elif action == "✏️ Edit":
            st.warning("Edit Data Pendamping")
            
            col1, col2 = st.columns(2)
            
            with col1:
                nama_edit = st.text_input("Nama Lengkap", value=selected_pdp['nama'])
                nip_edit = st.text_input("NIP", value=selected_pdp['nip'] or "")
                email_edit = st.text_input("Email", value=selected_pdp['email'] or "")
            
            with col2:
                no_hp_edit = st.text_input("No. HP", value=selected_pdp['no_hp'] or "")
                alamat_edit = st.text_area("Alamat", value=selected_pdp['alamat'] or "", height=100)
            
            if st.button("💾 Simpan Perubahan", type="primary", use_container_width=True):
                result = update_pendamping(
                    selected_pdp['id'],
                    nama=nama_edit,
                    nip=nip_edit if nip_edit else None,
                    email=email_edit if email_edit else None,
                    no_hp=no_hp_edit if no_hp_edit else None,
                    alamat=alamat_edit if alamat_edit else None
                )
                
                if result['success']:
                    st.success(result['message'])
                    st.rerun()
                else:
                    st.error(result['message'])
        
        # ===== DELETE =====
        elif action == "🗑️ Hapus":
            st.danger(f"⚠️ Anda akan menghapus: **{selected_pdp['nama']}**")
            st.warning("Tindakan ini tidak dapat dibatalkan!")
            
            if st.button("🗑️ Ya, Hapus Pendamping Ini", type="primary", use_container_width=True):
                result = delete_pendamping(selected_pdp['id'])
                if result['success']:
                    st.success(result['message'])
                    st.rerun()
                else:
                    st.error(result['message'])
