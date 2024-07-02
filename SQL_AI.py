"""
Module Name: SQL_AI
Version: 1.0

Description: Entrance.
Usage: Homepage
"""
import streamlit as st
from app.utils import streamlit_components, streamlit_docs, global_initialization

streamlit_components.streamlit_ui('🐬🦣 Chat with 🍃🦭')

with st.spinner('initializing...'):
    global_initialization.session_init()
    streamlit_docs.main_intro()
st.success(f'system is ready.')
