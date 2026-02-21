import streamlit as st
import sqlite3
from datetime import datetime

def login():
    """Halaman login untuk sistem"""
    
    # Custom CSS - Simple Dark Theme
    st.markdown("""
        <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        html, body, [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #2C3E50 0%, #34495E 100%);
            min-height: 100vh;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        
        [data-testid="stAppViewContainer"] {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        [data-testid="stVerticalBlock"] {
            width: 100%;
            max-width: 350px;
        }
        
        /* Hide sidebar */
        [data-testid="stSidebar"] {
            display: none;
        }
        
        .login-wrapper {
            text-align: center;
        }
        
        .login-title {
            color: #FFFFFF;
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 8px;
            text-align: center;
        }
        
        .login-subtitle {
            color: #BDC3C7;
            font-size: 12px;
            margin-bottom: 32px;
            text-align: center;
        }
        
        [data-testid="stTextInput"] {
            margin-bottom: 12px;
        }
        
        [data-testid="stTextInput"] label {
            color: #ECF0F1 !important;
            font-weight: 600;
            font-size: 12px !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 6px !important;
            display: block !important;
        }
        
        [data-testid="stTextInput"] input {
            background-color: #FFFFFF !important;
            color: #2C3E50 !important;
            border: 1px solid #D0D0D0 !important;
            border-radius: 4px !important;
            padding: 10px 12px !important;
            font-size: 14px !important;
            transition: all 0.3s ease !important;
            width: 100% !important;
        }
        
        [data-testid="stTextInput"] input:focus {
            border-color: #3498DB !important;
            box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1) !important;
            outline: none !important;
        }
        
        [data-testid="stCheckbox"] {
            margin: 16px 0 !important;
        }
        
        [data-testid="stCheckbox"] label {
            color: #ECF0F1 !important;
            font-size: 13px !important;
        }
        
        button[kind="primary"] {
            background: #3498DB !important;
            color: white !important;
            border: none !important;
            border-radius: 4px !important;
            padding: 10px 20px !important;
            font-size: 14px !important;
            font-weight: 600 !important;
            cursor: pointer !important;
            width: 100% !important;
            transition: all 0.3s ease !important;
            margin-top: 12px !important;
        }
        
        button[kind="primary"]:hover {
            background: #2980B9 !important;
            box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3) !important;
        }
        
        button[kind="primary"]:active {
            transform: translateY(1px) !important;
        }
        
        .footer-text {
            color: #95A5A6;
            font-size: 11px;
            margin-top: 24px;
            text-align: center;
        }
        
        @media (max-width: 600px) {
            [data-testid="stVerticalBlock"] {
                max-width: 100%;
            }
            
            .login-title {
                font-size: 28px;
            }
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="login-wrapper"><h1 class="login-title">Login</h1><p class="login-subtitle">Masukkan kredensial Anda</p></div>', unsafe_allow_html=True)
    
    # Username/Email input
    username = st.text_input("Username", key="login_username", placeholder="testuser")
    
    # Password input
    password = st.text_input("Password", type="password", key="login_password", placeholder="••••••••")
    
    # Remember me checkbox
    remember = st.checkbox("Remember me", value=False, key="remember_me")
    
    # Login button
    if st.button("🔓 Submit", use_container_width=True, key="login_btn"):
        if username and password:
            if authenticate_user(username, password):
                user_role = get_user_role(username)
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = user_role
                st.success("✅ Login berhasil! Redirecting...")
                st.balloons()
                st.rerun()
            else:
                st.error("❌ Username atau password salah!")
        else:
            st.warning("⚠️ Masukkan username dan password!")
    
    st.markdown('<p class="footer-text">© 2026 Bintrebusih</p>', unsafe_allow_html=True)

def authenticate_user(username, password):
    """Verifikasi pengguna"""
    demo_users = {
        "testuser": "testpass",
        "admin": "admin123",
        "pendamping1": "pass123",
        "mitra1": "pass123",
        "mahasiswa1": "pass123",
        "mahasiswa2": "pass123"
    }
    
    return demo_users.get(username) == password

def get_user_role(username):
    """Dapatkan role user"""
    roles = {
        "testuser": "Admin",
        "admin": "Admin",
        "pendamping1": "Pendamping",
        "mitra1": "Mitra Kerja",
        "mahasiswa1": "Mahasiswa",
        "mahasiswa2": "Mahasiswa"
    }
    return roles.get(username, "Viewer")

def check_login():
    """Cek apakah user sudah login"""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        login()
        st.stop()

def logout():
    """Logout user"""
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.success("✅ Logout berhasil!")
    st.rerun()
