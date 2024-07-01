# llm_handler.py
import streamlit as st

import os
from langchain_openai import OpenAI, ChatOpenAI, OpenAIEmbeddings
from . import llm_prompt_engineer


class LLMHandler:

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.llm = OpenAI(openai_api_key=self.api_key)
        self.chat_llm = ChatOpenAI(openai_api_key=self.api_key, temperature=0.4)
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)

    def get_response_from_llm(self, query):
        """
            :param query:
            :param unique_id:
            :param db_uri:
            :return:
        """
        table_info = st.session_state.DB_SCHEMA
        content = llm_prompt_engineer.sql_based_on_tables(query, table_info, self.chat_llm)
        return content
