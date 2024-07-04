# llm_prompt_engineer.py
import streamlit as st
import os

from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate


def sql_based_on_tables(query, chat_llm):
    template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=(
                    f"You are an assistant that can write complicated SQL Queries."
                    f"Given the text below, write a SQL query that answers the user's question."
                    f"DB connection string is {os.environ.get('POSTGRESQL_AI_URI')}"
                    f"Here is a detailed description of the table(s): "
                    f"{st.session_state.DB_SCHEMA}"
                    "Prepend and append the SQL query with three backticks '```'"
                )
            ),
            HumanMessagePromptTemplate.from_template("{text}"),
        ]
    )
    answer = chat_llm(template.format_messages(text=query))
    return answer.content


def sql_for_schema(query, chat_llm):
    template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=(
                    "You are an assistant who writes SQL queries."
                    "Given the text below, write a SQL query that answers the user's question."
                    "Prepend and append the SQL query with three backticks '```'"
                    "Write select query whenever possible"
                    f"Connection string to this database is {os.environ.get('POSTGRESQL_AI_URI')}"
                )
            ),
            HumanMessagePromptTemplate.from_template("{text}"),
        ]
    )

    answer = chat_llm(template.format_messages(text=query))
    print(answer.content)
    return answer.content


def sql_for_vector(query, relevant_tables, table_info, chat_llm):
    template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=(
                    f"You are an assistant that can write SQL Queries."
                    f"Given the text below, write a SQL query that answers the user's question."
                    f"Assume that there is/are SQL table(s) named '{relevant_tables}' "
                    f"Here is a more detailed description of the table(s): "
                    f"{table_info}"
                    "Prepend and append the SQL query with three backticks '```'"
                )
            ),
            HumanMessagePromptTemplate.from_template("{text}"),

        ]
    )
    answer = chat_llm(template.format_messages(text=query))
    return answer.content