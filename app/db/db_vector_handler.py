# db_vector_handler.py
import streamlit as st
import os
import psycopg2
import pandas as pd
from uuid import uuid4

from langchain_chroma import Chroma
from langchain_community.document_loaders import CSVLoader
from langchain_openai import OpenAI, ChatOpenAI, OpenAIEmbeddings

from .db_handler import DatabaseHandler


class DBVectorHandler(DatabaseHandler):
    def __init__(self):
        super().__init__()
        self.embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

    def create_vectors(self, filename, persist_directory):

        loader = CSVLoader(file_path=filename, encoding="utf8")
        data = loader.load()
        vectordb = Chroma.from_documents(data, embedding=self.embeddings, persist_directory=persist_directory)
        # vectordb.persist()

    def get_foreign_key_info(self, cursor):

        query_for_foreign_keys = """
        SELECT
            conrelid::regclass AS table_name,
            conname AS foreign_key,
            pg_get_constraintdef(oid) AS constraint_definition,
            confrelid::regclass AS referred_table,
            array_agg(a2.attname) AS referred_columns
        FROM
            pg_constraint
        JOIN
            pg_attribute AS a1 ON conrelid = a1.attrelid AND a1.attnum = ANY(conkey)
        JOIN
            pg_attribute AS a2 ON confrelid = a2.attrelid AND a2.attnum = ANY(confkey)
        WHERE
            contype = 'f'
            AND connamespace = 'public'::regnamespace
        GROUP BY
            conrelid, conname, oid, confrelid
        ORDER BY
            conrelid::regclass::text, contype DESC;
        """

        self.cursor.execute(query_for_foreign_keys)
        foreign_keys = self.cursor.fetchall()

        return foreign_keys

    def save_db_details(self):
        unique_id = str(uuid4()).replace("-", "_")
        try:
            self.create_vectors(st.session_state.path_tables_columns, f'{st.session_state.data}chroma')

            # Get all the foreign keys and enter them in a pandas dataframe
            foreign_keys = self.get_foreign_key_info(self.cursor)
            df = pd.DataFrame(foreign_keys, columns=['table_name', 'foreign_key', 'foreign_key_details', 'referred_table', 'referred_columns'])
            filename_fk = f'{st.session_state.foreignkeys}/foreign_keys_{unique_id}.csv'
            df.to_csv(filename_fk, index=False)
            return unique_id
        except Exception as e:
            st.error(f"Failed to save database details: {e}")
            raise
        finally:
            self.cursor.close()
            self.connection.close()
