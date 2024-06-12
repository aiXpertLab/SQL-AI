import streamlit as st
import os,  psycopg2
import pandas as pd
from uuid import uuid4

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.prompts import HumanMessagePromptTemplate

from langchain_openai import OpenAI, ChatOpenAI, OpenAIEmbeddings

from langchain_chroma import Chroma
from langchain_community.document_loaders.csv_loader import CSVLoader

uri = os.environ.get('POSTGRESQL_AI_URI')

folders_to_create = ['csvs', 'vectors']
# Check and create folders if they don't exist
for folder_name in folders_to_create:
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Folder '{folder_name}' created.")
    else:
        print(f"Folder '{folder_name}' already exists.")




## load the API key from the environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")


llm = OpenAI(openai_api_key=openai_api_key)
chat_llm = ChatOpenAI(openai_api_key=openai_api_key, temperature=0.4)
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)





def get_basic_table_details(cursor):
    cursor.execute("""SELECT
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
    );""")
    tables_and_columns = cursor.fetchall()
    return tables_and_columns



def get_foreign_key_info(cursor):
    query_for_foreign_keys = """SELECT
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

    cursor.execute(query_for_foreign_keys)
    foreign_keys = cursor.fetchall()

    return foreign_keys




def create_vectors(filename, persist_directory):
    loader = CSVLoader(file_path=filename, encoding="utf8")
    data = loader.load()
    vectordb = Chroma.from_documents(data, embedding=embeddings, persist_directory=persist_directory)
    # vectordb.persist()





def save_db_details(db_uri):

    unique_id = str(uuid4()).replace("-", "_")
    connection = psycopg2.connect(db_uri)
    cursor = connection.cursor()

    tables_and_columns = get_basic_table_details(cursor)

    ## Get all the tables and columns and enter them in a pandas dataframe
    df = pd.DataFrame(tables_and_columns, columns=['table_name', 'column_name', 'data_type'])
    filename_t = 'csvs/tables_' + unique_id + '.csv'
    df.to_csv(filename_t, index=False)

    create_vectors(filename_t, "./vectors/tables_"+ unique_id)

    ## Get all the foreign keys and enter them in a pandas dataframe
    foreign_keys = get_foreign_key_info(cursor)
    df = pd.DataFrame(foreign_keys, columns=['table_name', 'foreign_key', 'foreign_key_details', 'referred_table', 'referred_columns'])
    filename_fk = 'csvs/foreign_keys_' + unique_id + '.csv'
    df.to_csv(filename_fk, index=False)

    cursor.close()
    connection.close()

    return unique_id


# def generate_template_for_sql(query, table_info, db_uri):
#     template = ChatPromptTemplate.from_messages(
#             [
#                 SystemMessage(
#                     content=(
#                         f"You are an assistant that can write SQL Queries."
#                         f"Given the text below, write a SQL query that answers the user's question."
#                         f"DB connection string is {db_uri}"
#                         f"Here is a detailed description of the table(s): "
#                         f"{table_info}"
#                         "Prepend and append the SQL query with three backticks '```'"
                        
                        
#                     )
#                 ),
#                 HumanMessagePromptTemplate.from_template("{text}"),

#             ]
#         )
    
#     answer = chat_llm(template.format_messages(text=query))
#     return answer.content



def generate_template_for_sql(query, relevant_tables, table_info, foreign_key_info):
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



def check_if_users_query_want_general_schema_information_or_sql(query):
    template = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content=(
                        
                        f"In the text given text user is asking a question about database "
                        f"Figure out whether user wants information about database schema or wants to write a SQL query"
                        f"Answer 'yes' if user wants information about database schema and 'no' if user wants to write a SQL query"
                        
                    )
                ),
                HumanMessagePromptTemplate.from_template("{text}"),

            ]
        )
        
    answer = chat_llm(template.format_messages(text=query))
    print(answer.content)
    return answer.content


def prompt_when_user_want_general_db_information(query, db_uri):
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






def get_the_output_from_llm(query, unique_id, db_uri):
    ## Load the tables csv
    filename_t = 'csvs/tables_' + unique_id + '.csv'
    df = pd.read_csv(filename_t)

    ## For each relevant table create a string that list down all the columns and their data types
    table_info = ''
    for table in df['table_name']:
        table_info += 'Information about table' + table + ':\n'
        table_info += df[df['table_name'] == table].to_string(index=False) + '\n\n\n'

    answer_to_question_general_schema = check_if_users_query_want_general_schema_information_or_sql(query)
    if answer_to_question_general_schema == "yes":
        return prompt_when_user_want_general_db_information(query, db_uri)
    else:
        vectordb = Chroma(embedding_function=embeddings, persist_directory="./vectors/tables_"+ unique_id)
        retriever = vectordb.as_retriever()
        docs = retriever.get_relevant_documents(query)
        print(docs)

        relevant_tables = []
        relevant_tables_and_columns = []

        for doc in docs:
            table_name, column_name, data_type = doc.page_content.split("\n")
            table_name= table_name.split(":")[1].strip()
            relevant_tables.append(table_name)
            column_name = column_name.split(":")[1].strip()
            data_type = data_type.split(":")[1].strip()
            relevant_tables_and_columns.append((table_name, column_name, data_type))

        ## Load the tables csv
        filename_t = 'csvs/tables_' + unique_id + '.csv'
        df = pd.read_csv(filename_t)

        ## For each relevant table create a string that list down all the columns and their data types
        table_info = ''
        for table in relevant_tables:
            table_info += 'Information about table' + table + ':\n'
            table_info += df[df['table_name'] == table].to_string(index=False) + '\n\n\n'


        
        ## Load the foreign keys csv
        filename_fk = 'csvs/foreign_keys_' + unique_id + '.csv'
        df_fk = pd.read_csv(filename_fk)
        ## If table from relevant_tables above lies in refered_table or table_name in df_fk, then add the foreign key details to a string
        foreign_key_info = ''
        for i, series in df_fk.iterrows():
            if series['table_name'] in relevant_tables:
                text = table + ' has a foreign key ' + series['foreign_key'] + ' which refers to table ' + series['referred_table'] + ' and column(s) ' + series['referred_columns']
                foreign_key_info += text + '\n\n' 
            if series['referred_table'] in relevant_tables:
                text = table + ' is referred to by table ' + series['table_name'] + ' via foreign key ' + series['foreign_key'] + ' and column(s) ' + series['referred_columns']
                foreign_key_info += text + '\n\n'

    
        return generate_template_for_sql(query, relevant_tables, table_info, foreign_key_info)





def execute_the_solution(solution, db_uri):
    connection = psycopg2.connect(db_uri)
    cursor = connection.cursor()
    _,final_query,_ = solution.split("```") 
    final_query = final_query.strip('sql')
    cursor.execute(final_query)
    result = cursor.fetchall()
    return str(result)





# Function to establish connection and read metadata for the database
def connect_with_db(uri):
    st.session_state.db_uri = uri
    st.session_state.unique_id = save_db_details(uri)

    return {"message": "Connection established to Database!"}

# Function to call the API with the provided URI
def send_message(message):
    solution = get_the_output_from_llm(message, st.session_state.unique_id, st.session_state.db_uri)
    result = execute_the_solution(solution, st.session_state.db_uri)
    return {"message": solution + "\n\n" + "Result:\n" + result}



# ## Instructions
st.subheader("Instructions")
st.markdown(
    """
    1. Enter the URI of your RDS Database in the text box below.
    2. Click the **Start Chat** button to start the chat.
    3. Enter your message in the text box below and press **Enter** to send the message to the API.
    """
)

# Initialize the chat history list
chat_history = []

# Input for the database URI
# uri = st.text_input("Enter the RDS Database URI")

if st.button("Start Chat"):
    if not uri:
        st.warning("Please enter a valid database URI.")
    else:
        st.info("Connecting to the API and starting the chat...")
        chat_response = connect_with_db(uri)
        if "error" in chat_response:
            st.error("Error: Failed to start the chat. Please check the URI and try again.")
        else:
            st.success("Chat started successfully!")

# Chat with the API (a mock example)
st.subheader("Chat with the API")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # response = f"Echo: {prompt}"
    response = send_message(prompt)["message"]
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.text(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Run the Streamlit app
if __name__ == "__main__":
    st.write("This is a simple Streamlit app for starting a chat with an RDS Database.")