"""
Module Name: DatabaseHandler
Author: Leo Reny
Date: Jun 24, 2024
Version: 1.0

Description:
This module defines the DatabaseHandler class, which manages database connections,
retrieves basic table details from a PostgreSQL database, and saves these details to a CSV file.

Classes:
- DatabaseHandler: A class to handle database interactions and session state management.

Methods:
- __init__(self, db_uri): pass uri, save uri into session_state.
- save_db_details(self): ----------------------------------- Saves the fetched table details to a CSV file and returns a unique ID.
    └── get_basic_table_details(self): --------------------- Fetches basic details of tables in the 'public' schema.
        └── connect_to_db(self): --------------------------- Establishes a connection to the PostgreSQL database.
            └── _create_data_folder(self): ----------------- Creates a 'data' folder if it does not already exist.

Usage:
Instantiate the DatabaseHandler class with a database URI, 
then call save_db_details to connect to the database, fetch table details, and save them to a CSV file.
"""

import streamlit as st
import psycopg2
import pandas as pd
from uuid import uuid4


class DatabaseHandler:
    def __init__(self):
        """
        Establishes a connection to the PostgreSQL database using the provided URI and initializes a unique ID.
        """
        try:            
            self.connection = psycopg2.connect(st.session_state.db_uri)  # Connect to the database
            self.cursor = self.connection.cursor()  # Initialize a cursor
        except Exception as e:
            st.error(f"Failed to connect to the database: {e}")
            raise

    def get_basic_table_details(self):
        """
        Fetches basic details (table names, column names, and data types) of tables in the 'public' schema.

        Returns:
            list: A list of tuples containing table details.
        """

        query = """
        SELECT
            c.table_name,
            c.column_name,
            c.data_type
        FROM
            information_schema.columns c
        WHERE
            c.table_name IN (
                SELECT tablename
                FROM pg_tables
                WHERE schemaname = 'public'
        );
        """
        self.cursor.execute(query)
        tables_and_columns = self.cursor.fetchall()
        return tables_and_columns

    def save_db_details(self) -> str:
        """
        Fetches the basic table details and saves them to a CSV file named with the unique ID.
        Closes the database connection afterward.

        Returns:
            str: The unique ID for the session.
        """
        unique_id = str(uuid4()).replace("-", "_")
        st.code(f'save_db_details.DbHandler: {unique_id}')
        try:
            tables_and_columns = self.get_basic_table_details()  # Fetch table details
            df = pd.DataFrame(tables_and_columns, columns=['table_name', 'column_name', 'data_type'])
            filename = f'{st.session_state.tables}/t_{unique_id}.csv'
            df.to_csv(filename, index=False)  # Save details to CSV file
            return unique_id
        except Exception as e:
            st.error(f"Failed to save database details: {e}")
            raise
        finally:
            self.cursor.close()
            self.connection.close()
