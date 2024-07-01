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