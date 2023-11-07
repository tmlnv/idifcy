"""Сообщение в sidebar"""
import streamlit as st


def custom_sidebar():
    st.sidebar.write("""
    ### Credits:
    #### Artem Leonov

    Follow me on [GitHub](https://github.com/tmlnv)

    --------------
    License: MIT

    """)
    st.write("")
    st.sidebar.write("")
