import os, mysql.connector, streamlit as st
from datetime import datetime

# Function to call the API with the provided URI
def send_message(message):
    return {"message": message}