import streamlit as st


def postgre_intro():
    st.markdown(
        """
        ###### [Click to check Sample Database ERD](https://omnidevx.netlify.app/logo/postgresqlerd.png)
        ###### [Click to setup your own database](https://ai-pro.gitbook.io/ai-sql-linguist/installation/database-uri)

        ##### Sample queries
        - List all the films by ordered by their length
        - List how many films there are in each film category
        - Show the actors and actresses ordered by how many movies they are featured in
        - Get a list of all active customers, ordered by their first name

        ##### Challenge
        - What is the total revenue of each rental store?
        - Can you list the top 5 film genres by their gross revenue?
        - The film.description has the text type, allowing for full text search queries, what will you search for?        
        """)
    st.info("DON'T TRY: `DELETE, TRUNCATE, DROP TABLE, DROP DATABASE` ")


def main_intro():
    st.write('''
         
        ### ChatGPT has become a valuable tool for SQL query generation and optimization for several reasons:
        - Speed and efficiency: ChatGPT can generate SQL queries quickly, helping developers and analysts save time on query writing. This is especially useful for those who don't write SQL as their primary job duty.
        - Learning tool: For SQL beginners, ChatGPT serves as an excellent learning resource. It can provide examples, explain query structures, and introduce new concepts, helping users expand their SQL knowledge and skills.
        - Problem-solving assistance: ChatGPT can help tackle specific SQL challenges. For instance, it can suggest solutions for filtering data in particular instances or introduce advanced concepts like row partitioning to solve complex problems.
        - Query optimization: ChatGPT can analyze existing SQL statements, identify inefficiencies, and suggest optimized alternatives. This is particularly valuable for improving query performance and reducing compute costs in data warehouses.
        Broad knowledge base: Due to its extensive training data, ChatGPT is aware of various SQL functions, operations, and best practices across different SQL flavors (e.g., MySQL, PostgreSQL).
        - Consistency: Unlike humans, ChatGPT doesn't tire or get distracted, ensuring a consistent level of output quality.

            ### Let's explore the potential of the AI SQL!
         ''')
