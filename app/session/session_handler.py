import streamlit as st

import os
import re


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

    # unique_id = str(uuid4()).replace("-", "_")  # Generate a unique ID
    #
    # if "unique_id" not in st.session_state:
    #     st.session_state.unique_id = []
    # st.session_state.unique_id = unique_id

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "db_uri" not in st.session_state:
        db_uri = os.environ.get('POSTGRESQL_AI_URI')
        st.code(db_uri)
        if db_uri and is_valid_postgresql_uri(db_uri):
            st.session_state.db_uri = db_uri
            st.success("Database URI is set successfully.")
        else:
            st.error("Invalid database URI.")

    if "foreignkeys" not in st.session_state:
        st.session_state.foreignkeys = []
    st.session_state.foreignkeys = 'data/foreignkeys/'

    if "vectors" not in st.session_state:
        st.session_state.vectors = []
        st.session_state.vectors = 'data/vectors/'

    if "tables" not in st.session_state:
        st.session_state.tables = []
        st.session_state.tables = 'data/tables/'
