# llm_handler.py
import streamlit as st

import os
import pandas as pd
import psycopg2
from langchain_openai import OpenAI, ChatOpenAI, OpenAIEmbeddings
from . import llm_prompt_engineer


class LLMHandler:

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.llm = OpenAI(openai_api_key=self.api_key)
        self.chat_llm = ChatOpenAI(openai_api_key=self.api_key, temperature=0.4)
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)

    def get_the_output_from_llm(self, query, unique_id):
        """
            :param query:
            :param unique_id:
            :param db_uri:
            :return:
        """
        filename_t = f'{st.session_state.tables}t_{unique_id}.csv'
        df = pd.read_csv(filename_t)
        table_info = ''
        for table in df['table_name']:
            table_info += f'Information about table {table}:\n'
            table_info += df[df['table_name'] == table].to_string(index=False) + '\n\n\n'
        return llm_prompt_engineer.sql_generated_from_tables(query, table_info, self.chat_llm)

    def execute_the_solution(self, solution):
        connection = psycopg2.connect(st.session_state.db_uri)
        cursor = connection.cursor()
        _,final_query,_ = solution.split("```")
        final_query = final_query.strip('sql')
        cursor.execute(final_query)
        result = cursor.fetchall()
        return str(result)

