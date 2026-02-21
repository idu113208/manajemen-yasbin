"""
Improved horizontal navigation (modern + interactive)
"""
import streamlit as st

def horizontal_navbar():
    """Navigasi utama - HORIZONTAL di atas (styled + interactive)
    - Menyuntikkan CSS untuk hover / shadow / responsive cards
    - Tetap menggunakan st.button() untuk navigasi (session-state)
    """
    role = st.session_state.get('role', 'Unknown')
    username = st.session_state.get('username', 'Unknown')

    # Global styles for navbar & header
    st.markdown("""
    <style>
    /* Header / hero */
    .hb-hero { background: linear-gradient(135deg,#4f46e5 0%, #7c3aed 100%); padding:18px; border-radius:12px; color: #fff; box-shadow: 0 8px 30px rgba(2,6,23,0.45); margin-bottom:18px;}
    .hb-hero h2 { margin:0; font-size:28px; letter-spacing:0.2px; }
    .hb-hero p { margin:6px 0 0 0; opacity:0.9; font-size:13px; }

    /* Profile small button */
    .hb-profile .stButton>button { background: rgba(255,255,255,0.05) !important; color: #fff !important; border-radius: 10px !important; padding: 6px 12px !important; border: 1px solid rgba(255,255,255,0.06) !important; }

    /* Horizontal menu - cards */
    .stApp .hb-menu .stButton>button {
        background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01)) !important;
        color: #e6eef9 !important;
        border: 1px solid rgba(255,255,255,0.04) !important;
        border-radius: 12px !important;
        padding: 14px 10px !important;
        min-height: 72px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        gap: 6px !important;
        font-weight: 600 !important;
        transition: transform .14s ease, box-shadow .14s ease, background .14s ease !important;
        box-shadow: 0 6px 18px rgba(2,6,23,0.35) !important;
    }
    .stApp .hb-menu .stButton>button:hover {
        transform: translateY(-6px) scale(1.02) !important;
        box-shadow: 0 16px 40px rgba(2,6,23,0.55) !important;
        background: linear-gradient(90deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01)) !important;
    }
    .stApp .hb-menu .stButton>button:active { transform: translateY(-2px) !important; }

    /* Make labels wrap nicely */
    .stApp .hb-menu .stButton>button { white-space: normal !important; text-align:center !important; font-size:14px !important; }

    /* Quick visual separator */
    .hb-selected { margin-top: 8px; padding:6px 10px; border-radius:999px; background: rgba(255,255,255,0.02); color: #cfe8ff; display:inline-block; font-size:13px; border:1px solid rgba(255,255,255,0.02);}    

    /* Responsive tweaks */
    @media (max-width: 800px) {
        .hb-hero h2 { font-size:20px; }
        .stApp .hb-menu .stButton>button { min-height:64px !important; padding:10px !important; }
    }
    </style>
    """, unsafe_allow_html=True)

    # Header with profile
    col_header, col_profile = st.columns([4, 1])
    with col_header:
        st.markdown(f"""
            <div class="hb-hero">
                <h2>🎓 Dashboard Bintrebusih</h2>
                <p>Logged in as: <strong>{username}</strong> &nbsp;|&nbsp; Role: <strong>{role}</strong></p>
            </div>
        """, unsafe_allow_html=True)

    with col_profile:
        st.markdown('<div class="hb-profile"></div>', unsafe_allow_html=True)
        st.write("")
        st.write("")
        if st.button("👤 Profile"):
            st.switch_page("pages/profile.py")

    # Menu options (unchanged behaviour but prettier appearance)
    menu_options_data = {
        "Admin": [
            ("📊 Dashboard", "Dashboard"),
            ("👥 Manajemen Data", "Manajemen Data"),
            ("📍 Presensi", "Presensi"),
            ("📚 Pendampingan", "Pendampingan"),
            ("📋 Laporan", "Laporan"),
            ("📢 Pengumuman", "Pengumuman"),
            ("⚙️ Pengaturan", "Pengaturan"),
            ("🚪 Logout", "Logout")
        ],
        "Pendamping": [
            ("📊 Dashboard", "Dashboard"),
            ("📥 Upload Materi", "Upload Materi"),
            ("📤 Upload Laporan", "Upload Laporan"),
            ("📢 Pengumuman", "Pengumuman"),
            ("⚙️ Pengaturan", "Pengaturan"),
            ("🚪 Logout", "Logout")
        ],
        "Mahasiswa": [
            ("📊 Dashboard", "Dashboard"),
            ("📤 Upload Tugas", "Upload Tugas"),
            ("📭 Tugas Saya", "Tugas Saya"),
            ("📚 Materi Pembelajaran", "Materi Pembelajaran"),
            ("📢 Pengumuman", "Pengumuman"),
            ("🚪 Logout", "Logout")
        ],
        "Mitra Kerja": [
            ("📊 Dashboard", "Dashboard"),
            ("📋 Daftar Mahasiswa", "Daftar Mahasiswa"),
            ("📢 Pengumuman", "Pengumuman"),
            ("🚪 Logout", "Logout")
        ]
    }

    options = menu_options_data.get(role, menu_options_data["Mahasiswa"])
    menu_labels = [opt[0] for opt in options]
    menu_values = [opt[1] for opt in options]

    # Render horizontal menu (styled via CSS above)
    st.markdown('<div class="hb-menu"></div>', unsafe_allow_html=True)
    cols = st.columns(len(menu_labels))

    for idx, (col, label, value) in enumerate(zip(cols, menu_labels, menu_values)):
        with col:
            if st.button(label, use_container_width=True, key=f"nav_{idx}"):
                st.session_state.selected_menu = value

    # Show selected menu pill
    current = st.session_state.get('selected_menu', menu_values[0])
    st.markdown(f'<div class="hb-selected">Viewing: <strong>{current}</strong></div>', unsafe_allow_html=True)

    st.divider()
    return current
