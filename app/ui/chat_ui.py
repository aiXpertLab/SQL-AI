"""
    Module Name: StreamlitUI
    Version: 1.0

    Description:
    Chatbot, connected with a database and a language model. It manages session states, initializes
    database connections, and facilitates chat interactions.

    Classes:
    - StreamlitUI: A class to create and manage the Streamlit interface for database and language model interactions.

    Methods:
    - __init__(self, db_handler, llm_handler): Initializes session_state: message
    - start_chat(self, uri): Establishes a connection to the database.
    - run(self): Main method to run the Streamlit application.

    Usage:
    Instantiate the StreamlitUI class with appropriate database and language model handlers,
    then call the run method to start the Streamlit application.
"""

import streamlit as st


class ChatUI:

    def __init__(self, db_handler, llm_handler):
        self.db_handler = db_handler
        self.llm_handler = llm_handler
        self.unique_id = ''

    def connect_to_db(self) -> dict:
        try:
            self.unique_id = self.db_handler.save_db_details()  # st.session_state: db_uri, unique_id
            st.code(f'connect_to_db.chatUI: {self.unique_id}')
            return {"message": "Connection established to Database!"}
        except Exception as e:
            return {"error": str(e)}

    def send_message(self, message):

        solution = self.llm_handler.get_the_output_from_llm(message, self.unique_id)
        result = self.llm_handler.execute_the_solution(solution)

        return {"message": solution + "\n\nResult:\n" + result}

    def display_chat(self):

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        if prompt := st.chat_input("Start with: show tables"):
            st.chat_message("user").markdown(prompt)            # 1.Display user message in chat message container

            st.session_state.messages.append(
                {"role": "user", "content": prompt})            # 2. Add user message to chat history
            # st.write(st.session_state)

            response = self.send_message(prompt)["message"]     # 3. Get message from ChatGPT

            with st.chat_message("assistant"):
                st.markdown(response)                           # 4. Display message from ChatGPT

            st.session_state.messages.append(
                {"role": "assistant", "content": response})     # 5. keep history

    def run(self):
        if not st.session_state.get("db_uri"):
            st.error("Please enter a valid database URI.")
        else:
            chat_response = self.connect_to_db()  # "message": "Connection established to Database!"

            if "error" in chat_response:
                st.error(f"Error: {chat_response['error']}")
            else:
                st.success("Chat started successfully!")

        self.display_chat()
