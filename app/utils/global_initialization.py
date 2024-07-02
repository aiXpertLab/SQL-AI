import streamlit as st

import os
import re

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAI, ChatOpenAI, OpenAIEmbeddings

from ..db import db_handler


def is_valid_postgresql_uri(uri):
    # Regular expression to validate the PostgreSQL URI format
    regex = (
        r"^(postgresql|postgres):\/\/"              # Scheme
        r"(?:(?P<user>[^:@\s]+)(?::(?P<password>[^@\s]*))?@)?"  # Optional user and password
        r"(?P<host>[^:\/\s]+)"                      # Host
        r"(?::(?P<port>\d+))?"                      # Optional port
        r"(?:\/(?P<dbname>[^\?\s]*))?"              # Database name
        r"(?:\?(?P<params>[^\s]+))?$"               # Optional query parameters
    )

    match = re.match(regex, uri)
    if not match:
        return False
    return True


def session_init():

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "DATA_HOME" not in st.session_state:
        st.session_state.DATA_HOME = []
        st.session_state.DATA_HOME = 'data/'

    if "DB_SCHEMA" not in st.session_state:
        st.session_state.DB_SCHEMA = []
        table_info: str = db_handler.DatabaseHandler().get_db_schema()

        # Save the document to the vector database
        # document = Document(content=table_info)
        document = Document(page_content=table_info)
        embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
        vectordb = Chroma(embedding_function=embeddings, persist_directory='data/chroma')
        vectordb.add_documents([document])

        st.session_state.DB_SCHEMA = table_info
        st.session_state.VECTOR_EMBEDDINGS = vectordb
