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
from app.utils import streamlit_components,streamlit_docs

streamlit_components.streamlit_ui('🦣 PostgreSQL')
streamlit_docs.postgre_intro()
# -----------------------------------------------------------------------------------------------------------
from app import (
    chat_ui,
    db_handler,
    llm_handler
)


if __name__ == "__main__":
    db_handler = db_handler.DatabaseHandler()   # init: session_state add uri, with save() get unique_id.
    llm_handler = llm_handler.LLMHandler()      # Initialize the language model handler with the OpenAI API key
    app = chat_ui.ChatUI(db_handler, llm_handler, 'vector')   # Create an instance of the Streamlit UI and pass the handlers to it

    app.run()   # Run the Streamlit application
