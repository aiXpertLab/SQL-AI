"""
Module Name: SQL_AI
Version: 1.0

Description: Entrance.
Usage: Homepage
"""
import streamlit as st
from app.utils import (
    streamlit_components,
    streamlit_docs,
    global_initialization
)

# Set up the Streamlit UI with a custom title
streamlit_components.streamlit_ui('🐬🦣 Chat with 🍃🦭')

# Display a spinner while initializing
with st.spinner('initializing...'):

    global_initialization.session_init()    # Initialize the session
    streamlit_docs.main_intro()             # Display the main introduction

# Display a success message once initialization is complete
st.success(f'system is ready.')
