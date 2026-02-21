"""
Halaman Login - Bintrebusih Dashboard
"""
import streamlit as st
import sqlite3
from modules.auth import login

# Jangan tampilkan sidebar

# Check if already logged in
if 'username' in st.session_state and st.session_state.get('username'):
    st.switch_page("app.py")
else:
    login()
