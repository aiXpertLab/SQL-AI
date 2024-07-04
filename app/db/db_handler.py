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
import os
import streamlit as st
import psycopg2
import pandas as pd


class DatabaseHandler:

    def __init__(self):
        """
        Establishes a connection to the PostgreSQL database using the provided URI
        """
        try:            
            self.connection = psycopg2.connect(os.environ.get('POSTGRESQL_AI_URI'))  # Connect to the database
            self.cursor = self.connection.cursor()  # Initialize a cursor
        except Exception as e:
            st.error(f"Failed to connect to the database: {e}")
            raise

    def execute_sql(self, solution):
        try:
            _,final_query,_ = solution.split("```")
            final_query = final_query.strip('sql')
            self.cursor.execute(final_query)
            result = self.cursor.fetchall()
            return str(result)
        except Exception as e:
            st.error(f"Failed to save database details: {e}")
            raise
        finally:
            self.cursor.close()
            self.connection.close()

    def get_basic_table_details(self):
        """ run once in global_initialization
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

    def get_db_schema(self):
        """ run once in global_initialization
            :param query:
            :param unique_id:
            :param db_uri:
            :return:
        """
        try:
            tables_and_columns = self.get_basic_table_details()  # Fetch table details
            df = pd.DataFrame(tables_and_columns, columns=['table_name', 'column_name', 'data_type'])
            # df.to_csv(st.session_state.TABLES_COLUMNS_CSV, index=False)  # Save details to CSV file
            table_info = ''
            for table in df['table_name']:
                table_info += f'Information about table {table}:\n'
                table_info += df[df['table_name'] == table].to_string(index=False) + '\n\n\n'
            return table_info
        except Exception as e:
            st.error(f"Failed to save database details: {e}")
            raise
        finally:
            self.cursor.close()
            self.connection.close()
