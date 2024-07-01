# llm_prompt_engineer.py
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.prompts import HumanMessagePromptTemplate


def sql_based_on_tables(query, table_info, chat_llm):
    template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=(
                    f"You are an assistant that can write complicated SQL Queries."
                    f"Given the text below, write a SQL query that answers the user's question."
                    f"DB connection string is {os.environ.get('POSTGRESQL_AI_URI')}"
                    f"Here is a detailed description of the table(s): "
                    f"{table_info}"
                    "Prepend and append the SQL query with three backticks '```'"
                )
            ),
            HumanMessagePromptTemplate.from_template("{text}"),
        ]
    )
    answer = chat_llm(template.format_messages(text=query))
    return answer.content


def sql_for_schema(query, db_uri):
    template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=(
                    "You are an assistant who writes SQL queries."
                    "Given the text below, write a SQL query that answers the user's question."
                    "Prepend and append the SQL query with three backticks '```'"
                    "Write select query whenever possible"
                    f"Connection string to this database is {db_uri}"
                )
            ),
            HumanMessagePromptTemplate.from_template("{text}"),

        ]
    )

    answer = chat_llm(template.format_messages(text=query))
    print(answer.content)
    return answer.content


def sql_for_foreignkeys(query, relevant_tables, table_info, foreign_key_info):
    tables = ",".join(relevant_tables)
    template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=(
                    f"You are an assistant that can write SQL Queries."
                    f"Given the text below, write a SQL query that answers the user's question."
                    f"Assume that there is/are SQL table(s) named '{tables}' "
                    f"Here is a more detailed description of the table(s): "
                    f"{table_info}"
                    "Here is some information about some relevant foreign keys:"
                    f"{foreign_key_info}"
                    "Prepend and append the SQL query with three backticks '```'"
                )
            ),
            HumanMessagePromptTemplate.from_template("{text}"),

        ]
    )

    answer = chat_llm(template.format_messages(text=query))
    print(answer.content)
    return answer.content
