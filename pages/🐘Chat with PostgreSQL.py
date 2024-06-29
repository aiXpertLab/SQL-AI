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

        # init session_state: uri, unique_id, message
        session_handler.session_init()
        # st.write(st.session_state)

        # init: session_state add uri, with save() get unique_id.
        db_handler = db_handler.DatabaseHandler()

        # Initialize the language model handler with the OpenAI API key
        llm_handler = llm_handler.LLMHandler()

        # Create an instance of the Streamlit UI and pass the handlers to it
        app = chat_ui.ChatUI(db_handler, llm_handler)

        # Run the Streamlit application
        app.run()
