# llm_handler.py
import streamlit as st

import os
from langchain_openai import OpenAI, ChatOpenAI, OpenAIEmbeddings

from . import llm_prompt_engineer


class LLMHandler:
    """
        A class to handle interactions with the OpenAI language model, including
        generating responses based on SQL queries and vector embeddings.

        Attributes:
        ----------
        api_key : str
            The API key for accessing OpenAI services.
        llm : OpenAI
            An instance of the OpenAI language model.
        chat_llm : ChatOpenAI
            An instance of the OpenAI chat model with specified temperature.
        embeddings : OpenAIEmbeddings
            An instance of OpenAI embeddings for vector-based operations.
        table_info : str
            Information about the database schema.
        data_home : str
            The home directory for data storage.

        Methods:
        -------
        get_response_from_llm(query: str) -> str:
            Generates a response based on the provided SQL query using the language model.

        get_response_from_llm_vector(query: str) -> str:
            Generates a response based on the provided SQL query using vector embeddings to retrieve relevant documents.
        """
    def __init__(self):
        """
        Constructs all the necessary attributes for the LLMHandler object.
        """
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.llm = OpenAI(openai_api_key=self.api_key)
        self.chat_llm = ChatOpenAI(openai_api_key=self.api_key, temperature=0.4)
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)
        self.table_info = st.session_state.DB_SCHEMA
        self.data_home = st.session_state.DATA_HOME

    def get_response_from_llm(self, query):
        """
        Generates a response based on the provided SQL query using the language model.

        Parameters:
        ----------
        query : str
            The SQL query to be processed.

        Returns:
        -------
        str:
            The generated response content.
        """

        content = llm_prompt_engineer.sql_based_on_tables(query, self.chat_llm)
        return content
# ^PostgreSQL  --------------------------------------------------------------------------------------------- >vector>

    def get_response_from_llm_vector(self, query):
        """
        Generates a response based on the provided SQL query using vector embeddings
        to retrieve relevant documents.

        Parameters:
        ----------
        query : str
            The SQL query to be processed.

        Returns:
        -------
        str:
            The generated response content based on vector embeddings.
        """
        vectordb = st.session_state.VECTOR_EMBEDDINGS
        retriever = vectordb.as_retriever()
        docs = retriever.get_relevant_documents(query)

        relevant_tables = []
        relevant_tables_and_columns = []

        for doc in docs:
            table_name, column_name, data_type = doc.page_content.split("\n")
            table_name = table_name.split(":")[1].strip()
            relevant_tables.append(table_name)
            column_name = column_name.split(":")[1].strip()
            data_type = data_type.split(":")[1].strip()
            relevant_tables_and_columns.append((table_name, column_name, data_type))

        tables = ",".join(relevant_tables)
        table_info = st.session_state.DB_SCHEMA

        return llm_prompt_engineer.sql_for_vector(query, relevant_tables, table_info, self.chat_llm)
