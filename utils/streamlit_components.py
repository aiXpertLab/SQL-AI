import streamlit as st


def streamlit_ui(main_title):
    st.set_page_config(page_title='AI SQL Linguist 👋', page_icon="💯", ),
    st.title(main_title)  # not accepting default

    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://omnidevx.netlify.app/logo/aipro.png);
                background-size: 300px; /* Set the width and height of the image */
                background-repeat: no-repeat;
                padding-top: 80px;
                background-position: 15px 10px;
            }
        </style>
        """,
                unsafe_allow_html=True,
                )
