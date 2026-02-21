"""
Halaman Profile User
User bisa melihat dan mengedit profile pribadi mereka
"""
import streamlit as st
import pandas as pd
from modules.auth import check_login
from modules.navbar import horizontal_navbar
from modules.crud import get_connection
from datetime import datetime

# Check login
check_login()

# Navigation Bar
horizontal_navbar()

st.title("👤 Profile Pribadi Saya")

username = st.session_state.get('username', 'Unknown')
role = st.session_state.get('role', 'Unknown')

# Get user data from database
conn = get_connection()
cursor = conn.cursor()

cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
user_data = dict(cursor.fetchone() or {})
conn.close()

# Tab untuk View dan Edit
tab1, tab2 = st.tabs(["👁️ Lihat Profile", "✏️ Edit Profile"])

# ==================== TAB 1: VIEW PROFILE ====================
with tab1:
    st.subheader("Informasi Pribadi")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write(f"**Username:** {user_data.get('username', '-')}")
        st.write(f"**Email:** {user_data.get('email', '-')}")
        st.write(f"**Nama Lengkap:** {user_data.get('nama_lengkap', '-')}")
        st.write(f"**Role:** {user_data.get('role', '-')}")
        st.write(f"**Akun Dibuat:** {user_data.get('created_at', '-')}")
    
    with col2:
        st.info(f"""
        ### 👤 {user_data.get('nama_lengkap', username)}
        
        **Role:** {user_data.get('role', 'Unknown')}
        
        **Status:** ✅ Aktif
        """)

# ==================== TAB 2: EDIT PROFILE ====================
with tab2:
    st.subheader("Edit Informasi Pribadi")
    
    st.warning("⚠️ Hati-hati saat mengubah data - pastikan informasi yang Anda masukkan benar")
    
    col1, col2 = st.columns(2)
    
    with col1:
        nama_lengkap = st.text_input(
            "Nama Lengkap",
            value=user_data.get('nama_lengkap', '')
        )
        email = st.text_input(
            "Email",
            value=user_data.get('email', '')
        )
    
    with col2:
        new_password = st.text_input(
            "Password Baru (kosongkan jika tidak ingin ubah)",
            type="password"
        )
        confirm_password = st.text_input(
            "Konfirmasi Password Baru",
            type="password"
        )
    
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Simpan Perubahan", type="primary", use_container_width=True):
            # Validasi
            if not nama_lengkap:
                st.error("Nama lengkap tidak boleh kosong!")
            elif not email:
                st.error("Email tidak boleh kosong!")
            elif new_password and new_password != confirm_password:
                st.error("Password tidak cocok!")
            else:
                # Update database
                conn = get_connection()
                cursor = conn.cursor()
                
                try:
                    if new_password:
                        cursor.execute(
                            'UPDATE users SET nama_lengkap = ?, email = ?, password = ? WHERE username = ?',
                            (nama_lengkap, email, new_password, username)
                        )
                    else:
                        cursor.execute(
                            'UPDATE users SET nama_lengkap = ?, email = ? WHERE username = ?',
                            (nama_lengkap, email, username)
                        )
                    
                    conn.commit()
                    st.success("✅ Profile berhasil diperbarui!")
                    st.balloons()
                    
                    # Update session state
                    st.session_state.nama_lengkap = nama_lengkap
                    
                    # Refresh page
                    import time
                    time.sleep(1)
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                finally:
                    conn.close()
    
    with col2:
        if st.button("🔄 Reset", use_container_width=True):
            st.rerun()
    
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.clear()
            st.info("Terima kasih! Anda telah logout.")
            st.switch_page("pages/login.py")
    
    st.divider()
    
    st.subheader("📊 Informasi Akun Lainnya")
    
    info_data = {
        'Informasi': [
            'Username',
            'Email Verified',
            'Akun Aktif Sejak',
            'Akses Terakhir',
            'Role',
            'Status'
        ],
        'Detail': [
            user_data.get('username', '-'),
            '✅ Terverifikasi',
            user_data.get('created_at', '-'),
            'Hari ini',
            user_data.get('role', '-'),
            '✅ Aktif'
        ]
    }
    
    df_info = pd.DataFrame(info_data)
    st.dataframe(df_info, use_container_width=True, hide_index=True)
