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
    """
       A class to represent the chat user interface for handling messages
       and interacting with the database and language model handlers.

       Attributes:
       ----------
       db_handler : object
           The database handler object to interact with the database.
       llm_handler : object
           The language model handler object to interact with the language model.
       vector_or_others : str
           A string indicating whether to use vector-based responses or other types.

       Methods:
       -------
       send_message(message: str) -> dict:
           Processes the input message and returns the response.

       run():
           Runs the chat UI, displaying messages and handling user input.
       """
    def __init__(self, db_handler, llm_handler, vector_or_others):
        """
        Constructs all the necessary attributes for the ChatUI object.

        Parameters:
        ----------
        db_handler : object
            The database handler object to interact with the database.
        llm_handler : object
            The language model handler object to interact with the language model.
        vector_or_others : str
            A string indicating whether to use vector-based responses or other types.
        """
        self.db_handler = db_handler
        self.llm_handler = llm_handler
        self.vector_or_others = vector_or_others

    def send_message(self, message):
        """
        Processes the input message and returns the response.

        Parameters:
        ----------
        message : str
            The message to be processed.

        Returns:
        -------
        dict:
            A dictionary containing the response message and the result of executing the SQL.
        """
        if self.vector_or_others == 'vector':
            print('vector')
            respond_contents = self.llm_handler.get_response_from_llm_vector(message)
        else:
            respond_contents = self.llm_handler.get_response_from_llm(message)

        result = self.db_handler.execute_sql(respond_contents)


        result = result.replace("),", "),  \n")

        return {"message": respond_contents + "\n\n ###### Result: ###### \n\n" + result}

    def run(self):
        """
        Runs the chat UI, displaying messages and handling user input.
        """
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("⌨️ ask me "):
            st.chat_message("user").markdown(prompt)            # 1.Display user message in chat message container

            st.session_state.messages.append(
                {"role": "user", "content": prompt})            # 2. Add user message to chat history

            response = self.send_message(prompt)["message"]     # 3. Get message from ChatGPT
            with st.chat_message("assistant"):
                st.info(response)                           # 4. Display message from ChatGPT

            st.session_state.messages.append(
                {"role": "assistant", "content": response})     # 5. keep history
