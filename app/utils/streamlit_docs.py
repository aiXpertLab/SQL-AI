import streamlit as st


def postgre_intro():
    st.markdown(
        """
        When sending entire columns and tables as context to the prompt is not practical, VectorDB provides help.
        ###### [Click to check Sample Database ERD](https://omnidevx.netlify.app/logo/postgresqlerd.png)

        ##### Sample queries
        - Group films based on: 1 hour or less, Between 1-2 hours, Between 2-3 hours, More than 3 hours.
        - How many films are there in each film category?
        - List last names of actors, as well as top 5 of how many actors have that last name.
        - Get a list of top 5 active customers, ordered by their first name

        ##### Challenges
        - Show the top 5 actors and actresses ordered by how many movies they are featured in
        - Can you list the top 5 film genres by their gross revenue?
        - The music of Queen and Kris Kristofferson have seen an unlikely resurgence. As an unintended consequence, films starting with the letters K and Q have also soared in popularity. display the titles of movies starting with the letters K and Q whose language is English Use subqueries to display all actors who appear in the film Alone Trip
        """)
    st.info("DON'T TRY: `DELETE, TRUNCATE, DROP TABLE, DROP DATABASE` ")


def main_intro():
    st.write('''
         
        ### LLM has become a valuable tool for SQL query generation and optimization for several reasons:
        - Speed and efficiency: LLM can generate SQL queries quickly, helping developers and analysts save time on query writing. Especially useful for those who don't write SQL as their primary job duty.
        - Learning tool: LLM can serve as an excellent learning resource. It can provide examples, explain query structures, and introduce new concepts, helping users expand their SQL knowledge and skills.
        - Problem-solving assistance: LLM can help tackle specific SQL challenges. For instance, it can suggest solutions for filtering data in particular instances or introduce advanced concepts like row partitioning to solve complex problems.
        - Query optimization: LLM can analyze existing SQL statements, identify inefficiencies, and suggest optimized alternatives. 
        It can improve query performance and reduce costs in data warehouses.
        - Broad knowledge base: Due to its extensive training data, LLM is aware of various SQL functions, operations, and best practices across different SQL flavors (e.g., MySQL, PostgreSQL).
        - Consistency: LLM doesn't tire or get distracted, ensuring a consistent level of output quality.

            ### Let's explore the potential of the AI SQL!
         ''')
