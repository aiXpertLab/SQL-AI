"""
Module Name: SQL_AI
Version: 1.0

Description: Entrance.
Usage: Homepage
"""
import streamlit as st
from app.utils import streamlit_components, streamlit_docs, global_initialization

streamlit_components.streamlit_ui('🐬🦣 Chat with 🍃🦭')
streamlit_docs.main_intro()

with st.spinner('initializing...'):
    global_initialization.session_init()
st.write(st.session_state)
