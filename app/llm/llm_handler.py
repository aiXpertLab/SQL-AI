# llm_handler.py
import streamlit as st

import os
import pandas as pd
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.prompts import HumanMessagePromptTemplate
from langchain_chroma import Chroma
from langchain_openai import OpenAI, ChatOpenAI, OpenAIEmbeddings

from . import llm_prompt_engineer


class LLMHandler:

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.llm = OpenAI(openai_api_key=self.api_key)
        self.chat_llm = ChatOpenAI(openai_api_key=self.api_key, temperature=0.4)
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)
        self.table_info = st.session_state.DB_SCHEMA
        self.data_home = st.session_state.DATA_HOME

    def get_response_from_llm(self, query):
            """
                :param query:
                :param unique_id:
                :param db_uri:
                :return:
            """
            content = llm_prompt_engineer.sql_based_on_tables(query, self.chat_llm)
            return content
# ^PostgreSQL  --------------------------------------------------------------------------------------------- >vector>

    def schema_or_sql(self, query):
        template = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content=(
                        f"In the text given text user is asking a question about database "
                        f"Figure out whether user wants information about database schema or wants to write a SQL query"
                        f"Answer 'schema' if user wants information about database schema and 'sql' if user wants to write a SQL query"
                    )
                ),
                HumanMessagePromptTemplate.from_template("{text}"),
            ]
        )

        answer = self.chat_llm(template.format_messages(text=query))
        st.write(answer.content)
        return answer.content

    def get_response_from_llm_vector(self, query):
        schema_or_sql = self.schema_or_sql(query)
        if schema_or_sql == "schema":
            return llm_prompt_engineer.sql_for_schema(self.chat_llm, query)
        else:
            vectordb = st.session_state.VECTOR_EMBEDDINGS
            retriever = vectordb.as_retriever()
            docs = retriever.get_relevant_documents(query)
            st.write(docs)
            st.write('-'*100)

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

            # ## Load the foreign keys csv
            # filename_fk = f'{st.session_state.foreignkeys}foreign_keys_{unique_id}.csv'
            # df_fk = pd.read_csv(filename_fk)
            # ## If table from relevant_tables above lies in refered_table or table_name in df_fk, then add the foreign key details to a string
            # foreign_key_info = ''
            # for i, series in df_fk.iterrows():
            #     if series['table_name'] in relevant_tables:
            #         text = table + ' has a foreign key ' + series['foreign_key'] + ' which refers to table ' + series[
            #             'referred_table'] + ' and column(s) ' + series['referred_columns']
            #         foreign_key_info += text + '\n\n'
            #     if series['referred_table'] in relevant_tables:
            #         text = table + ' is referred to by table ' + series['table_name'] + ' via foreign key ' + series[
            #             'foreign_key'] + ' and column(s) ' + series['referred_columns']
            #         foreign_key_info += text + '\n\n'
            #
            # return llm_prompt_engineer.sql_for_foreignkeys(query, relevant_tables, table_info, foreign_key_info)
