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

    db_handler = db_handler.DatabaseHandler()   # initialize database handler
    llm_handler = llm_handler.LLMHandler()      # initialize the language model handler with the OpenAI API key

    # Create an instance of the Streamlit UI and pass database and LLM handlers to it
    app = chat_ui.ChatUI(db_handler, llm_handler, 'others') # others means no vector

    app.run()   # Run the Streamlit application
