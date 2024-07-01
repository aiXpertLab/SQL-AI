"""
    Module Name: Chat with PostgreSQL
    Version: 1.0

    Description: PostgreSQL entrance page.

    Initialize:
    - message
    - uri
    - unique_id
    - ui to run()
"""
import streamlit as st
from utils import streamlit_components, docs

streamlit_components.streamlit_ui('🦣 PostgreSQL')
docs.postgre_intro()
# -----------------------------------------------------------------------------------------------------------
from app import db_handler, session_handler, llm_handler, chat_ui

with st.spinner('loading'):
    if __name__ == "__main__":

        session_handler.session_init()              # init session_state: uri, unique_id, message
        db_handler = db_handler.DatabaseHandler()   # init: session_state add uri, with save() get unique_id.
        llm_handler = llm_handler.LLMHandler()      # Initialize the language model handler with the OpenAI API key
        app = chat_ui.ChatUI(db_handler, llm_handler)   # Create an instance of the Streamlit UI and pass the handlers to it

        app.run()   # Run the Streamlit application
