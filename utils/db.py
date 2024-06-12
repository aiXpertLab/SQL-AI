import os, mysql.connector, streamlit as st
from datetime import datetime

def connect_with_pgsql(uri):
    st.session_state.db_uri = uri
    return {"message": "Connection established to Database!"}

