# llm_vector_handler.py
import streamlit as st
import pandas as pd

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.prompts import HumanMessagePromptTemplate
from langchain_chroma import Chroma
from langchain_openai import OpenAI, ChatOpenAI, OpenAIEmbeddings

from . import llm_handler, llm_prompt_engineer


class LLMVectorHandler(llm_handler.LLMHandler):
    def __init__(self):
        super().__init__()

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

    def get_the_output_from_llm(self, query, unique_id):
        # Load the tables csv
        filename_t = f'{st.session_state.tables}tables_{unique_id}.csv'
        df = pd.read_csv(filename_t)

        # For each relevant table create a string that list down all the columns and their data types
        table_info = ''
        for table in df['table_name']:
            table_info += 'Information about table' + table + ':\n'
            table_info += df[df['table_name'] == table].to_string(index=False) + '\n\n\n'

        schema_or_sql = self.schema_or_sql(query)
        if schema_or_sql == "schema":
            return llm_prompt_engineer.sql_for_schema(query, st.session_state.db_uri)
        else:
            vectordb = Chroma(embedding_function=self.embeddings, persist_directory=f"{st.session_state.tables}tables_{unique_id}")
            retriever = vectordb.as_retriever()
            docs = retriever.get_relevant_documents(query)
            print(docs)

            relevant_tables = []
            relevant_tables_and_columns = []

            for doc in docs:
                table_name, column_name, data_type = doc.page_content.split("\n")
                table_name = table_name.split(":")[1].strip()
                relevant_tables.append(table_name)
                column_name = column_name.split(":")[1].strip()
                data_type = data_type.split(":")[1].strip()
                relevant_tables_and_columns.append((table_name, column_name, data_type))

            ## Load the tables csv
            filename_t = f'{st.session_state.foreignkeys}tables_{unique_id}.csv'
            df = pd.read_csv(filename_t)

            ## For each relevant table create a string that list down all the columns and their data types
            table_info = ''
            for table in relevant_tables:
                table_info += 'Information about table' + table + ':\n'
                table_info += df[df['table_name'] == table].to_string(index=False) + '\n\n\n'

            ## Load the foreign keys csv
            filename_fk = f'{st.session_state.foreignkeys}foreign_keys_{unique_id}.csv'
            df_fk = pd.read_csv(filename_fk)
            ## If table from relevant_tables above lies in refered_table or table_name in df_fk, then add the foreign key details to a string
            foreign_key_info = ''
            for i, series in df_fk.iterrows():
                if series['table_name'] in relevant_tables:
                    text = table + ' has a foreign key ' + series['foreign_key'] + ' which refers to table ' + series[
                        'referred_table'] + ' and column(s) ' + series['referred_columns']
                    foreign_key_info += text + '\n\n'
                if series['referred_table'] in relevant_tables:
                    text = table + ' is referred to by table ' + series['table_name'] + ' via foreign key ' + series[
                        'foreign_key'] + ' and column(s) ' + series['referred_columns']
                    foreign_key_info += text + '\n\n'

            return llm_prompt_engineer.sql_for_foreignkeys(query, relevant_tables, table_info, foreign_key_info)
