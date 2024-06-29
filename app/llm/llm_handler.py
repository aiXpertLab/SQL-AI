import os
import pandas as pd
import psycopg2
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.prompts import HumanMessagePromptTemplate
from langchain_openai import OpenAI, ChatOpenAI, OpenAIEmbeddings


class LLMHandler:

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.llm = OpenAI(openai_api_key=self.api_key)
        self.chat_llm = ChatOpenAI(openai_api_key=self.api_key, temperature=0.4)
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)

    def generate_template_for_sql(self, query, table_info, db_uri):
        template = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content=(
                        f"You are an assistant that can write complicated SQL Queries."
                        f"Given the text below, write a SQL query that answers the user's question."
                        f"DB connection string is {db_uri}"
                        f"Here is a detailed description of the table(s): "
                        f"{table_info}"
                        "Prepend and append the SQL query with three backticks '```'"
                    )
                ),
                HumanMessagePromptTemplate.from_template("{text}"),
            ]
        )
        answer = self.chat_llm(template.format_messages(text=query))
        return answer.content

    def get_the_output_from_llm(self, query, unique_id, db_uri):
        """
            :param query:
            :param unique_id:
            :param db_uri:
            :return:
        """

        filename_t = f'data/tables_{unique_id}.csv'
        df = pd.read_csv(filename_t)
        table_info = ''
        for table in df['table_name']:
            table_info += f'Information about table {table}:\n'
            table_info += df[df['table_name'] == table].to_string(index=False) + '\n\n\n'
        return self.generate_template_for_sql(query, table_info, db_uri)

    def execute_the_solution(self, solution, db_uri):
        connection = psycopg2.connect(db_uri)
        cursor = connection.cursor()
        _, final_query, _ = solution.split("```")
        final_query = final_query.strip('sql')
        cursor.execute(final_query)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return str(result)
